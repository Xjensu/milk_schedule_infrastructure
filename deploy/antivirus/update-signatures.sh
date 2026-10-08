#!/bin/sh
set -eu
# Seed a new volume from the official image, including detached signatures.
for source in /var/lib/clamav/*.cvd /var/lib/clamav/*.cvd.sign; do
  [ -f "$source" ] || continue
  target="/signatures/$(basename "$source")"
  [ -f "$target" ] || cp "$source" "$target"
done
chown -R clamav:clamav /signatures
exec freshclam --datadir=/signatures --daemon --foreground=true --stdout
