#!/bin/sh
set -eu

case "${ANTHROPIC_AUTH_TOKEN-}" in
  sk-ant-oat*) unset ANTHROPIC_AUTH_TOKEN ;;
esac

repo="${RUBATO_REPO:-/Users/wooojin/dev/Rubato}"
exec "$repo/harness/scripts/rubato-pi.sh" "$@"
