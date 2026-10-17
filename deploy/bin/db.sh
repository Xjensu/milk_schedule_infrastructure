#!/bin/sh
# Resolve the same database identity for Hanami CLI and the application.
set -eu
cd "$(dirname "$0")/../.."
case "${1:-}" in
  create|migrate|seed|version) ;;
  *) echo 'Usage: db.sh create|migrate|seed|version' >&2; exit 2 ;;
esac
[ "$#" -eq 1 ] || exit 2
exec deploy/bin/compose.sh run --rm --no-deps api_geteway \
  bundle exec hanami db "$1"
