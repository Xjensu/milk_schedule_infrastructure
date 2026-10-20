#!/bin/sh
set -eu
# Official non-base ClamAV images contain signed databases. Replace stale seeds
# only with a verified newer version, never by touching their timestamps.
for source in /var/lib/clamav/*.cvd; do
  [ -f "$source" ] || continue
  info=$(sigtool --info "$source") || exit 1
  version=$(printf '%s\n' "$info" | sed -n 's/^Version: *//p')
  case "$version" in ''|*[!0-9]*) exit 1 ;; esac
  base=$(basename "$source" .cvd)
  current=0
  for existing in "/signatures/$base.cvd" "/signatures/$base.cld"; do
    [ -s "$existing" ] || continue
    existing_info=$(sigtool --info "$existing" 2>/dev/null) || continue
    existing_version=$(printf '%s\n' "$existing_info" | sed -n 's/^Version: *//p')
    case "$existing_version" in ''|*[!0-9]*) continue ;; esac
    [ "$existing_version" -le "$current" ] || current=$existing_version
  done
  if [ "$version" -gt "$current" ]; then
    target="/signatures/$base.cvd"
    temporary_dir=$(mktemp -d "/signatures/.seed-$base.XXXXXX")
    temporary="$temporary_dir/$base.cvd"
    cp "$source" "$temporary"
    sigtool --info "$temporary" >/dev/null || { rm -f "$temporary"; rmdir "$temporary_dir"; exit 1; }
    chmod 644 "$temporary"
    mv -f "$temporary" "$target"
    rmdir "$temporary_dir"
    # A previous CLD must not shadow the newly verified CVD.
    rm -f "/signatures/$base.cld"
    echo "Installed verified $base signatures: $current -> $version"
  fi
done
for source in /var/lib/clamav/*.cvd.sign; do
  [ -f "$source" ] || continue
  target="/signatures/$(basename "$source")"
  [ -f "$target" ] || cp "$source" "$target"
done
chown -R clamav:clamav /signatures
# Registry refresh imports databases without contacting the blocked CDN.
[ "${1:-}" != "--seed-only" ] || exit 0
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
