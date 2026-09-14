#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_root="$root/overlays/skills"
destination="$HOME/.agents/skills"

[[ "${1-}" == "--apply" ]] || {
  echo "dry run only; pass --apply to write"
  for source in "$source_root"/*/; do
    [[ -f "$source/SKILL.md" ]] || continue
    rsync -ani --delete "$source/" "$destination/$(basename "$source")/"
  done
  exit 0
}

mkdir -p "$destination"
for source in "$source_root"/*/; do
  [[ -f "$source/SKILL.md" ]] || continue
  target="$destination/$(basename "$source")"
  mkdir -p "$target"
  rsync -a --delete "$source/" "$target/"
done

mkdir -p "$HOME/.claude/skills" "$HOME/.codex/skills" "$HOME/.local/bin"
for client in claude codex; do
  link="$HOME/.$client/skills/browser-cli"
  rm -rf "$link"
  ln -s "$destination/browser-cli" "$link"
done
for command in abrowse gbrowse isearch; do
  ln -sf "$destination/browser-cli/scripts/$command" "$HOME/.local/bin/$command"
done
ln -sf "$root/scripts/rubato-clean-env.sh" "$HOME/.local/bin/rubato-personal"

shell_hook="[ -f \"$root/shell/rubato.zsh\" ] && source \"$root/shell/rubato.zsh\""
# The official installer owns an alias block. Keep the personal hook after it so
# these functions, especially the setup-token sanitizer, are the live commands.
touch "$HOME/.zshrc"
shell_tmp="$(mktemp "${TMPDIR:-/tmp}/rubato-zshrc.XXXXXX")"
trap 'rm -f "$shell_tmp"' EXIT
grep -Fvx "$shell_hook" "$HOME/.zshrc" > "$shell_tmp" || true
printf '%s\n' "$shell_hook" >> "$shell_tmp"
if ! cmp -s "$shell_tmp" "$HOME/.zshrc"; then
  cat "$shell_tmp" > "$HOME/.zshrc"
fi
rm -f "$shell_tmp"
trap - EXIT

echo "applied Rubato personal overlays from $source_root"
