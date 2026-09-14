#!/bin/sh

case "${ANTHROPIC_AUTH_TOKEN-}" in
  sk-ant-oat*) unset ANTHROPIC_AUTH_TOKEN ;;
esac
