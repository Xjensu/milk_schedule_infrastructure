# Single-host deployment and descriptor repair — 2026-10-17

This runbook supersedes the October 16 repair guide for this release. It upgrades an existing installation without deleting PostgreSQL, MinIO, Redis or antivirus data. Commands run from the existing infrastructure checkout on the server; Docker commands use `sudo`.

## What changes

Compose's built-in DNS replaces Consul on this single host. The default deployment removes Consul, ACL bootstrap, PostgreSQL/Redis/MinIO registrars, the Python Nginx supervisor and consul-template. Rails/API/Python applications use `db`, `redis`, `minio`, `api_geteway` and `scheduler` directly. Nginx refreshes backend addresses through Docker DNS every ten seconds, including when containers are replaced. Idle registration loops and duplicate Consul readiness requests disappear.

The default Rails replica count is one. Existing installations must explicitly set `WEB_REPLICAS=1` to replace their previous value. Multiple replicas remain supported through Docker DNS when actually required. Keep `WEB_CONCURRENCY=1` initially.

The separate web operations console is optional (`operations` profile). Nginx resolves its hostname only on an actual `/ops/` request, so a disabled console causes no idle DNS retry loop. Maintenance commands remain available over SSH. The unused legacy frontend and experimental Solr service are absent from the base Compose configuration. Their historical volumes are preserved.

The Excel processor explicitly selects its installed psycopg2 driver for direct PostgreSQL URLs; this prevents a missing-psycopg3 startup failure.

Docker Compose 2.20.2 or newer is required for `start_interval`: health checks probe every two seconds during startup, then return to their normal steady interval. Verify `docker compose version` before deploying.

The following services remain because they own real product behavior: PostgreSQL, Redis, MinIO, Rails, API, Excel processing, outbox relay, media sanitization, notice exports, schedule-generation worker, scheduling engine and signature updater. MinIO bucket initialization is a one-shot job. Deleting these workers would break processing or silently leave jobs unfinished.

The descriptor repair must be deployed in the Rails image, not just infrastructure: short-lived HTTP clients must close their owning pools, and readiness must check Redis/API even in direct-DNS mode. A larger descriptor limit is headroom, not proof of repair. Falcon remains because the existing gateways and cache use its Async reactor; replacing it requires a separate transport migration.

FreshClam is not a prerequisite for serving ordinary pages. Required scans must reject uploads/processing while signatures are missing, stale or unavailable. The updater health check continues to report freshness failure, and a CDN block remains an operational incident. Do not disable scanning or widen the freshness limit to disguise it.

## 1. Record and back up

Record the old infrastructure commit and old image overrides for rollback. Do not print full environment files, full Docker inspection output or expanded Compose configuration: these contain secrets.

```bash
git status --short
git rev-parse HEAD
sudo ./deploy/bin/compose.sh ps -a
sudo ./deploy/bin/compose.sh images
umask 077
mkdir -p backups
sudo ./deploy/bin/compose.sh exec -T db sh -c \
  'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' \
  > "backups/postgres-$(date +%Y%m%d-%H%M%S).dump"
```

Back up object storage and private environment files through the established backup procedure. Verify restoration independently. Never run `down -v`, `docker volume prune`, regenerate secrets or reseed during this upgrade. Keep `COMPOSE_PROJECT_NAME` unchanged so existing volumes retain their identity.

## 2. Install the matching release

The infrastructure, Rails, API and Excel source branches are `codex/simple-deployment-2026-10-17` in their owning repositories. For the `milk_proto` workspace mirror, use `codex/simple-deployment-workspace-2026-10-17`.

On the infrastructure server checkout:

```bash
git fetch origin codex/simple-deployment-2026-10-17
git merge --ff-only origin/codex/simple-deployment-2026-10-17
```

Fetch and fast-forward the infrastructure revision accompanying this release. Resolve any server-specific changes deliberately; do not `reset --hard`. Keep the existing `.env.local` and its credentials. Set these values only after the corresponding images have been built, published and verified:

```dotenv
WEB_IMAGE=xjensu/table-bsut-by:2026-10-17-1
API_IMAGE=xjensu/table-api:2026-10-17-1
EDGE_IMAGE=xjensu/table-edge:2026-10-17-1
MINIO_INIT_IMAGE=xjensu/table-minio-init:2026-10-17-1
EXCEL_IMAGE=xjensu/excel-processor:2026-10-17-1
WEB_REPLICAS=1
WEB_CONCURRENCY=1
CLAMAV_MAX_SIGNATURE_AGE_SECONDS=259200
API_GETEWAY_URL=http://api_geteway:2300
MINIO_ENDPOINT=http://minio:9000
REDIS_HOST=redis
POSTGRES_HOST=db
```

Retain the working `IMAGE_TAG` for the scheduler image. Five images are updated: Rails, API, edge, MinIO initialization and Excel processor. All services using `API_IMAGE` must use the new API image together. Check the accompanying release evidence for publication status; a tag in this document alone is not proof of publication.

Verify that existing `DATABASE_URL` and `REDIS_URL` use Compose hostnames `db` and `redis`, with the existing credentials and URL encoding. If their definitions interpolate `${POSTGRES_HOST}` and `${REDIS_HOST}`, update those host variables rather than replacing credentials. Former Consul deployments may have ignored incorrect fallback URLs until now.

Keep the working pinned MinIO image, public object endpoint, CORS origin and network restrictions. The network is still named `discovery` for compatibility; the name no longer implies a registry service. Existing `deploy/generated` tokens can remain untouched for rollback and are no longer mounted in application containers.

```bash
python3 deploy/bin/prepare-discovery.py
sudo ./deploy/bin/compose.sh config --quiet
sudo ./deploy/bin/compose.sh pull
```

The preparation script keeps its old filename for compatibility. It now generates LAN/network/firewall policy only and preserves the existing subnet. Review unexpected interface/subnet changes before proceeding.

If using a private FreshClam mirror, keep the existing private configuration and use its overlay for every applicable `up` command:

```bash
sudo ./deploy/bin/compose.sh -f deploy/antivirus/compose.mirror.yml \
  up -d --no-build clamav_signatures
```

Honor cooldown periods. The mirror URL in the example is a placeholder, not a maintained public service. Neither this release nor a container restart removes a CDN denial.

## 3. Recreate during a maintenance window

The following targeted retirement removes only old project-labelled infrastructure containers, never volumes. It does not prune unrelated containers or monitoring stacks. Stop the old optional console separately if it is running and not wanted:

```bash
sudo python3 deploy/bin/retire-discovery.py
sudo ./deploy/bin/compose.sh --profile operations stop ops_console
sudo ./deploy/bin/compose.sh up -d --no-build --wait --wait-timeout 120 \
  db redis minio scheduler
sudo ./deploy/bin/compose.sh up -d --no-build minio_init
sudo ./deploy/bin/compose.sh up -d --no-build
sudo python3 deploy/bin/install-project-firewall.py
```

No schema migration or seed is required for this repair. Recreating containers applies image, environment and `ulimits` changes; `restart` alone does not. Ordinary Compose recreation does not guarantee zero downtime.

For subsequent releases that actually include migrations, `sudo ./deploy/bin/deploy.sh` performs preparation, image pulls, targeted retirement, dependency startup, migration, application startup and firewall installation. `deploy-discovery.sh` remains a compatibility alias. Do not run seed automatically on upgrades.

The existing freshness health check can remain unhealthy during a CDN block. Consequently, do not interpret a global `compose up --wait` failure by itself as a website failure: inspect readiness and antivirus health separately.

## 4. Verify service and container replacement

```bash
sudo ./deploy/bin/compose.sh ps -a
sudo ./deploy/bin/compose.sh exec -T schedule_web \
  curl -fsS --max-time 10 http://127.0.0.1:3000/readyz
sudo ./deploy/bin/compose.sh exec -T api_geteway \
  curl -fsS --max-time 10 http://127.0.0.1:2300/readyz
sudo ./deploy/bin/compose.sh exec -T nginx nginx -t
sudo ./deploy/bin/compose.sh exec -T nginx cat /etc/nginx/upstreams.conf
sudo ./deploy/bin/compose.sh logs --since=10m --tail=100 schedule_web api_geteway nginx
```

Expect Rails readiness 200 with Redis and API true. Nginx upstream configuration now contains hostnames with `resolve`; `/run/nginx/upstreams.conf` is obsolete. A temporary backend failure produces 503 without permanently overwriting an upstream with `127.0.0.1:9 down`. Never bypass readiness to conceal dependency failures.

Verify public pages, current CSS/JS URLs, administrator login and edit/reload. Check one Excel import and notice export when antivirus is healthy; stale signatures must prevent unsafe processing with a clear failure rather than silently accepting it. Read job history before retrying an upload after a timeout.

In staging, force-recreate API and Rails and verify the public endpoint recovers after DNS refresh without restarting Nginx. Verify readiness becomes unavailable during an API outage and returns after recovery. Do not perform this disruption test on a busy production server.

## 5. Prove descriptors are bounded

```bash
sudo ./deploy/bin/compose.sh exec -T schedule_web ruby \
  < deploy/bin/rails-fd-report.rb
```

Capture a baseline after warm-up, after ten minutes idle, after repeated readiness calls, after representative traffic, and beyond the previous multi-day failure window. The report discovers current worker PIDs. Repeat with `--index 2` if you deliberately configured a second replica.

Descriptor counts should settle; they should not increase in proportion to idle probes or completed requests. Compare the actual image digest and source revision serving traffic before concluding a previous fix was deployed. A high limit can postpone exhaustion while hiding continued growth.

If growth resumes, collect descriptor categories and socket states/destinations before restarting. Investigate the owning transport; do not blindly blame DNS, Redis or the HTTP server based only on `EMFILE`. Alert on growth and usage relative to the soft limit, readiness failure, signature age and public 503s. Restart is temporary mitigation, not evidence of a permanent fix.

## 6. Optional operations console

The normal administrator panel is part of Rails and remains enabled. Only the separate `/ops/` console is optional:

```bash
sudo ./deploy/bin/compose.sh --profile operations up -d --no-build ops_console
```

Keep its independent credentials and LAN restrictions. With the console disabled, `/ops/` is unavailable; business administration and SSH maintenance remain usable.

## 7. Rollback

Restore the recorded infrastructure revision and image overrides together, preserving all data and private generated files. Recreate the old discovery/registrar/edge services if rolling back to Consul-based ingress. The retained Consul volume and tokens allow that rollback; do not delete them during initial acceptance. This repair has no schema migration to undo.

No remote deployment or multi-day production soak is implied by local validation. Record the actual runtime evidence accompanying the release before calling the incident permanently resolved.


## Verified release evidence

The five images listed above were built and published. Source commits: Rails `1646796`, API `ddf921c`, Excel `deefab6`. Full immutable digests and machine-readable evidence are in [the release manifest](image-releases/2026-10-17-1.json).

Local checks completed:

- Starting the stopped stack reached Nginx startup in 17.01 seconds with cached images and existing data. This excludes image download/build time and is not a server performance guarantee.
- Rails passed 250 repeated readiness requests and returned to 9 worker descriptors. A separate 180-second idle observation (normal scheduled health checks still enabled) ranged from 9 to 11 and ended at 9. This is a short regression check, not a multi-day soak.
- A later snapshot of the same worker at 38,889 seconds of monotonic process age (over 10 hours) still showed 9 descriptors. This supplements the controlled idle check; it is not continuous monitoring for the whole interval.
- The API was replaced at a different IP address; Rails recovered without restart, and Nginx served the public page without reload.
- Administrator sign-in and persisted faculty read-back passed. Playwright loaded the public page without console errors.
- The Excel worker became healthy using the installed psycopg2 driver. Database-version maintenance worked without Consul.
- An authenticated valid GeoJSON upload was rejected with HTTP 503 when signatures were stale. No upload record was created. This proves fail-closed behavior, not successful scanning or ingestion.
- The separate optional-console DNS retry loop was removed; disabled operations no longer generate background resolution errors.

Live ClamAV updates remain subject to CDN/network access. The repair does not upgrade the bundled ClamAV engine, configure a trusted mirror automatically, or claim complete business spreadsheet/notice-export acceptance. Check updater and scanner versions separately; use supported patched engines. The long-running default is 13 containers instead of the former discovery-based topology; business workers are retained. Existing databases, storage, Redis files and retired Consul volumes are preserved.

For an optional server archive, retain the unchanged scheduler tag explicitly:

```bash
python3 deploy/bin/package-release.py 2026-10-17-1 --base-tag 2026-10-12-1
```

Substitute the actual retained scheduler release if different. The archive records runtime image references; it does not include private credentials or application sources.
