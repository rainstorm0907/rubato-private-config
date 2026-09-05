#!/bin/sh
set -eu

root="${RUBATO_PRIVATE_CONFIG:-/Users/wooojin/App/rubato-private-config}"
if [ "${1-}" = "update" ]; then
  shift
  exec "$root/scripts/update-rubato.sh" "$@"
fi

. "$root/scripts/prepare-rubato-env.sh"

repo="${RUBATO_REPO:-/Users/wooojin/dev/Rubato}"
exec "$repo/harness/scripts/rubato-pi.sh" "$@"
