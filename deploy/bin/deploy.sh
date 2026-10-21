#!/bin/sh
set -eu
cd "$(dirname "$0")/../.."
python3 deploy/bin/prepare-discovery.py
deploy/bin/compose.sh config --quiet
deploy/bin/compose.sh pull
python3 deploy/bin/retire-discovery.py
# Bring persistent dependencies up before migrations; no service registry required.
deploy/bin/compose.sh up -d --no-build --wait --wait-timeout 120 db redis minio scheduler
deploy/bin/compose.sh up -d --no-build minio_init
deploy/bin/db.sh migrate
# New Rails workload catalog requires the matching API before web recreation.
deploy/bin/compose.sh up -d --no-build --no-deps --wait --wait-timeout 180 api_geteway
deploy/bin/compose.sh up -d --no-build
python3 deploy/bin/install-project-firewall.py
python3 deploy/bin/install-recovery.py
python3 deploy/bin/install-signature-refresh.py
# Signature freshness is reported separately: CDN outages must not block page availability.
for service in api_geteway schedule_web; do
  case "$service" in api_geteway) port=2300 ;; schedule_web) port=3000 ;; esac
  container_ids=$(deploy/bin/compose.sh ps -q "$service")
  if [ -z "$container_ids" ]; then
    echo "$service has no running containers." >&2
    exit 1
  fi
  for container_id in $container_ids; do
    attempt=0
    until docker exec "$container_id" curl -fsS --max-time 3 \
        "http://127.0.0.1:$port/readyz" >/dev/null 2>&1; do
      attempt=$((attempt + 1))
      if [ "$attempt" -ge 45 ]; then
        echo "$service container $container_id readiness failed; inspect service logs." >&2
        exit 1
      fi
      sleep 2
    done
  done
done
deploy/bin/compose.sh exec -T nginx nginx -t
if ! deploy/bin/compose.sh exec -T clamav_signatures \
    sh /opt/antivirus/check-signatures.sh; then
  echo 'WARNING: antivirus signatures unavailable/stale; scanning flows must fail closed.' >&2
fi
deploy/bin/compose.sh ps
