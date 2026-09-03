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
ln -sf "$destination/browser-cli/scripts/isearch" "$HOME/.local/bin/isearch"
ln -sf "$root/scripts/rubato-clean-env.sh" "$HOME/.local/bin/rubato-personal"

shell_hook="[ -f \"$root/shell/rubato.zsh\" ] && source \"$root/shell/rubato.zsh\""
if ! grep -Fqx "$shell_hook" "$HOME/.zshrc"; then
  printf '\n%s\n' "$shell_hook" >> "$HOME/.zshrc"
fi

echo "applied Rubato personal overlays from $source_root"
