# Deployment guide — release 2026-10-19-1

This is the single operational guide for Milk Schedule: installation from zero, updates with existing data, migration from Consul, administrator setup, outage handling, automatic recovery, antivirus, diagnostics and rollback.

Use `Xjensu/milk_schedule_infrastructure`, branch `main`. The server pulls published Docker Hub images; it needs no application source, Ruby, Node.js, compiler or image builds. `milk_proto` is a separate project and is not a deployment source.

## Choose your starting point

| Situation | Start here |
| --- | --- |
| New server, or intentionally empty installation after removing containers/images | [A. Install from scratch](#a-install-from-scratch), then the shared checks and operations sections. |
| Existing simplified deployment; keep university data and accounts | [B. Update an existing installation](#b-update-an-existing-installation). |
| Existing Consul/registrar deployment | Read [C. Migrate from Consul](#c-migrate-from-consul), then follow section B with its additional retirement step. |
| Stack already running; verify recovery, scans or diagnose an outage | [D. Recovery and failover](#d-recovery-and-failover), [E. Antivirus](#e-antivirus), [F. Diagnostics](#f-diagnostics). |
| Normal shutdown/startup or rollback | [G. Stop restart and rollback](#g-stop-restart-and-rollback). |

The exact image set is shown in section A.3 and repeated for safe updating in section B. API/edge use `2026-10-19-1`; Rails/MinIO initialization/Excel use `2026-10-17-1`; scheduler retains `IMAGE_TAG=2026-10-12-1`. Do not set every component to the new tag. [The release manifest](image-releases/2026-10-19-1.json) records immutable application image digests.

Deleting containers/images does not necessarily delete named volumes or `storage/redis_data`. New credentials must never be pointed at an old PostgreSQL volume. A fresh installation uses a new directory/project; an update keeps its existing directory/project, secrets and data. No global Docker prune is needed.

## A. Install from scratch

This path creates a NEW database and administrator. Old teachers, groups, schedules and files are not restored automatically. To retain them, use section B with their existing private configuration and volumes/backups.

### A.1. Check server prerequisites

Use an amd64/x86_64 Linux server. These published images have been verified on amd64; an ARM server needs a separately verified image build.

Required: a systemd Linux host for automatic recovery, Docker Engine 25+ with the Compose plugin 2.20.2+ (or newer), Git, Python 3, `iproute2` and `iptables`. The firewall helper expects Docker's iptables backend and `DOCKER-USER` chain. Docker must already be running.

On Ubuntu/Debian, install the small host utilities if missing:

```bash
sudo apt-get update
sudo apt-get install -y git python3 iproute2 iptables
sudo systemctl enable --now docker
sudo docker version
sudo docker compose version
uname -m
```

Expected architecture: `x86_64`. If Docker is not installed, follow the official [Ubuntu](https://docs.docker.com/engine/install/ubuntu/) or [Debian](https://docs.docker.com/engine/install/debian/) installation instructions, including the Compose plugin, then repeat the checks above. Do not use the obsolete standalone `docker-compose` command.

The server must have outbound access to GitHub and the image registries, enough free disk for images/data, and a private IPv4 interface or an explicitly configured administration network. First-time image downloads take substantially longer than starting cached images.

Check that ports 80 and 9000 are available on their intended interfaces:

```bash
sudo ss -ltnp '( sport = :80 or sport = :9000 )'
```

Resolve an existing listener deliberately before continuing. Do not stop an unrelated server just to free the port.

### A.2. Clone the exact infrastructure branch

Run as your normal deployment user. The destination below must not already exist:

```bash
cd "$HOME"
git clone --branch main --single-branch \
  https://github.com/Xjensu/milk_schedule_infrastructure.git \
  milk-schedule-clean-20261019
cd "$HOME/milk-schedule-clean-20261019"
git rev-parse HEAD
test -f deploy/DEPLOYMENT_GUIDE.md
```

Use the current `main` branch, which includes the October 19 outage/recovery release. If GitHub requires authentication, use your authorized Git credentials; the SSH equivalent is `git@github.com:Xjensu/milk_schedule_infrastructure.git`.

No nested `apps/` repositories are needed. The server will pull the five updated images plus their existing dependencies.

### A.3. Generate NEW credentials and select a fresh project

```bash
python3 deploy/bin/init-env.py
```

This creates `.env.local` with generated database, Redis, storage, signing and administrator secrets. It also creates optional operations/monitoring credential files. Existing files are not overwritten; in this new directory you should see `Created`, not unexpected reused configuration.

Set an isolated project name for this clean installation:

```bash
python3 - <<'PY'
from pathlib import Path
import re
p = Path('.env.local')
text = p.read_text()
text = re.sub(r'^COMPOSE_PROJECT_NAME=.*$',
              'COMPOSE_PROJECT_NAME=milk_schedule_20261019', text, flags=re.M)
p.write_text(text)
p.chmod(0o600)
PY
sudo docker volume ls \
  --filter label=com.docker.compose.project=milk_schedule_20261019 \
  --format '{{.Name}}'
```

The last command should print nothing. If this exact project already has volumes, choose a different unused project name in `.env.local` before proceeding. Do not generate new database passwords against an old PostgreSQL volume. Fixed application container names also require the old application containers to have been removed, as assumed by this guide.

Open the private configuration:

```bash
nano .env.local
```

Verify this release selection:

```dotenv
COMPOSE_PROJECT_NAME=milk_schedule_20261019
IMAGE_NAMESPACE=xjensu
IMAGE_TAG=2026-10-12-1
WEB_IMAGE=xjensu/table-bsut-by:2026-10-17-1
API_IMAGE=xjensu/table-api:2026-10-19-1
EDGE_IMAGE=xjensu/table-edge:2026-10-19-1
MINIO_INIT_IMAGE=xjensu/table-minio-init:2026-10-17-1
EXCEL_IMAGE=xjensu/excel-processor:2026-10-17-1
WEB_REPLICAS=1
WEB_CONCURRENCY=1
HTTP_BIND_IP=0.0.0.0
HTTP_PORT=80
ASSUME_SSL=false
FORCE_SSL=false
```

`IMAGE_TAG` intentionally remains `2026-10-12-1` for the unchanged scheduler. API and edge use October 19 references; Rails, storage initialization and Excel retain October 17 references. Do not set every image to the new tag: a new scheduler image was not published for this repair. Immutable digests are recorded in [the release manifest](image-releases/2026-10-19-1.json).

Also review:

| Setting | Action |
| --- | --- |
| `SEED_ADMIN_EMAIL` | Choose the initial administrator email, or retain `admin@milk-schedule.local`. |
| `SEED_ADMIN_PASSWORD` | Keep the generated value and store it securely for first sign-in. It is not printed by seeding. |
| `CORS_ORIGINS` | Set the exact browser origin you will use, e.g. `http://table.bsut.by` or `http://192.168.1.50`, without a trailing slash. |
| `ADMIN_INTERFACE` | Normally blank. Set the actual interface name only if automatic detection cannot choose the correct private interface. |
| `ADMIN_LAN_CIDRS` | Normally blank for the detected local subnet. For another trusted LAN/VPN/proxy peer, list only the required trusted client CIDRs. |
| `CLAMAV_MAX_SIGNATURE_AGE_SECONDS` | Retain `259200` (three days). A larger number does not fix failed updates. |

Keep `db`, `redis`, `minio`, `api_geteway` and `scheduler` as INTERNAL hostnames. Do not replace these with `localhost` or the physical server IP. Preserve the generated secrets and the template's `${VARIABLE}` connection-URL expressions. Do not create a server `.env` or copy an old one into this fresh checkout.

If the server has only a public IPv4 address, explicitly set `LAN_BIND_IP` to that address and `ADMIN_LAN_CIDRS` to the exact trusted administrator client networks before preflight. The default LAN auto-detection is intended for the private-network setup.

With the default storage settings, notice-download links use the detected private address on port 9000. External clients need a separately reachable and secured storage endpoint configured through `NOTICE_EXPORT_PUBLIC_ENDPOINT`; website forwarding alone does not expose private storage.

This release serves HTTP. An existing outer TLS proxy, DNS and router forwarding are separate configuration. Administrator routes remain restricted by the configured network policy.

### A.4. Generate network policy and pull every required image

```bash
python3 deploy/bin/prepare-discovery.py
sudo ./deploy/bin/compose.sh config --quiet
sudo ./deploy/bin/compose.sh config --services
sudo ./deploy/bin/compose.sh config --images
sudo ./deploy/bin/compose.sh pull
```

Despite its legacy filename, `prepare-discovery.py` now generates only host network/firewall policy. It does not start Consul or require old tokens.

The service list should contain 14 default services, including the one-shot `minio_init`. It must not contain Consul, ACL initialization or registrars. The operations console and monitoring are optional and are not started here.

Use `config --quiet`, `--services` and `--images` as shown. Plain `config` expands secrets. Do not post private environment files or expanded container configuration in support messages.

If an image pull is denied because the repositories are private, authenticate the SAME Docker account/context used above:

```bash
sudo docker login --username xjensu
sudo ./deploy/bin/compose.sh pull
```

Enter an authorized pull token interactively. No registry credential should be put in the guide or shell command. A missing image/tag must be fixed before starting; there is no local-build fallback.

### A.5. Start only database/storage dependencies

```bash
sudo ./deploy/bin/compose.sh up -d --no-build --wait --wait-timeout 180 \
  db redis minio scheduler
sudo ./deploy/bin/compose.sh up -d --no-build minio_init
init_id=$(sudo ./deploy/bin/compose.sh ps -a -q minio_init)
if test -n "$init_id" && test "$(sudo docker wait "$init_id")" = "0"; then
  echo "Storage initialization: OK"
else
  echo "STOP: storage initialization failed; inspect minio_init logs." >&2
  false
fi
```

The first command waits for the four dependencies to become healthy. The remaining commands initialize private storage buckets and check the job's exit code. You must see `Storage initialization: OK`. Otherwise, inspect `sudo ./deploy/bin/compose.sh logs --tail=80 minio_init` and do not continue. `minio_init` exiting with code 0 is expected; do not use `up --wait` for this one-shot job.

PostgreSQL creates the empty database using the configured name and credentials when its NEW volume initializes. Do not start with `db.sh create`: the normal clean-install path is migrate, then seed.

### A.6. Create tables, reference data and the administrator

```bash
sudo ./deploy/bin/db.sh migrate
sudo ./deploy/bin/db.sh seed
sudo ./deploy/bin/db.sh version
```

All three commands must succeed. Migrations create the application schema. Seeding creates time slots, week types and the initial super-administrator from `.env.local`; it does not create your university's teachers, groups or schedules. The administrator password is not printed.

If seeding reports an existing administrator on a supposedly empty installation, stop and check the project/volume selection. A seed does not reset an existing password. Do not repeatedly regenerate credentials to troubleshoot authentication.

### A.7. Start the website and business workers

```bash
sudo ./deploy/bin/compose.sh up -d --no-build
sudo python3 deploy/bin/install-project-firewall.py
sudo python3 deploy/bin/install-recovery.py
sudo python3 deploy/bin/install-signature-refresh.py
sudo ./deploy/bin/compose.sh ps -a
```

The recovery installer must succeed and prints a `milk-recovery-…` unit name. Replace `<name>` below with that printed name:

```bash
sudo python3 deploy/bin/recover-services.py --dry-run
sudo systemctl is-enabled <name>.timer
sudo systemctl is-active <name>.timer
sudo journalctl -u <name>.service --since=10m --no-pager -n 30
```

Expect `enabled` and `active`. The one-shot service can be inactive between checks; the timer stays active. Its first sweep can wait up to 90 seconds. A dry-run alone does not install the timer. If the host has no systemd, use the explicit host-scheduler alternative in [section D](#d-recovery-and-failover).

The website uses one Rails replica by default. The scheduler, Excel worker, outbox relay, media sanitizer, notice exporter and schedule-generation worker remain because they provide application functions. No Consul registry or Python ingress supervisor runs.

Do not use a global `up --wait` for this step: the signature updater may be unhealthy during a CDN failure while ordinary pages are ready. Verify web readiness here and signature freshness in section E. The Excel worker applies its own additional migrations when it starts.

`install-project-firewall.py` must succeed. It applies project ingress rules after Nginx/MinIO exist; Docker must expose the expected iptables chain. Reapply it after relevant container/firewall/host changes. This release does not install an automatic boot-time firewall restoration service.

### A.8. Check startup before opening the panel

```bash
sudo ./deploy/bin/compose.sh exec -T schedule_web \
  curl -fsS --max-time 10 http://127.0.0.1:3000/readyz
sudo ./deploy/bin/compose.sh exec -T api_geteway \
  curl -fsS --max-time 10 http://127.0.0.1:2300/readyz
sudo ./deploy/bin/compose.sh exec -T nginx nginx -t
sudo ./deploy/bin/compose.sh logs --since=10m --tail=80 \
  api_geteway schedule_web excel_processor nginx
```

Expect both readiness requests to return HTTP 200; Rails reports `redis: true` and `api: true`. Nginx's configuration check should succeed. If the first check happens during startup, allow a short interval and retry; continuing 503 responses require inspecting the relevant logs.

Display the detected server URL:

```bash
python3 - <<'PY'
import json
from pathlib import Path
network = json.loads(Path('deploy/generated/network.json').read_text())
print('Website: http://' + network['address'])
print('Administrator: http://' + network['address'] + '/admin/')
PY
```

Use your configured hostname instead if appropriate. This procedure uses `HTTP_PORT=80` throughout. The October 19 proxy also preserves explicit host ports; configure origins and external forwarding consistently if you choose another port.

### A.9. Sign in and create the first application data

From an allowed LAN/VPN client, open the `/admin/` URL. Enter `SEED_ADMIN_EMAIL` and the generated `SEED_ADMIN_PASSWORD` from the private `.env.local` file. Change the bootstrap password after first sign-in and save the new password securely. The seed password then becomes historical; rerunning seed will not restore it.

Before importing scanned files, complete section E. Verify a simple real workflow: open the reference books, create a faculty, reload the page and confirm it remains. Enter/import your university's departments, teachers, subjects, groups, semesters and workload through the corresponding administrator pages. A fresh installation intentionally starts without that business data.

If CSS/JavaScript fail to load, inspect current asset URLs from a fresh page; both compiled assets and application code are already in the Rails image. Do not compile assets manually inside the running container.

## B. Update an existing installation

Run from the existing infrastructure checkout on the deployment server. This release uses the same Linux/Docker prerequisites as section A.1. Keep the SAME checkout directory, `COMPOSE_PROJECT_NAME`, secrets and database/storage/Redis data. Do not initialize new credentials or reseed during an update.

### B.1 Record the current version and back up

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

Record the current infrastructure commit and image overrides privately for rollback. Back up `.env.local`, generated private configuration, optional mirror settings, object storage and Redis data using the established consistent backup procedure; verify restoration independently. Never run `down -v`, volume pruning or credential regeneration for this update. Plain Compose configuration and full Docker inspection can expose secrets; do not post them.

### B.2 Fetch the infrastructure release

```bash
git fetch origin
git switch main
git pull --ff-only origin main
nano .env.local
```

Resolve tracked server changes deliberately; do not reset them blindly. Git does not update ignored `.env.local`. Change these release settings while retaining the existing project name, secrets and network/public endpoint settings:

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
CLAMAV_MAX_SIGNATURE_AGE_SECONDS=259200
```

Retain two Rails replicas only if deliberately required and adequately resourced; see section D. Clear conflicting exported image overrides if file values should be authoritative. If this is a Consul migration, apply the connection-setting checks in section C before continuing.

### B.3 Preflight and pull

```bash
python3 deploy/bin/prepare-discovery.py
sudo ./deploy/bin/compose.sh config --quiet
sudo ./deploy/bin/compose.sh config --images
sudo ./deploy/bin/compose.sh pull
```

Stop on missing/denied images and fix registry access as described in section A.4. Preflight retains the configured subnet and generates network policy. Review unexpected host/interface changes. If migrating from Consul, perform the targeted retirement in section C now, before recreating the application.

### B.4 Apply the update

For the October 19 update from the simplified October 17 deployment, no business migration or seed is required:

```bash
sudo ./deploy/bin/compose.sh up -d --no-build
sudo python3 deploy/bin/install-project-firewall.py
sudo python3 deploy/bin/install-recovery.py
sudo python3 deploy/bin/install-signature-refresh.py
sudo python3 deploy/bin/recover-services.py --dry-run
sudo ./deploy/bin/compose.sh ps -a
```

If coming from an older release requiring migrations, or performing later routine updates, use the deployment helper after reviewing the compatible image/schema release notes:

```bash
sudo ./deploy/bin/deploy.sh
```

It prepares networking, pulls images, retires old discovery containers, starts dependencies, migrates, starts applications, installs firewall/recovery policy and checks web readiness. It does NOT seed a first administrator. Recreating containers applies new images/environment/limits; `restart` alone does not. Normal recreation does not guarantee zero downtime.

If retaining a private antivirus mirror, include `-f deploy/antivirus/compose.mirror.yml` on every applicable Compose create/recreate command as explained in section E. The standard deployment helper does not accept that overlay; use the manual procedure instead. Where migrations are required, start healthy `db redis minio scheduler`, complete `minio_init` as in A.5, then run `sudo ./deploy/bin/db.sh migrate` before starting the full application. Do not seed on upgrades.

### B.5 Acceptance

Repeat the readiness/Nginx checks in A.8 and the timer checks in section D. Sign in using the existing administrator account and verify a normal read/edit/reload workflow. Existing passwords are unchanged. Complete the separate antivirus checks before scanned imports; worker health alone does not prove a full Excel or notice-export journey.

## C. Migrate from Consul

This section supplements section B when upgrading the old topology. Keep existing data, the same Compose project and matching credentials. Consul, ACL bootstrap, PostgreSQL/Redis/MinIO registrars and the Python Nginx supervisor are retired. Compose DNS now resolves services directly; the network remains named `discovery` for compatibility.

Before B.3, review `.env.local` connection settings:

```dotenv
API_GETEWAY_URL=http://api_geteway:2300
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
MINIO_ENDPOINT=http://minio:9000
```

Existing `DATABASE_URL` and `REDIS_URL` must derive from those internal names and the existing credentials. Correct an old fallback URL without changing its password; URL-reserved credentials need URL encoding. Preserve `NOTICE_EXPORT_PUBLIC_ENDPOINT`, signing keys, CORS origin and network restrictions. Old generated tokens and retired volumes can remain for rollback; current application containers no longer mount them.

After pulling the current images in B.3, run during a maintenance window:

```bash
sudo python3 deploy/bin/retire-discovery.py
sudo ./deploy/bin/compose.sh --profile operations stop ops_console
sudo ./deploy/bin/compose.sh up -d --no-build --wait --wait-timeout 180 \
  db redis minio scheduler
sudo ./deploy/bin/compose.sh up -d --no-build minio_init
```

Verify the one-shot job's exit code using A.5 before proceeding. The retirement helper targets only old discovery containers labelled for this project; it does not remove their volumes or other projects. The optional console stop is intentional if it is no longer wanted; section H explains how to enable it again.

Continue B.4, including migrations if required by the source release. All business workers remain because they own actual product functions. Rails keeps Falcon because its gateways/cache use the Async reactor. The published Rails image contains the HTTP-pool descriptor repair; a higher `nofile` limit alone is not a repair. Nginx uses `/etc/nginx/upstreams.conf` with Docker hostnames and `resolve`; the old `/run/nginx/upstreams.conf` is obsolete.

## D. Recovery and failover

### D.1 Outage behavior

Nginx starts independently of Rails/API health. Browser requests receiving upstream 500/502/503/504 show a branded static 503 page with local CSS/JavaScript, a safe GET retry button and a status check every 15 seconds (at most 40 active checks). Checks pause in hidden tabs. No failed POST, upload or save is replayed automatically. The page explicitly tells users to reconcile ambiguous writes first. It does not promise that an interrupted operation was rolled back.

Gateway failures on `/api/` or JSON requests return a structured 503 response with `Retry-After: 15` and `Cache-Control: no-store`. Existing API business responses, including their structured 503 reasons, remain intact. Authorization, validation, missing-route and rate-limit responses keep their distinct behavior. The fallback does not require fonts, Rails assets, API, Redis, PostgreSQL or CDN access. The optional operations console uses the same browser fallback.

Read-only public requests can retry another resolved Rails replica on connection failures/timeouts/502/503/504, with two attempts and a six-second retry window. Writes are never retried across replicas. Docker DNS refresh discovers replacement containers without reloading Nginx. One Rails replica remains the resource-conscious default; replica failover requires at least two replicas.

Internal worker outages do not redirect every page: their jobs retain existing durable status/retry semantics. A user request that fails with an intercepted server error shows the outage page. Worker recovery is described below; Nginx cannot infer a failed background job from an otherwise successful HTTP response.

### D.2 Automatic recovery policy

All long-running default services retain `restart: unless-stopped`: Docker restarts exited processes and resumes running services after daemon reboot. Explicitly stopped services remain stopped. The one-shot `minio_init` remains a successful completed job and is never auto-restarted by the controller.

The additional host timer checks every 30 seconds. It only acts on existing, running, explicitly labelled containers in this Compose project that Docker already marks `unhealthy`. It waits another 120 seconds, waits for declared `service_healthy` dependencies, then restarts that container. Per-container restart budgets persist privately under `deploy/generated/recovery/`: 300-second cooldown, exponential backoff, maximum three attempts per rolling hour. A controller lock prevents overlapping sweeps. Recreating a container creates a new identity/budget; ordinary restarts preserve it.

Nginx has a local liveness check independent of upstream availability. PostgreSQL, Redis, MinIO, API, Rails, scheduler and Excel retain or gain meaningful health checks. API's outbox, media, notice-export and generation workers now write a local heartbeat after completing each polling batch, including an empty queue. Their health check detects a loop stalled longer than `WORKER_HEARTBEAT_MAX_AGE` (default 1200 seconds), plus Docker's check retries and controller grace. File writes close immediately and do not retain descriptors. Long batches need an age above their legitimate maximum duration; do not reduce the default blindly.

The ClamAV updater is deliberately excluded from unhealthy-container restarts: stale signatures/CDN denial are external failures that a restart cannot repair. Its exited process still follows Docker's restart policy; scanning remains fail-closed. Budget exhaustion is logged; the timer does not erase the failure or restart indefinitely.

There is no extra recovery sidecar, Consul process, or Docker socket mounted into application containers. The root host timer has Docker control and must run trusted checkout code.

### D.3 Install and verify the host timer

Run from the persistent deployment checkout:

```bash
sudo python3 deploy/bin/install-recovery.py
sudo python3 deploy/bin/install-signature-refresh.py
sudo python3 deploy/bin/recover-services.py --dry-run
```

The installer prints a checkout-specific `milk-recovery-…` unit name. Replace `<name>` with that exact printed name:

```bash
sudo systemctl is-enabled <name>.timer
sudo systemctl is-active <name>.timer
sudo journalctl -u <name>.service --since=10m --no-pager -n 30
```

Expect `enabled` and `active`. The service is a one-shot sweep and can be inactive between runs; the timer remains active. Its first sweep can wait up to 90 seconds. A dry-run exit 0 confirms configuration access but does not install or enable the timer. Pulling images alone does not enable recovery.

The installer is safe to rerun from the SAME directory and survives reboot. Before moving or deleting that checkout, remove its timer, then reinstall from the new persistent location:

```bash
sudo python3 deploy/bin/install-recovery.py --remove
```

On a non-systemd host, schedule `recover-services.py` once a minute from a root-owned host scheduler/cron entry using its absolute path, and retain output in protected host logs. Do not enable both timer and cron. The controller lock prevents overlaps. The normal deploy helper expects systemd; use manual startup steps and this alternative scheduler on other hosts.

### D.4 Optional Rails replica failover

Set `WEB_REPLICAS=2` in the existing `.env.local` only if the host has enough memory/CPU for two Rails processes, then run:

```bash
sudo ./deploy/bin/compose.sh up -d --no-build schedule_web
```

Keep `WEB_CONCURRENCY=1` unless measured load justifies more. Shared sessions/Redis stay unchanged. Observe both replicas' readiness and resource use. This provides Rails process redundancy on one host; it cannot survive loss of the entire host, Docker, Nginx, or shared database/storage. Database/Redis/MinIO use recovery of their persistent instances, not unsafe ad hoc replication.

### D.5 Controlled failure checks

During a maintenance window, stop one Rails replica when using two and confirm safe public GET requests continue. Stopping both should show the static 503 page. Start them again and verify the page's status becomes available, then choose the retry action. The controller respects explicit stops; restore those containers yourself after the drill.

Stopping API or Redis should make the relevant requests report an outage. They must not return empty catalogues or a success code as a substitute for failure. Inspect actual request/worker status when diagnosing background jobs. Do not kill a database during real writes to test recovery.

If the restart budget is exhausted, inspect/fix the root cause and let the rolling hour expire or perform a deliberate operator restart. Do not delete recovery state as a routine fix.

## E. Antivirus

### E.1 Repair stale signatures while the CDN is blocked

A persistent signature volume can retain an obsolete database even when containers are healthy. The new refresh helper downloads the three signed ClamAV CVD files from the [Microsoft-hosted mirror](https://packages.microsoft.com/clamav/), verifies their embedded ClamAV signatures using an official verifier image, and atomically installs only newer versions. It then checks the actual embedded build date against the unchanged three-day freshness limit. No timestamp changes, disabled scans or FreshClam cooldown resets are used.

```bash
sudo python3 deploy/bin/refresh-signatures.py
sudo python3 deploy/bin/install-signature-refresh.py
```

Expect `Signature freshness: PASS`. The API/media scanners read the shared volume immediately; no API restart is needed. The installer prints `milk-signatures-…`; verify that timer with `sudo systemctl is-enabled <name>.timer`, `sudo systemctl is-active <name>.timer` and its service journal, as in section D. The timer refreshes every six hours. Conditional requests avoid repeatedly downloading unchanged databases; downloads have time/size bounds. The helper uses only this project's named signature volume and skips intentionally stopped/absent updater containers.

`CLAMAV_DATABASE_MIRROR` defaults to `https://packages.microsoft.com/clamav`; configure another maintained HTTPS CVD mirror if required. Files from a mirror must still pass cryptographic verification and freshness checks. No uploaded user files or credentials are sent to the mirror. `CLAMAV_SEED_IMAGE` defaults to the official `clamav/clamav:1.5` non-base image; it supplies the verifier and signed bootstrap data. Its [preloaded databases](https://docs.clamav.net/manual/Installing/Docker.html) are a fallback, not a daily feed: upstream image database refreshes may be less frequent than the three-day acceptance limit. If the mirror is unavailable, the helper tries the verified image seed and fails closed if that data is stale. If the registry is unavailable, an already-cached official verifier image can still be used.

Failures stay visible in the host service journal and do not relax required scanning. FreshClam continues its normal hourly attempts with its own cooldown state intact. The separate updater runtime image can stay pinned while the signed data feed advances.

For a workstation without passwordless sudo, install this timer using `python3 deploy/bin/install-signature-refresh.py --user`, verify it with `systemctl --user`, and enable lingering using `loginctl enable-linger` if permitted so it survives logout/reboot. Do not install both user and system copies. Before moving/deleting the checkout, run the same installer with `--remove` (and `--user` for a user installation).

On October 20, recovery first restored official-image daily version 28157 (October 18), then verified mirror version 28159 (October 20). Clean-file acceptance, EICAR rejection and a real administrator workbook upload were checked; the upload returned HTTP 201 and appeared in history. The synthetic empty workbook was removed; business-data import correctness was not inferred from that upload.

### E.2 Freshness and scanner checks

```bash
sudo ./deploy/bin/compose.sh logs --tail=100 clamav_signatures
sudo ./deploy/bin/compose.sh exec -T clamav_signatures \
  sh /opt/antivirus/check-signatures.sh
sudo ./deploy/bin/compose.sh exec -T api_geteway clamscan --version
sudo ./deploy/bin/compose.sh exec -T media_sanitizer clamscan --version
```

The freshness command must exit 0 for required scanning to proceed. The updater and API/sanitizer scanner binaries are separate; check their versions independently. The repair images do not upgrade the bundled scanner engine automatically.

Your previously reported CDN 403/429 block is not repaired by deleting images, changing project names, or reinstalling. If the official CDN remains inaccessible, use the verified mirror refresh in E.1, or configure an actual trusted, maintained mirror/proxy. Do not repeatedly force downloads, remove cooldown state as a workaround, or increase the age threshold to hide stale signatures.

An optional mirror configuration is supplied:

```bash
umask 077
cp deploy/antivirus/freshclam.conf.example deploy/antivirus/freshclam.conf
nano deploy/antivirus/freshclam.conf
sudo ./deploy/bin/compose.sh -f deploy/antivirus/compose.mirror.yml \
  config --quiet
sudo ./deploy/bin/compose.sh -f deploy/antivirus/compose.mirror.yml \
  up -d --no-build --no-deps clamav_signatures
```

Replace the example mirror URL BEFORE running this; it is a placeholder. The mirror must obtain current official signatures successfully. Use the overlay for every later Compose command that creates/recreates the updater. The private configuration is ignored by Git. See [ClamAV's official mirror instructions](https://docs.clamav.net/appendix/CvdPrivateMirror.html).

Ordinary pages/admin data entry remain available during a signature outage, but file operations requiring scanning fail closed. Therefore "the website started" is not proof that Excel import is ready. Once signatures and patched scanners are working, test a supported workbook and inspect processing history before retrying any timeout.

## F. Diagnostics

### F.1 File descriptors

```bash
sudo ./deploy/bin/compose.sh exec -T schedule_web ruby \
  < deploy/bin/rails-fd-report.rb
```

Save a baseline after startup and compare after ten minutes, an hour and longer idle operation. The report finds current PIDs automatically. Counts may vary with live connections, but should settle rather than grow continuously with completed probes. Compare against the soft limit; increasing that limit alone does not fix a leak.

If growth resumes, capture descriptor categories and socket destinations/states BEFORE restarting. Check the actual running image/revision and investigate the owning transport rather than assuming every `EMFILE` is a DNS problem. Observe beyond the earlier failure window; short checks do not prove a multi-day leak is eliminated.

### F.2 Worker progress and logs

```bash
sudo ./deploy/bin/compose.sh logs --since=10m --tail=80 \
  nginx api_geteway schedule_web excel_processor outbox_relay
sudo ./deploy/bin/compose.sh exec -T outbox_relay ruby -e \
  'puts "Heartbeat age: #{(Time.now - File.mtime("/tmp/milk-worker-heartbeat")).round}s"'
sudo ./deploy/bin/compose.sh ps -a
```

### F.3 Troubleshooting

| Symptom | Check |
| --- | --- |
| Old Consul/registrar services appear | Wrong repository branch/configuration; stop before deploying it. |
| API or Rails still references October 16 images | Existing override/shell environment or old template. Check `config --images`. |
| Database authentication fails | Old volume with new credentials, incorrect URL, or wrong project name. Do not delete it blindly. |
| Administrator missing | Successful `db.sh seed`, matching email, correct new database/project. |
| `/admin/` returns 403 | Client/proxy peer is outside the detected/configured administrator network. Use an allowed LAN/VPN client or deliberately configure its CIDR. |
| Public page returns 503 | API/Rails readiness, worker logs and Docker DNS. The old `/run/nginx/upstreams.conf` no longer applies. |
| Signature updater is unhealthy | Check actual signature freshness/CDN access separately from web readiness. |
| Excel worker restarts | Confirm `EXCEL_IMAGE=...:2026-10-17-1`, database readiness and worker logs. |
| Firewall installation fails | Docker iptables backend, `DOCKER-USER`, privileges and running Nginx/MinIO. |
| Recovery does not run | Verify the correct checkout's timer is enabled/active and inspect its journal; a dry-run alone is insufficient. |
| Worker remains unhealthy | Verify the October 19 API image, heartbeat age, dependencies and legitimate batch duration. |
| Outage page appears | Inspect upstream readiness; a rendered 503 page confirms error handling, not application recovery. |

## G. Stop restart and rollback

### G.1 Normal stop and resume

Stop containers while retaining this installation's data:

```bash
sudo ./deploy/bin/compose.sh stop
```

Start this SAME installation later, with the SAME directory, project name and credentials:

```bash
sudo ./deploy/bin/compose.sh up -d --no-build
sudo python3 deploy/bin/install-project-firewall.py
```

Do not seed or regenerate credentials on every restart. After a complete new installation, the shorter `deploy/bin/deploy.sh` is an update/startup helper; it migrates but does NOT seed a first administrator automatically. If retaining the mirror option, consistently include its overlay when creating/recreating the updater.

The timer respects intentional stops. Keep its service files enabled for normal resume; verify it after a host reboot. Reapply project firewall policy after host/container/firewall changes; this release does not install a separate boot-time firewall restoration service.

### G.2 Roll back the October 19 update

Remove the recovery timer first using D.3. Restore the recorded compatible infrastructure revision and API/edge `2026-10-17-1` overrides together, keeping data and secrets. Pull/recreate services and reapply firewall policy. Revert worker healthchecks together with the API image: October 17 workers do not emit the new heartbeat. This incremental release changes no business schema; an arbitrary future image rollback does not undo database migrations.

### G.3 Roll back a Consul topology migration

Restore the recorded pre-migration infrastructure revision AND matching image overrides, then recreate its discovery/registrar/edge services. Retained Consul volumes, generated tokens and old private settings are required. Preserve business data and credentials. Use the restore procedure tested with your backups if a separate migration changed schema/data; do not delete current volumes as a shortcut.

## H. Optional operations and release packaging

### H.1 Operations console

The application administrator panel is part of Rails and remains enabled. Only the separate `/ops/` console is optional:

```bash
sudo ./deploy/bin/compose.sh --profile operations up -d --no-build ops_console
```

It uses independent credentials in `deploy/ops/.env.local` and keeps LAN restrictions. Disabled `/ops/` does not disable the normal administrator panel. SSH database commands remain available. Optional monitoring has its own configuration under `deploy/observability`; it is not a prerequisite for starting the application.

### H.2 Optional image-only server archive

Git checkout is the standard server path. On the source workstation, package the exact mixed-version release with:

```bash
python3 deploy/bin/package-release.py 2026-10-19-1 \
  --base-tag 2026-10-12-1 --web-tag 2026-10-17-1 \
  --minio-init-tag 2026-10-17-1 --excel-tag 2026-10-17-1
```

The archive contains deployment files, this guide and image manifests; it excludes private credentials and application source. It does not build or publish images. API and edge `2026-10-19-1` are already published. Future releases require publishing compatible source in each owning repository and building/pushing the changed images before updating image references. Never push deployment workspace changes into the unrelated `milk_proto` project.

## I. Verification and limits

The October 17 base path was validated on a fresh project through pulls, storage initialization, migrations, seed, administrator login and persisted faculty creation. The October 19 stack additionally passed fresh-database migrations/seeding, all 12 non-antivirus long-running service healthchecks, HTML/JSON outage handling, failed POST safety, mixed healthy/failing Rails replica reads, Docker DNS recovery, restart grace/dependency/cooldown/budget/manual-stop/project-isolation checks and a real unhealthy-container restart. Four workers emitted empty-queue heartbeats; 1000 heartbeat writes did not grow descriptor counts. Generated systemd units passed structural validation. Desktop/mobile Playwright checks covered responsive layout, availability status and safe retry.

These were isolated local checks with synthetic data and alternate ports/container names. Shared application data and firewall policy were not changed; synthetic resources were removed. This consolidation changes documentation/packaging only and does not claim a production deployment, full workbook/notice-export acceptance, live ClamAV CDN updates or a multi-day workload soak. The static page requires a working Nginx; whole-host/ingress/database redundancy needs separate infrastructure.
