# Personal launch overlay until the public setup-token fix is merged.
unalias rubato rubato-pi rubato-soul dispatch 2>/dev/null

rubato() {
  "$HOME/.local/bin/rubato-personal" "$@"
}

rubato-pi() {
  "$HOME/.local/bin/rubato-personal" "$@"
}

rubato-soul() {
  (
    case "${ANTHROPIC_AUTH_TOKEN-}" in
      sk-ant-oat*) unset ANTHROPIC_AUTH_TOKEN ;;
    esac
    export RUBATO_NO_VAULT=1
    exec "$RUBATO_HARNESS/scripts/rubato-soul.sh" "$@"
  )
}

dispatch() {
  (
    case "${ANTHROPIC_AUTH_TOKEN-}" in
      sk-ant-oat*) unset ANTHROPIC_AUTH_TOKEN ;;
    esac
    export RUBATO_NO_VAULT=1
    exec "$RUBATO_HARNESS/scripts/rubato-dispatch.sh" "$@"
  )
}
