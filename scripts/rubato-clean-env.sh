#!/bin/sh
set -eu

root="${RUBATO_PRIVATE_CONFIG:-/Users/wooojin/App/rubato-private-config}"
if [ "${1-}" = "update" ]; then
  shift
  exec "$root/scripts/update-rubato.sh" "$@"
fi

case "${ANTHROPIC_AUTH_TOKEN-}" in
  sk-ant-oat*) unset ANTHROPIC_AUTH_TOKEN ;;
esac

repo="${RUBATO_REPO:-/Users/wooojin/dev/Rubato}"
exec "$repo/harness/scripts/rubato-pi.sh" "$@"
