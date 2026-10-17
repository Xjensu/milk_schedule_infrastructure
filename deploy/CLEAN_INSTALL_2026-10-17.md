# Clean installation of the simplified release — 2026-10-17-1

Follow this guide after removing the previous application containers and images, or on a new Linux server. Everything runs from published images: no application source checkout, Docker builds, Ruby, Node.js or Python virtual environment is required on the server.

This guide creates a NEW database, new administrator and new private configuration. Existing teachers, groups, schedules and files are not restored automatically. If you need the old data, retain its volumes/backups AND matching private configuration and follow the upgrade guide instead.

Deleting images and containers does not necessarily delete volumes or `storage/redis_data`. To make this installation independent of leftovers, the steps below use a new directory and project name. They do not delete other Docker workloads or old data. No global prune commands are needed.

## 1. Check server prerequisites

Use an amd64/x86_64 Linux server. These published images have been verified on amd64; an ARM server needs a separately verified image build.

Required: Docker Engine 25+ with the Compose plugin 2.20.2+ (or newer), Git, Python 3, `iproute2` and `iptables`. The firewall helper expects Docker's iptables backend and `DOCKER-USER` chain. Docker must already be running.

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

## 2. Clone the exact infrastructure branch

Run as your normal deployment user. The destination below must not already exist:

```bash
cd "$HOME"
git clone --branch codex/simple-deployment-2026-10-17 --single-branch \
  https://github.com/Xjensu/milk_schedule_infrastructure.git \
  milk-schedule-clean-20261017
cd "$HOME/milk-schedule-clean-20261017"
git rev-parse HEAD
test -f deploy/CLEAN_INSTALL_2026-10-17.md
```

Use the branch above, not an older default branch or the previous Consul release. If GitHub requires authentication, use your authorized Git credentials; the SSH equivalent is `git@github.com:Xjensu/milk_schedule_infrastructure.git`.

No nested `apps/` repositories are needed. The server will pull the five updated images plus their existing dependencies.

## 3. Generate NEW credentials and select a fresh project

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
              'COMPOSE_PROJECT_NAME=milk_schedule_20261017', text, flags=re.M)
p.write_text(text)
p.chmod(0o600)
PY
sudo docker volume ls \
  --filter label=com.docker.compose.project=milk_schedule_20261017 \
  --format '{{.Name}}'
```

The last command should print nothing. If this exact project already has volumes, choose a different unused project name in `.env.local` before proceeding. Do not generate new database passwords against an old PostgreSQL volume. Fixed application container names also require the old application containers to have been removed, as assumed by this guide.

Open the private configuration:

```bash
nano .env.local
```

Verify this release selection:

```dotenv
COMPOSE_PROJECT_NAME=milk_schedule_20261017
IMAGE_NAMESPACE=xjensu
IMAGE_TAG=2026-10-12-1
WEB_IMAGE=xjensu/table-bsut-by:2026-10-17-1
API_IMAGE=xjensu/table-api:2026-10-17-1
EDGE_IMAGE=xjensu/table-edge:2026-10-17-1
MINIO_INIT_IMAGE=xjensu/table-minio-init:2026-10-17-1
EXCEL_IMAGE=xjensu/excel-processor:2026-10-17-1
WEB_REPLICAS=1
WEB_CONCURRENCY=1
HTTP_BIND_IP=0.0.0.0
HTTP_PORT=80
ASSUME_SSL=false
FORCE_SSL=false
```

`IMAGE_TAG` intentionally remains `2026-10-12-1` for the unchanged scheduler. The other five components use their explicit October 17 references. Do not set every image to the new tag: a new scheduler image was not published for this repair. Immutable digests are recorded in [the release manifest](image-releases/2026-10-17-1.json).

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

## 4. Generate network policy and pull every required image

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

## 5. Start only database/storage dependencies

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

## 6. Create tables, reference data and the administrator

```bash
sudo ./deploy/bin/db.sh migrate
sudo ./deploy/bin/db.sh seed
sudo ./deploy/bin/db.sh version
```

All three commands must succeed. Migrations create the application schema. Seeding creates time slots, week types and the initial super-administrator from `.env.local`; it does not create your university's teachers, groups or schedules. The administrator password is not printed.

If seeding reports an existing administrator on a supposedly empty installation, stop and check the project/volume selection. A seed does not reset an existing password. Do not repeatedly regenerate credentials to troubleshoot authentication.

## 7. Start the website and business workers

```bash
sudo ./deploy/bin/compose.sh up -d --no-build
sudo python3 deploy/bin/install-project-firewall.py
sudo ./deploy/bin/compose.sh ps -a
```

The website uses one Rails replica by default. The scheduler, Excel worker, outbox relay, media sanitizer, notice exporter and schedule-generation worker remain because they provide application functions. No Consul registry or Python ingress supervisor runs.

Do not use a global `up --wait` for this step: the signature updater may be unhealthy during a CDN failure while ordinary pages are ready. Verify web readiness and signature freshness separately below. The Excel worker applies its own additional migrations when it starts.

`install-project-firewall.py` must succeed. It applies project ingress rules after Nginx/MinIO exist; Docker must expose the expected iptables chain. Reapply it after relevant container/firewall/host changes. This release does not install an automatic boot-time firewall restoration service.

## 8. Check startup before opening the panel

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

Use your configured hostname instead if appropriate. This procedure uses `HTTP_PORT=80` throughout. A custom external port also requires the reverse proxy to preserve that port in forwarded host information and origins; that setup is outside this guide.

## 9. Sign in and create the first application data

From an allowed LAN/VPN client, open the `/admin/` URL. Enter `SEED_ADMIN_EMAIL` and the generated `SEED_ADMIN_PASSWORD` from the private `.env.local` file. Change the bootstrap password after first sign-in and save the new password securely. The seed password then becomes historical; rerunning seed will not restore it.

Verify a simple real workflow: open the reference books, create a faculty, reload the page and confirm it remains. Enter/import your university's departments, teachers, subjects, groups, semesters and workload through the corresponding administrator pages. A fresh installation intentionally starts without that business data.

If CSS/JavaScript fail to load, inspect current asset URLs from a fresh page; both compiled assets and application code are already in the Rails image. Do not compile assets manually inside the running container.

## 10. Check antivirus separately before importing files

```bash
sudo ./deploy/bin/compose.sh logs --tail=100 clamav_signatures
sudo ./deploy/bin/compose.sh exec -T clamav_signatures \
  sh /opt/antivirus/check-signatures.sh
sudo ./deploy/bin/compose.sh exec -T api_geteway clamscan --version
sudo ./deploy/bin/compose.sh exec -T media_sanitizer clamscan --version
```

The freshness command must exit 0 for required scanning to proceed. The updater and API/sanitizer scanner binaries are separate; check their versions independently. The repair images do not upgrade the bundled scanner engine automatically.

Your previously reported CDN 403/429 block is not repaired by deleting images, changing project names, or reinstalling. If the official CDN remains inaccessible, retain scanning requirements and configure an actual trusted, maintained mirror/proxy. Do not repeatedly force downloads, remove cooldown state as a workaround, or increase the age threshold to hide stale signatures.

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

## 11. Confirm descriptors remain bounded

```bash
sudo ./deploy/bin/compose.sh exec -T schedule_web ruby \
  < deploy/bin/rails-fd-report.rb
```

Save a baseline after startup and compare after ten minutes, an hour and longer idle operation. The report finds current PIDs automatically. Counts may vary with live connections, but should settle rather than grow continuously with completed probes. Compare against the soft limit; increasing that limit alone does not fix a leak.

## 12. Normal stop and next startup

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

## Troubleshooting

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

For an existing installation with data to preserve, use [the upgrade runbook](SIMPLIFIED_DEPLOYMENT_2026-10-17.md), not new credentials/project volumes.

## Verification of this guide

Validated with published images and an isolated fresh project: no existing private configuration, new PostgreSQL/MinIO/antivirus volumes, a new Redis directory and generated credentials. Image pulls, dependency health, storage initialization, migrations, seed, database-version check, API/Rails readiness, Nginx validation, new administrator login and faculty creation/reload passed.

For test isolation only, container names and host ports differed from the production examples; the test handled redirected URLs explicitly for the alternate port. Application entrypoints, database initialization and image versions were unchanged. Existing application data and shared firewall rules were not modified by that test. The test project's synthetic data was removed afterward.

This does not claim a remote production deployment, complete workbook/notice-export acceptance or successful ClamAV CDN downloads. The externally imposed signature-download restriction remains subject to section 10.
