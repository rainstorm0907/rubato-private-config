#!/bin/sh

case "${ANTHROPIC_AUTH_TOKEN-}" in
  sk-ant-oat*) unset ANTHROPIC_AUTH_TOKEN ;;
esac

rubato_private="${RUBATO_PRIVATE_CONFIG:-/Users/wooojin/App/rubato-private-config}"
resume_hook="--import=$rubato_private/runtime/resume-recovery-register.mjs"
case "${NODE_OPTIONS-}" in
  *resume-recovery-register.mjs*) ;;
  *) export NODE_OPTIONS="${NODE_OPTIONS:+$NODE_OPTIONS }$resume_hook" ;;
esac

export RUBATO_NO_VAULT=1
