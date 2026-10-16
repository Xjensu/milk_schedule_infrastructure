#!/bin/sh
set -eu
# Seed a new volume from the official image, including detached signatures.
for source in /var/lib/clamav/*.cvd /var/lib/clamav/*.cvd.sign; do
  [ -f "$source" ] || continue
  target="/signatures/$(basename "$source")"
  [ -f "$target" ] || cp "$source" "$target"
done
chown -R clamav:clamav /signatures
# A fatal CDN refusal exits daemon mode. Do not let Docker turn that into a
# rapid restart loop. One check per hour also respects FreshClam's own cooldown.
child=
trap 'if [ -n "$child" ]; then kill "$child" 2>/dev/null || true; wait "$child" 2>/dev/null || true; fi; exit 0' TERM INT
while :; do
  freshclam --datadir=/signatures --stdout &
  child=$!
  if ! wait "$child"; then
    echo 'Signature update failed; retaining existing databases and retrying in one hour.' >&2
  fi
  sleep 3600 &
  child=$!
  wait "$child" || true
done
