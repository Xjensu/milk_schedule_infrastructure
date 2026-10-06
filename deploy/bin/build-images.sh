#!/bin/sh
set -eu
cd "$(dirname "$0")/../.."
IMAGE_TAG=${1:?Usage: build-images.sh TAG [--push]}
export IMAGE_TAG
case "$IMAGE_TAG" in *[!a-zA-Z0-9_.-]*|[-.]*|'') echo 'Invalid image tag' >&2; exit 2;; esac
case "${2:-}" in ''|--push) ;; *) echo 'Expected --push or no second argument' >&2; exit 2;; esac
[ "$#" -le 2 ] || exit 2
# Explicit file: no application secrets or host-generated network data required.
docker compose --env-file .env -f compose.build.yml config --quiet
docker compose --env-file .env -f compose.build.yml build --pull
if [ "${2:-}" = --push ]; then
  docker compose --env-file .env -f compose.build.yml push
fi
