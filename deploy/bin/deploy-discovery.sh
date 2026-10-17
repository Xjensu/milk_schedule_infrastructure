#!/bin/sh
# Compatibility entrypoint for existing operators.
set -eu
exec "$(dirname "$0")/deploy.sh" "$@"
