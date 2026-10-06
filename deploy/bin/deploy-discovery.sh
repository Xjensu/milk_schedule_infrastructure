#!/bin/sh
set -eu
cd "$(dirname "$0")/../.."
python3 deploy/bin/prepare-discovery.py
deploy/bin/compose.sh config --quiet
deploy/bin/compose.sh pull
# Infrastructure must be discoverable before Hanami can migrate the schema.
deploy/bin/compose.sh up -d --no-build db redis minio consul discovery_acl \
  postgres_registrar redis_registrar minio_registrar minio_init scheduler
deploy/bin/db.sh migrate
deploy/bin/compose.sh up -d --no-build
python3 deploy/bin/install-project-firewall.py
deploy/bin/compose.sh up -d --no-build --wait --wait-timeout 180
deploy/bin/compose.sh ps
