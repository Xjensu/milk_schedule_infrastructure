# Deploy from GitHub using Docker Hub images

The development PC builds and publishes images. The separate Linux server clones the main GitHub repository, reads `.env.local`, pulls those images and runs the application. No image builds run on the server, and no host IP entry is required.

MinIO uses a pinned `linux/amd64` mirror in `xjensu/table-minio`; its original Quay reference rejects unauthenticated pulls. The mirror contains the same MinIO image used by this release. `MINIO_IMAGE` can override the reference in `.env.local`.

The archive packaging script is optional. The standard procedure below uses a Git checkout of the main repository.

For detailed image publishing instructions, see [DOCKERHUB_GUIDE.md](DOCKERHUB_GUIDE.md).

## 1. Publish the release from the development PC

Run these commands on the development PC in the complete source workspace:

```bash
cd /home/xjensu/Desktop/milk_schedule
[ -f .env ] || cp .env.compose.example .env
docker login --username xjensu
./deploy/bin/build-images.sh 2026-10-06-1 --push
```

Use a new tag for each release. The build file reads `.env` on the development PC for registry settings; the script supplies the requested image tag. It builds and pushes these seven images:

| Image | Used by |
| --- | --- |
| `xjensu/table-bsut-by:2026-10-06-1` | Rails web interface |
| `xjensu/table-api:2026-10-06-1` | Hanami API, operations console and API workers |
| `xjensu/excel-processor:2026-10-06-1` | Excel processing |
| `xjensu/table-scheduler:2026-10-06-1` | Scheduling solver |
| `xjensu/table-discovery:2026-10-06-1` | Service registrars and ACL initialization |
| `xjensu/table-minio-init:2026-10-06-1` | Storage initialization |
| `xjensu/table-edge:2026-10-06-1` | Nginx ingress |

Create these repositories in your Docker Hub account and choose their visibility before pushing. Enter the Docker Hub token interactively at login. Build for the server's CPU architecture; an amd64 server needs amd64 images. ARM compatibility of the pinned dependencies has not been verified.

Publish infrastructure changes from a checkout of this infrastructure repository on its `main` branch:

```bash
git push origin main
```

This publishes the infrastructure release to the infrastructure repository's main branch. The server must use its compatible published revision. Application directories under `apps/` have independent Git state; their compatible sources are required on the build PC, while the server uses their published images. Commit application source changes in their owning repositories when preparing a reproducible release.

Do not change sources or deployment configuration between building the images and identifying the matching Git revision. The build commands do not start or restart the development application.

## 2. Clone the main repository on the server

Install Git, Docker Engine with the Compose plugin, Python 3 and `iproute2` on the Linux server. The deployment account needs Docker access. The firewall helper requires Docker's iptables backend and a `DOCKER-USER` chain; iptables-nft is supported.

Connect to the server through SSH. Create a persistent directory, substituting your actual deployment account for `deploy`:

```bash
sudo install -d -m 750 -o deploy -g deploy /opt/milk-schedule
```

As that deployment account, clone the branch containing the release's deployment changes. Replace `DEPLOYMENT_BRANCH` with the branch published in step 1:

```bash
git clone --branch main \
  git@github.com:Xjensu/milk_schedule_infrastructure.git /opt/milk-schedule
cd /opt/milk-schedule
```

For a fixed release, check out its published commit or tag. GitHub SSH access is required for this clone URL; HTTPS cloning is also available for authorized users. The repository contains the server Compose file and its support files. You do not need to clone the nested application source repositories on the server.

For private Docker Hub images, log in on the server using a token with pull access:

```bash
docker login --username xjensu
```

Your router can keep forwarding incoming website traffic to this server on port 80. Nginx listens on all server interfaces. SSH/DNS/router configuration does not need to be copied into `.env.local`.

## 3. Generate and edit server configuration

On the server, run:

```bash
python3 deploy/bin/init-env.py
nano .env.local
```

The initializer creates `.env.local` with random secrets and private permissions. It also creates separate operations-console and optional monitoring credential files. Existing files are never overwritten. It does not create a server `.env` file.

Choose the published image tag in `.env.local`:

```dotenv
COMPOSE_PROJECT_NAME=milk_schedule
IMAGE_NAMESPACE=xjensu
IMAGE_TAG=2026-10-06-1
HTTP_BIND_IP=0.0.0.0
HTTP_PORT=80
WEB_REPLICAS=2
ADMIN_INTERFACE=
ADMIN_LAN_CIDRS=
```

Leave the network overrides blank for the normal LAN/router setup. Deployment detects the server's private address and subnet, preferring its normal outbound route when multiple private interfaces exist. `HTTP_BIND_IP=0.0.0.0` means all interfaces; it is not the machine's actual address. No `LAN_BIND_IP` entry is needed.

Review these runtime settings in the same file:

| Settings | What to configure |
| --- | --- |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | Database name and credentials. The initializer generates a password. |
| `DATABASE_URL` | Must agree with the PostgreSQL settings. The template derives it automatically. |
| `REDIS_PASSWORD`, `REDIS_URL` | Matching Redis authentication settings. |
| `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY` | Storage credentials. The template derives matching MinIO root credentials. |
| `JWT_SECRET`, `SECRET_KEY_BASE` | Generated signing keys; retain them across upgrades. |
| `SEED_ADMIN_EMAIL`, `SEED_ADMIN_PASSWORD` | Initial application administrator. Set the desired email; a password is generated. |
| `CORS_ORIGINS` | Actual browser origin, e.g. `http://your-website.example`, without a trailing slash. |
| `ASSUME_SSL`, `FORCE_SSL` | Keep false for the current HTTP ingress. These settings do not configure HTTPS. |

Keep internal hostnames `db`, `redis` and `minio`; do not put the server IP or `localhost` in container connection settings. Consul discovers internal endpoints.

The template expands `${VARIABLE}` references. Generated passwords are hexadecimal and safe in connection URLs. Existing passwords with URL-reserved characters require URL-encoded credentials in `DATABASE_URL` and `REDIS_URL`. Single-quote literal dotenv values containing `$` when interpolation is unwanted.

Edit `deploy/ops/.env.local` if you want a different operations-console username/password. Its account is separate from the application administrator. Optional Grafana credentials are in `deploy/observability/.env.local`.

Teachers, groups, subjects and workload are application data, not environment settings. Enter or import them after the database and administrator are ready.

## 4. Pull images and start infrastructure

The following commands run only on the deployment server:

```bash
cd /opt/milk-schedule
python3 deploy/bin/prepare-discovery.py
./deploy/bin/compose.sh config --quiet
./deploy/bin/compose.sh pull
./deploy/bin/compose.sh up -d --no-build \
  db redis minio consul discovery_acl \
  postgres_registrar redis_registrar minio_registrar minio_init scheduler
```

Preflight writes host-specific settings and private discovery credentials to ignored `deploy/generated/`. The Compose wrapper loads `.env.local` and those generated settings. An existing `.env` is supported as a legacy fallback, but `.env.local` takes precedence for server settings.

All runtime services use `image:` references. Pulling or starting this configuration does not build images, and no `apps/` directory is needed.

Use `config --quiet` rather than plain `config` to avoid displaying expanded secrets.

## 5. Initialize the database through Hanami

The PostgreSQL image creates the database named by `POSTGRES_DB` when its data volume is first initialized. Normally, you therefore run Hanami migrations and seeds directly:

```bash
./deploy/bin/db.sh migrate
./deploy/bin/db.sh seed
./deploy/bin/db.sh version
```

`db.sh` runs a temporary container from the published API image and resolves the database URL through Consul before executing the Hanami command. The API web server does not need to be running for these commands.

If the configured database does not exist, Hanami database creation is available:

```bash
./deploy/bin/db.sh create
./deploy/bin/db.sh migrate
./deploy/bin/db.sh seed
```

Do not run `create` as a required step when PostgreSQL has already created the database. `migrate` creates/updates tables. `seed` loads reference data and creates the initial administrator using the server's configured credentials; it does not reset an existing administrator's password. Hanami `db prepare` also runs seeds, so use `migrate` for routine updates.

The Excel worker applies its own migrations on startup.

## 6. Start the application

After migrations and initial seeding:

```bash
./deploy/bin/compose.sh up -d --no-build
python3 deploy/bin/install-project-firewall.py
./deploy/bin/compose.sh up -d --no-build --wait --wait-timeout 180
./deploy/bin/compose.sh ps
./deploy/bin/compose.sh images
```

Open the website through the hostname/router you already use. From an allowed LAN client, open `/admin/` and sign in with `SEED_ADMIN_EMAIL` and `SEED_ADMIN_PASSWORD`. Change the bootstrap password after first sign-in, then add/import teachers and other schedule data.

The `/ops/` console uses its own credentials and exposes allowlisted Hanami database operations. You can manage later migrations there or through `db.sh` over SSH. It has no arbitrary shell or Docker socket.

Public pages are reachable through router forwarding. Administrator/login routes and `/ops/` remain LAN-restricted by default. Use the LAN or a deliberately configured VPN for administration. The current ingress is HTTP and does not encrypt credentials.

### Sign in through localhost on the Docker host

Public pages work at `http://localhost`, but local login can return **403** with the default LAN policy. Docker presents host requests to Nginx as the Docker bridge gateway, which is outside the detected LAN subnet. This is an ingress denial before the application checks the password.

You can sign in through the automatically detected LAN address instead. To print it without reading secrets:

```bash
python3 -c 'import json; print("http://" + json.load(open("deploy/generated/network.json"))["address"] + "/admin/")'
```

If you need login at `http://localhost`, run this after starting the application, from the deployment directory. It detects the edge network gateway and adds only that host address (`/32`) to the existing administrator allowlist in the private `.env.local`. No machine IP needs to be entered manually.

```bash
python3 - <<'PYCODE'
import json
import re
import subprocess
from pathlib import Path

container_id = subprocess.check_output(
    ["./deploy/bin/compose.sh", "ps", "-q", "nginx"], text=True
).strip()
if not container_id:
    raise SystemExit("Start Nginx before configuring localhost access.")
container = json.loads(subprocess.check_output(
    ["docker", "inspect", container_id], text=True
))[0]
gateways = {
    network["Gateway"]
    for name, network in container["NetworkSettings"]["Networks"].items()
    if name.endswith("_edge") and network["Gateway"]
}
if len(gateways) != 1:
    raise SystemExit("Could not identify a unique edge network gateway.")
cidrs = json.loads(Path("deploy/generated/network.json").read_text())["cidrs"]
cidrs = list(dict.fromkeys([*cidrs, next(iter(gateways)) + "/32"]))
env_path = Path(".env.local")
settings = env_path.read_text()
if not re.search(r"^ADMIN_LAN_CIDRS=", settings, re.M):
    raise SystemExit("Add the ADMIN_LAN_CIDRS setting from .env.example first.")
settings = re.sub(
    r"^ADMIN_LAN_CIDRS=.*$",
    "ADMIN_LAN_CIDRS=" + ",".join(cidrs),
    settings,
    flags=re.M,
)
env_path.write_text(settings)
print("Configured localhost access; credentials were not printed.")
PYCODE
python3 deploy/bin/prepare-discovery.py
./deploy/bin/compose.sh exec -T nginx nginx -t
./deploy/bin/compose.sh exec -T nginx nginx -s reload
```

Allow a moment for Nginx to reload, refresh `http://localhost`, and sign in using `SEED_ADMIN_EMAIL` and `SEED_ADMIN_PASSWORD` from `.env.local`. A fresh deployment generates a new administrator password; credentials from another deployment will not match. Updating the seed password does not reset an existing account.

This is an optional host-access exception, not a requirement for remote LAN deployment. It also permits that host gateway to reach the other LAN-restricted routes. Do not allow the entire Docker subnet or `0.0.0.0/0`. If the edge network is recreated with a different gateway, remove the old gateway `/32` from `ADMIN_LAN_CIDRS` and repeat these steps. To restore LAN-only access, leave `ADMIN_LAN_CIDRS` blank and rerun preflight and the Nginx reload.

Notice download links currently target MinIO on the detected private address at port 9000. Forwarding website port 80 alone does not make that private storage endpoint reachable from external clients. LAN/VPN downloads can use the default; external downloads require an appropriately secured storage endpoint and `NOTICE_EXPORT_PUBLIC_ENDPOINT` configuration.

Verify schedules, administrator sign-in, an edit/reload, Excel import and notice download. Container health checks do not prove these complete workflows.

## 7. Shorter automatic startup option

If you prefer the supplied automation after configuration:

```bash
./deploy/bin/deploy-discovery.sh
./deploy/bin/db.sh seed
```

The deployment script performs detection, pull, infrastructure startup, migrations, application startup, firewall installation and health waits. It does not seed automatically. Use the manual steps above when you want to control when migrations run.

## 8. Deploy an update

On the development PC, build/push a new image tag and publish its compatible main repository revision to GitHub.

On the server, back up first, then update the checked-out deployment branch:

```bash
cd /opt/milk-schedule
git pull --ff-only
nano .env.local
```

Set `IMAGE_TAG` to the newly published tag. Compare the new `.env.example` with your existing `.env.local` and add new settings deliberately. Git does not replace the ignored private file. Keep the project name and existing secrets unchanged.

Then deploy with the wrapper, which includes migrations:

```bash
./deploy/bin/deploy-discovery.sh
```

Alternatively, repeat the manual pull/infrastructure/migration/start steps. Routine updates do not require another seed. Review schema changes and back up before migrations; an image rollback does not undo database migrations.

## 9. Change environment settings without rebuilding

On the server:

```bash
nano .env.local
./deploy/bin/compose.sh config --quiet
./deploy/bin/compose.sh up -d --no-build
python3 deploy/bin/install-project-firewall.py
```

Compose recreates containers whose environment changed. A restart alone does not apply edited environment values. Clear stale shell overrides such as `IMAGE_TAG` when file values should be used.

After a server address/subnet change, refresh automatic detection:

```bash
python3 deploy/bin/prepare-discovery.py
./deploy/bin/compose.sh up -d --no-build
./deploy/bin/compose.sh exec -T nginx nginx -t
./deploy/bin/compose.sh exec -T nginx nginx -s reload
python3 deploy/bin/install-project-firewall.py
```

No IP edit is needed in `.env.local`. Detection runs at deployment/preflight, not continuously. The router's forwarding rule must still target the server's current address.

Changing `POSTGRES_PASSWORD` in a file does not change the stored PostgreSQL role password; rotate the database credential and clients together. Changing signing keys invalidates authentication/session data. Grafana stores its initialized administrator password in its own database and needs its own password rotation procedure.

## 10. Backups and diagnostics

Preserve PostgreSQL, MinIO objects, Redis files, Consul data/tokens and optional monitoring volumes. Back up the private environment files and `deploy/generated/` securely. Do not copy another machine's generated networking to a new server. Never use `down -v` or volume pruning during routine updates.

Example PostgreSQL logical backup on the server:

```bash
umask 077
mkdir -p backups
./deploy/bin/compose.sh exec -T db sh -c \
  'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' \
  > "backups/postgres-$(date +%Y%m%d-%H%M%S).dump"
```

This backs up PostgreSQL only. Back up other state separately and verify restoration. To stop services while preserving data, use `./deploy/bin/compose.sh stop`.

Useful server diagnostics:

```bash
./deploy/bin/compose.sh ps -a
./deploy/bin/compose.sh logs --tail=100 api_geteway
./deploy/bin/compose.sh logs --tail=100 discovery_acl
./deploy/bin/compose.sh logs --tail=100 excel_processor
./deploy/bin/db.sh version
./deploy/bin/compose.sh exec -T nginx nginx -t
```

| Problem | Check |
| --- | --- |
| Image missing / pull denied | All seven images were published with the chosen tag; registry access is correct. |
| `exec format error` | Images match the server architecture. |
| Missing runtime mount | The compatible main repository revision was cloned, including `deploy/` and `schemas/`, and preflight ran. |
| IP detection fails | Host private IPv4/default route; optional `ADMIN_INTERFACE` for unusual routing. |
| Login, `/admin/` or `/ops/` returns 403 | Client must be on the detected LAN or configured administrator network. For host localhost access, follow the section above. |
| `/ops/` returns 401 | Its separate credentials and container recreation after changes. |
| Env edit has no effect | Recreate containers; check shell overrides. |
| Firewall helper fails | Docker iptables backend and `DOCKER-USER` chain. |

For optional monitoring, see [observability/README.md](observability/README.md). Build/push Fluentd on the development PC for the chosen tag before enabling the server overlay.

Deployment does not configure router rules, DNS, TLS certificates or automatic firewall restoration after host restarts. Reapply `install-project-firewall.py` after host/firewall restarts or container replacement.
