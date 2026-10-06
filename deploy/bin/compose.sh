#!/bin/sh
# Server settings live in .env.local; retain .env as an optional legacy fallback.
set -eu
cd "$(dirname "$0")/../.."
if [ -f .env ]; then
  exec docker compose --env-file .env --env-file .env.local \
    --env-file deploy/generated/compose.env -f docker-compose.yml "$@"
fi
exec docker compose --env-file .env.local --env-file deploy/generated/compose.env \
  -f docker-compose.yml "$@"
