# Deployment guide — release 2026-10-19-1

Deploy from `Xjensu/milk_schedule_infrastructure`, branch `main`. The server pulls published Docker Hub images; it does not build application images or need the nested application repositories. `milk_proto` is a separate project and must not be used for deployment.

Choose the procedure that matches your data:

| Situation | Procedure |
| --- | --- |
| New server, or a new empty installation after deleting containers/images | [Complete clean installation](CLEAN_INSTALL_2026-10-17.md): prerequisites, credentials, image pulls, migrations, seed, administrator login and first data. The filename is retained; its contents cover the October 19 release. |
| Existing simplified deployment with data to preserve | Follow the update steps below, then [the recovery runbook](FAILOVER_2026-10-19.md). |
| Existing older Consul deployment | First follow [the topology migration](SIMPLIFIED_DEPLOYMENT_2026-10-17.md), preserving data and credentials, then apply the October 19 update below. |

Deleting containers/images does not necessarily remove volumes or Redis bind-mounted data. The clean-install procedure uses a new directory/project to avoid accidentally attaching new credentials to an old database. Do not use it to upgrade data you want to retain.

## Published image selection

Use this exact compatible set. Do not assign the October 19 tag to every image:

```dotenv
IMAGE_NAMESPACE=xjensu
IMAGE_TAG=2026-10-12-1
API_IMAGE=xjensu/table-api:2026-10-19-1
EDGE_IMAGE=xjensu/table-edge:2026-10-19-1
WEB_IMAGE=xjensu/table-bsut-by:2026-10-17-1
MINIO_INIT_IMAGE=xjensu/table-minio-init:2026-10-17-1
EXCEL_IMAGE=xjensu/excel-processor:2026-10-17-1
WEB_REPLICAS=1
WEB_CONCURRENCY=1
WORKER_HEARTBEAT_MAX_AGE=1200
```

`IMAGE_TAG` selects the unchanged scheduler. API and Nginx were published on October 19; Rails, storage initialization and Excel retain October 17 images. PostgreSQL, Redis, MinIO and ClamAV retain the pinned/default references from the current template. See [the release manifest](image-releases/2026-10-19-1.json) for application image digests.

## Update an existing simplified installation

Run from the existing infrastructure checkout on the Linux deployment server. This path assumes a systemd host with Docker Engine/Compose, Python 3 and the existing generated network policy. Back up the database, private configuration, storage and Redis data using the established backup procedure before updating.

Keep the same checkout directory, `COMPOSE_PROJECT_NAME`, database/storage volumes and secrets. Do not run the credential initializer or seed as part of this update.

```bash
git fetch origin
git switch main
git pull --ff-only origin main
nano .env.local
```

Merge any real local tracked changes deliberately. Update the image references using the block above; preserve all other private values. Existing `.env.local` files are ignored by Git and are not updated by `git pull`. Clear conflicting exported image variables if they override the file.

Review the selection, pull and deploy:

```bash
python3 deploy/bin/prepare-discovery.py
sudo ./deploy/bin/compose.sh config --quiet
sudo ./deploy/bin/compose.sh config --images
sudo ./deploy/bin/compose.sh pull
sudo ./deploy/bin/compose.sh up -d --no-build
sudo python3 deploy/bin/install-project-firewall.py
sudo python3 deploy/bin/install-recovery.py
sudo python3 deploy/bin/recover-services.py --dry-run
sudo ./deploy/bin/compose.sh ps -a
```

This incremental October 19 release changes no business schema and needs no new seed. For later releases that add migrations, use `sudo ./deploy/bin/deploy.sh` after selecting their documented compatible images. That helper performs migrations, startup, firewall installation, timer installation and web readiness checks; it does not seed a first administrator.

If using the optional antivirus mirror overlay, retain `-f deploy/antivirus/compose.mirror.yml` on Compose commands that create/recreate the updater. Use the explicit manual procedure rather than the regular helper when you need that overlay. Do not print plain `compose config`: it expands secrets.

## Verify the application and recovery separately

```bash
sudo ./deploy/bin/compose.sh exec -T schedule_web \
  curl -fsS --max-time 10 http://127.0.0.1:3000/readyz
sudo ./deploy/bin/compose.sh exec -T api_geteway \
  curl -fsS --max-time 10 http://127.0.0.1:2300/readyz
sudo ./deploy/bin/compose.sh exec -T nginx nginx -t
sudo ./deploy/bin/compose.sh logs --since=10m --tail=80 \
  nginx api_geteway schedule_web outbox_relay
```

Both readiness requests must return HTTP 200; Rails reports `redis: true` and `api: true`. Nginx must pass validation. Allow startup time, then inspect logs if checks continue to fail. Worker heartbeats should become healthy after a completed poll. `minio_init` is expected to be `Exited (0)`.

The recovery installer prints its checkout-specific unit name. Copy it into these commands, replacing `<name>` with the printed `milk-recovery-…` name:

```bash
sudo systemctl is-enabled <name>.timer
sudo systemctl is-active <name>.timer
sudo journalctl -u <name>.service --since=10m --no-pager -n 30
```

Expected timer results: `enabled` and `active`. The service is a one-shot sweep, so an inactive service between runs is normal; the timer must remain active. The first sweep can wait up to 90 seconds after timer activation. A dry-run exit code 0 confirms the controller can read this project's configuration; it does not prove the timer was installed. Pulling images alone does not enable host recovery.

The timer respects manual stops, waits for healthy dependencies and caps restart attempts. The ClamAV updater is excluded from unhealthy-triggered restarts. See [the recovery policy and failure drills](FAILOVER_2026-10-19.md) for precise timing, logs, optional two-replica Rails failover and rollback.

From an allowed administration network, open `/admin/`, sign in using the existing account and verify a normal read/edit/reload workflow. Existing passwords are not reset by this update. Administrator routes remain network-restricted; HTTPS/DNS/router configuration is separate from this HTTP release.

## Check scanning before file imports

```bash
sudo ./deploy/bin/compose.sh exec -T clamav_signatures \
  sh /opt/antivirus/check-signatures.sh
sudo ./deploy/bin/compose.sh logs --tail=80 clamav_signatures
```

The freshness check must exit 0 before required scanning can succeed. A CDN 403/429 or stale signatures are not repaired by reinstallation or restart loops. Ordinary pages can remain healthy while scanned uploads fail closed. Do not use a global `up --wait` as the acceptance gate for the entire stack; verify website readiness and signatures separately.

## Stop, restart and rollback

```bash
sudo ./deploy/bin/compose.sh stop
```

This intentionally stops the application while preserving data; the controller will not undo the stop. To resume from the same directory/configuration:

```bash
sudo ./deploy/bin/compose.sh up -d --no-build
sudo python3 deploy/bin/install-project-firewall.py
```

The already-installed timer remains enabled. Verify it is active after a host reboot and reapply firewall policy after relevant host/firewall changes. Remove the timer before moving/deleting its checkout with `sudo python3 deploy/bin/install-recovery.py --remove`, then reinstall from the new location if appropriate.

For rollback, follow [the coordinated infrastructure/API rollback](FAILOVER_2026-10-19.md#rollback). Revert worker healthchecks together with the API image; the older workers do not write the new heartbeat. Keep data volumes and credentials.

## Verification scope

The October 19 implementation was verified with an isolated fresh database, migration/seed, all 12 non-antivirus long-running services healthy, HTML/JSON outage responses, safe POST error handling, Rails replica failover, a real unhealthy-container restart and responsive browser checks. Generated systemd units passed structural validation. This documentation update adds no runtime changes and does not repeat deployment or claim a production rollout. A full host failure requires separate infrastructure redundancy; the static page is served only while Nginx is available.
