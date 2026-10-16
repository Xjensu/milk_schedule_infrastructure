#!/bin/sh
# A populated volume can still contain an obsolete seed database.
set -eu
export LC_ALL=C
directory=${1:-/signatures}
max_age=${CLAMAV_MAX_SIGNATURE_AGE_SECONDS:-259200}
case "$max_age" in ''|*[!0-9]*) exit 1 ;; esac
test -s "$directory/main.cvd" || test -s "$directory/main.cld"
daily="$directory/daily.cld"
[ -s "$daily" ] || daily="$directory/daily.cvd"
test -s "$daily"
build_time=$(sigtool --info "$daily" | sed -n 's/^Build time: *//p')
test -n "$build_time"
# GNU date (Debian) and BusyBox date (the official Alpine image).
timestamp=$(date -d "$build_time" +%s 2>/dev/null) || \
  timestamp=$(date -D '%d %b %Y %H:%M:%S %z' -d "$build_time" +%s 2>/dev/null) || \
  timestamp=$(date -D '%d %b %Y %H:%M %z' -d "$build_time" +%s)
age=$(( $(date +%s) - timestamp ))
test "$age" -ge -86400
test "$age" -le "$max_age"
