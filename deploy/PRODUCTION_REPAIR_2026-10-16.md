> Superseded for the 2026-10-17 simplified release: use [the current deployment runbook](SIMPLIFIED_DEPLOYMENT_2026-10-17.md). The instructions below describe the older Consul deployment.

# Production repair and deployment — 2026-10-16

This is an update guide for the existing server, not a clean installation. Preserve the Compose project name, private configuration, discovery tokens and all application data. Never run `down -v`, prune volumes, regenerate secrets or reseed as part of this repair.

## 1. What failed and what this release changes

The production Rails worker had 1,022 open descriptors against a 1,024 soft limit; 1,015 were sockets. `/up` still returned 200, but `/readyz` reported Redis/API unavailable. Consul removed Rails from its passing instances, and Nginx correctly installed a disabled `rails_web` upstream. Restarting Rails restored readiness.

The gateway created a new Async HTTP pool for each short-lived gateway, including each readiness probe. It closed responses but not the owning pool. The corrective release closes both the response and pool on success, failure and cancellation. This trades some connection reuse for deterministic ownership. Do not replace it with a process-global client shared across Falcon forks/event loops.

Other changes:

- Readiness API calls have a two-second deadline; both Docker and Consul check `/readyz`. `/up` remains a separate liveness endpoint.
- Rails `nofile` soft/hard limits are 65,536. This is headroom, not the leak fix.
- Discovery address-detection sockets close even when address lookup/connect fails. Existing Consul HTTP checks and generated Consul addresses are retained.
- The API starts with `bundle exec puma -C config/puma.rb`, explicitly bound to `0.0.0.0:2300`.
- Rails explicitly serves precompiled public assets by default. Asset compilation already happens in the Docker build.
- ClamAV health checks inspect the daily database build date, not merely file existence. The default maximum age is three days. Shared writable-updater/read-only-scanner mounts are retained.
- The updater checks once an hour and retains FreshClam cooldown state. Fatal CDN refusals no longer cause a rapid Docker restart loop.
- The previously published Docker Hub MinIO mirror remains pinned; the broken original Quay default is not restored.
- `deploy/bin/rails-fd-report.rb` reports descriptor categories and socket states/remote ports without credentials or process arguments.

Docker does not automatically restart a running unhealthy container. Restart policies act on process exits. Do not add an unconditional restart loop based on Redis/API readiness failures.

## 2. Published components

Use the `codex/production-stability-2026-10-16` branch in these repositories:

| Component | Repository | Source |
| --- | --- | --- |
| Infrastructure and this guide | `git@github.com:Xjensu/milk_schedule_infrastructure.git` | branch above, based on `9cdb95d` |
| Rails | `git@github.com:Xjensu/milk_schedule_frontend.git` | commit `e729d8a` |
| API | `git@github.com:Xjensu/milk_schedule_api.git` | commit `9aba520` |

Rails is published on a new branch because the frontend repository's existing `main` contains the legacy frontend. Do not reset or replace that branch.

Only two new application images are required:

```dotenv
WEB_IMAGE=xjensu/table-bsut-by:2026-10-16-1
API_IMAGE=xjensu/table-api:2026-10-16-1
```

Keep the existing `IMAGE_TAG` for scheduler, Excel worker, discovery, storage initialization and ingress. Seven images have NOT been released under the new tag. All services using `API_IMAGE`, including workers and operations console, should be updated together. The release manifest in `deploy/image-releases/2026-10-16-1.json` records published image digests and validation results.

## 3. Record state and back up on the server

Run commands from your existing `milk_schedule_infrastructure` deployment directory. The examples use `sudo` for Docker; omit it only if your deployment account already has Docker access.

```bash
git status --short
git rev-parse HEAD
sudo ./deploy/bin/compose.sh ps -a
sudo ./deploy/bin/compose.sh images

for cid in $(sudo ./deploy/bin/compose.sh ps -q schedule_web api_geteway nginx); do
  sudo docker inspect --format \
    '{{.Name}} reference={{.Config.Image}} image_id={{.Image}}' "$cid"
done
```

Record the current infrastructure commit and explicit `WEB_IMAGE`/`API_IMAGE` values for rollback. Do not print whole environment files, expanded Compose configuration or complete Docker inspect output.

```bash
umask 077
mkdir -p backups
sudo ./deploy/bin/compose.sh exec -T db sh -c \
  'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' \
  > "backups/postgres-$(date +%Y%m%d-%H%M%S).dump"
```

Back up MinIO/storage and private credentials separately according to your normal backup procedure. Store backups outside the Git repository and verify restoration. A PostgreSQL dump alone is not a full application backup.

## 4. Update infrastructure safely

Confirm that `origin` points to `milk_schedule_infrastructure`. If it has another name, substitute that name below. For a `milk_proto` deployment, fetch and fast-forward to `codex/production-stability-workspace-2026-10-16` in that repository instead.

```bash
git remote -v
git fetch origin codex/production-stability-2026-10-16
git merge --ff-only origin/codex/production-stability-2026-10-16
```

If fast-forward is refused, review the server's local commits and configuration. Do not use `reset --hard`. Preserve custom ingress, firewall and outer reverse-proxy changes. This application update does not require replacing your running Nginx image.

Edit the existing `.env.local`:

```dotenv
WEB_IMAGE=xjensu/table-bsut-by:2026-10-16-1
API_IMAGE=xjensu/table-api:2026-10-16-1
CLAMAV_MAX_SIGNATURE_AGE_SECONDS=259200
```

Do not replace the file with `.env.example`. Keep all secrets, `IMAGE_TAG`, `COMPOSE_PROJECT_NAME`, Redis/database settings and working MinIO override. Existing explicit image overrides take precedence over `IMAGE_TAG`.

```bash
python3 deploy/bin/prepare-discovery.py
sudo ./deploy/bin/compose.sh config --quiet
sudo ./deploy/bin/compose.sh pull schedule_web api_geteway \
  outbox_relay media_sanitizer notice_export_worker \
  schedule_generation_worker ops_console clamav_signatures
```

Preflight must detect the actual server interface/subnet. Review a reported network change before continuing. Refreshing generated addresses may require reconciling dependencies too; the bounded update below assumes the existing database, Redis, MinIO and Consul networking still matches the generated configuration.

## 5. Verify antivirus freshness before replacing the application

```bash
sudo ./deploy/bin/compose.sh up -d --no-build --no-deps clamav_signatures
sudo ./deploy/bin/compose.sh logs --tail=100 clamav_signatures
sudo ./deploy/bin/compose.sh exec -T clamav_signatures \
  sh /opt/antivirus/check-signatures.sh
```

The final command must exit 0. A populated but stale database now fails health checks deliberately. Allow FreshClam time to download/update the shared database. Its initial synchronization can take several minutes.

If it remains unhealthy, check updater logs for DNS, outbound connectivity, proxy errors, permission errors, unsupported engine versions, CDN denial or rate limits. Honor upstream retry/cooldown instructions. Do not repeatedly run another FreshClam process against the same database or disable required scanning to make deployment pass.

The updater writes `/signatures`; API and sanitizer read the same volume at `/var/lib/clamav`. Confirm this using mount-only inspection if necessary:

```bash
for cid in $(sudo ./deploy/bin/compose.sh ps -q \
  clamav_signatures api_geteway media_sanitizer); do
  sudo docker inspect --format \
    '{{.Name}} {{range .Mounts}}{{.Destination}} <- {{.Source}} writable={{.RW}}; {{end}}' "$cid"
done
```

Freshness failure is an operational blocker requiring correction, not proof that the application image is broken. Already running API containers are not automatically stopped merely because the updater becomes unhealthy; monitor freshness independently.

Local verification on October 16 reproduced a CDN 403 and a cooldown through October 17. The stale seed database was correctly rejected. Publishing this release does not resolve a server's CDN access restrictions. Check the exact cooldown and error on YOUR server; do not assume its network has the same block.

If the server cannot use the official CDN after the cooldown, use an organization-approved, maintained private mirror or HTTP proxy. ClamAV documents FreshClam and cvdupdate as supported download methods; repeatedly scraping database URLs with curl is not a replacement. A private mirror must itself obtain fresh official databases successfully.

For an existing trusted mirror, an optional configuration overlay is supplied:

```bash
umask 077
cp deploy/antivirus/freshclam.conf.example deploy/antivirus/freshclam.conf
nano deploy/antivirus/freshclam.conf
```

Replace the placeholder `DatabaseMirror` with the actual mirror URL. Configure authentication/proxy settings privately if required. Then load the overlay for EVERY subsequent Compose invocation that creates or updates the updater:

```bash
sudo ./deploy/bin/compose.sh -f deploy/antivirus/compose.mirror.yml config --quiet
sudo ./deploy/bin/compose.sh -f deploy/antivirus/compose.mirror.yml \
  up -d --no-build --no-deps clamav_signatures
```

For the application deployment in section 6, likewise insert `-f deploy/antivirus/compose.mirror.yml` before `up` when using this option. The wrapper already loads the base Compose file. The private `freshclam.conf` is ignored by Git. Do not delete FreshClam cooldown files as a workaround for a CDN block. See [ClamAV private mirror instructions](https://docs.clamav.net/appendix/CvdPrivateMirror.html).

## 6. Recreate the corrected application services

Schedule a maintenance window. Ordinary Compose recreation is not a guaranteed zero-downtime rolling deployment.

```bash
sudo ./deploy/bin/compose.sh up -d --no-build --no-deps \
  --wait --wait-timeout 180 \
  api_geteway schedule_web outbox_relay media_sanitizer \
  notice_export_worker schedule_generation_worker ops_console

sudo python3 deploy/bin/install-project-firewall.py
sudo ./deploy/bin/compose.sh ps -a
sudo ./deploy/bin/compose.sh images
```

This release contains no database schema changes. No migration, seed, database creation or volume deletion is required. Do not change signing keys or administrator passwords during this deployment.

Recreation is required to apply the image, health check and `ulimits` changes. A simple `restart` does not apply them. Ruby discovery files are mounted from infrastructure, so the corrected discovery code also requires process restart/recreation.

## 7. Verify readiness, production startup and routing

```bash
sudo ./deploy/bin/compose.sh exec -T --index 1 schedule_web \
  curl -fsS --max-time 10 http://127.0.0.1:3000/readyz
sudo ./deploy/bin/compose.sh exec -T --index 2 schedule_web \
  curl -fsS --max-time 10 http://127.0.0.1:3000/readyz
sudo ./deploy/bin/compose.sh exec -T api_geteway \
  curl -fsS --max-time 10 http://127.0.0.1:2300/readyz
sudo ./deploy/bin/compose.sh exec -T nginx cat /run/nginx/upstreams.conf
sudo ./deploy/bin/compose.sh logs --since=10m --tail=100 api_geteway schedule_web
```

Adjust replica indices to the configured count. Expect Rails readiness 200 with `redis: true` and `api: true`; Nginx should list real Rails addresses. The API should boot Puma directly without the Hanami reloader warning. Registration/routing updates can take several probe intervals.

Never manually replace `/run/nginx/upstreams.conf`: it is generated and supervised. Do not bypass readiness to conceal dependency failures.

## 8. Monitor descriptors and prove the fix under traffic

```bash
sudo ./deploy/bin/compose.sh exec -T --index 1 schedule_web ruby \
  < deploy/bin/rails-fd-report.rb
sudo ./deploy/bin/compose.sh exec -T --index 2 schedule_web ruby \
  < deploy/bin/rails-fd-report.rb
```

The report finds current worker PIDs automatically. Old PIDs disappear after restart. Capture a baseline after warm-up, then compare after 10 minutes, an hour, a day and beyond the previous four-day failure window. Monitor each worker, not just PID 1.

Success means descriptor counts remain bounded under comparable load and return toward baseline after bursts. A larger limit merely delays recurrence if counts continue climbing. Alert on sustained growth, descriptor utilization, readiness failure, missing passing Consul instances and website 503s.

On a host with `nsenter` and `ss`, capture connection details before another restart if counts grow:

```bash
for cid in $(sudo ./deploy/bin/compose.sh ps -q schedule_web); do
  host_pid=$(sudo docker inspect --format '{{.State.Pid}}' "$cid")
  echo "Container: $cid"
  sudo nsenter -t "$host_pid" -n ss -tanp
  sudo nsenter -t "$host_pid" -n ss -uanp
done
```

Large populations targeting API port 2300 implicate outbound API lifecycle; Consul 8500 implicates discovery HTTP; Redis 6379 implicates cache clients. Local server port 3000 and connection states help distinguish accepted connections. These are investigation clues, not automatic attribution.

## 9. Verify static assets and actual user workflows

Both Rails replicas must use the same published image digest and compiled asset manifest:

```bash
sudo ./deploy/bin/compose.sh exec -T --index 1 schedule_web \
  ls -la public/assets
sudo ./deploy/bin/compose.sh exec -T --index 2 schedule_web \
  ls -la public/assets
```

Open a fresh public page, inspect the asset URLs it currently references, and request those exact URLs. Expect CSS/JavaScript responses with status 200 and correct content types. Do not assume old fingerprinted URLs from historical logs belong to the current release. If necessary compare `.manifest.json` between replicas and inspect outer-proxy HTML caching.

Retain assets referenced by cached HTML across future release transitions, or serve versioned assets from an appropriate store. Do not delete all assets as a troubleshooting shortcut.

Then verify administrator login, create/edit/reload of a disposable record, one supported Excel import, processing history and notice download. Check upload history before retrying after a timeout: a failed response does not prove the upload was never committed. Test antivirus rejection using an approved EICAR fixture in staging, not a production user document. Verify updater freshness from both scanner containers:

```bash
sudo ./deploy/bin/compose.sh exec -T api_geteway clamscan --version
sudo ./deploy/bin/compose.sh exec -T media_sanitizer clamscan --version
```

## 10. Rollback and limits of acceptance

If the corrected images fail acceptance, restore the recorded previous `WEB_IMAGE` and `API_IMAGE` values and recreate the same application service set. Keep credentials and volumes intact. If rolling back infrastructure too, review and restore the recorded revision without discarding private or custom server changes. This release has no database migration to undo.

The socket fix requires failure-path verification and observation beyond the previous incident window before calling the incident permanently resolved. No remote production deployment or multi-day production soak is implied by publishing this release.

See the release manifest for the precise checks actually completed. The local workspace's application services are returned to their previously stopped state after verification.

## References

- [Async HTTP connection and pool lifecycle](https://socketry.github.io/async-http/guides/concurrent-requests/index.html)
- [Docker Compose service configuration](https://docs.docker.com/reference/compose-file/services/)
- [ClamAV signature updates](https://docs.clamav.net/manual/Usage/SignatureManagement.html)
- [Rails asset pipeline](https://guides.rubyonrails.org/v8.1/asset_pipeline.html)
