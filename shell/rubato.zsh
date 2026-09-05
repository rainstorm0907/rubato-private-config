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
    source "/Users/wooojin/App/rubato-private-config/scripts/prepare-rubato-env.sh"
    exec "$RUBATO_HARNESS/scripts/rubato-soul.sh" "$@"
  )
}

dispatch() {
  (
    source "/Users/wooojin/App/rubato-private-config/scripts/prepare-rubato-env.sh"
    exec "$RUBATO_HARNESS/scripts/rubato-dispatch.sh" "$@"
  )
}
