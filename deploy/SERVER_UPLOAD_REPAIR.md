# Fix “Upload service temporarily unavailable” on the server

Run these commands on the deployment server, from the existing `milk_schedule_infrastructure` checkout. This procedure addresses uploads blocked by stale ClamAV signature databases when the official CDN returns HTTP 403/429.

Keep the existing `.env.local`, credentials, project name, database, object storage and Redis data. No application image rebuild, migration or seed is needed for this repair.

## 1. Download the fix

```bash
git fetch origin
git switch main
git pull --ff-only origin main
test -f deploy/bin/refresh-signatures.py
test -f deploy/bin/install-signature-refresh.py
```

The branch must include commit `463214a` or a later commit. If Git reports tracked local changes or divergent history, resolve them deliberately; do not use `reset --hard`.

## 2. Recreate only the signature updater

```bash
sudo ./deploy/bin/compose.sh config --quiet
sudo ./deploy/bin/compose.sh up -d --no-build --no-deps clamav_signatures
```

Do not run plain `compose config` in shared logs: it expands private settings. Application services should already be running; this command updates only the signature updater.

## 3. Refresh and verify the antivirus databases

```bash
sudo python3 deploy/bin/refresh-signatures.py
```

Expected final output:

```text
Signature freshness: PASS; existing API/scanners use the shared volume immediately.
```

The helper downloads signed databases from the Microsoft-hosted HTTPS mirror, verifies their embedded ClamAV signatures and atomically installs only newer versions. The official ClamAV image supplies the verifier and bootstrap fallback. Freshness is checked using the actual database build date; downloading a file does not automatically make it acceptable.

The helper preserves FreshClam cooldown state and the existing three-day freshness limit. If this command fails, inspect its error before proceeding. Do not disable scanning, change database timestamps or increase the allowed age to hide the failure.

The server needs outbound HTTPS access to the configured mirror and Docker Hub. Settings default to:

```dotenv
CLAMAV_DATABASE_MIRROR=https://packages.microsoft.com/clamav
CLAMAV_SEED_IMAGE=clamav/clamav:1.5
```

They are optional overrides in `.env.local`; the current Compose file supplies these defaults. Keep any deliberately configured, working mirror. If changing these values, repeat step 2 before refreshing. The helper uses host Docker access and does not send uploaded user files or application credentials to the mirror.

## 4. Enable automatic refresh

On a systemd Linux server:

```bash
sudo python3 deploy/bin/install-signature-refresh.py
```

Refreshes run every six hours. Determine this checkout's timer name automatically:

```bash
signature_unit=$(python3 - <<'PY'
from pathlib import Path
import hashlib
root = Path.cwd().resolve()
print('milk-signatures-' + hashlib.sha256(str(root).encode()).hexdigest()[:12])
PY
)
sudo systemctl is-enabled "$signature_unit.timer"
sudo systemctl is-active "$signature_unit.timer"
```

Expected results: `enabled` and `active`. Run these commands from the same checkout used for installation. The service is a one-shot task and can be inactive between executions while the timer remains active.

Inspect its operational logs:

```bash
sudo journalctl -u "$signature_unit.service" --since=1h --no-pager -n 50
```

The first scheduled run can wait up to two minutes. Step 3 already performs an immediate refresh. If a future refresh fails, inspect the journal; scanning continues to reject files once signatures become stale.

## 5. Check scanner readiness

```bash
sudo ./deploy/bin/compose.sh exec -T clamav_signatures \
  sh /opt/antivirus/check-signatures.sh
sudo ./deploy/bin/compose.sh exec -T api_geteway clamscan --version
sudo ./deploy/bin/compose.sh ps
```

The freshness command must exit successfully; it may print nothing on success. The scanner version should show a recent database date. The API and media scanners read the shared volume immediately, so an API restart is unnecessary.

## 6. Retry the workbook upload

Refresh `/admin/excel_imports`, upload the workbook and confirm it appears in upload history. Then check its processing result: successful upload does not prove that the workbook matches the university's expected import format.

The original CDN may continue logging HTTP 403 while required scanning works with fresh, verified mirror data. Do not erase cooldown files, delete volumes or set `MEDIA_REQUIRE_VIRUS_SCAN=false`.

If the same message persists, collect recent logs without sharing credentials or private environment files:

```bash
sudo ./deploy/bin/compose.sh logs --since=10m --tail=100 \
  schedule_web api_geteway excel_processor clamav_signatures
sudo journalctl -u "$signature_unit.service" --since=1h --no-pager -n 50
```

## Optional workstation installation without sudo

If the deployment account has Docker access and a working user systemd manager:

```bash
python3 deploy/bin/refresh-signatures.py
python3 deploy/bin/install-signature-refresh.py --user
systemctl --user is-enabled "$signature_unit.timer"
systemctl --user is-active "$signature_unit.timer"
```

Use the same timer-name calculation from step 4. To keep user timers running after logout/reboot, enable lingering with `loginctl enable-linger` if local policy permits. Do not install both system and user copies. Before moving/deleting the checkout, remove the matching installation with `install-signature-refresh.py --remove`, adding `--user` for a user installation.

## Verification

The local repair was verified with current signed databases, clean-file acceptance, EICAR rejection, an administrator workbook upload returning HTTP 201, persisted upload history and a successful scheduled refresh. The synthetic workbook was removed without importing schedule data. This file documents server deployment of that repair; it does not claim the remote server has already been updated.

For the complete deployment procedure, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).
