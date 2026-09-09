#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

sync_dir() {
  local source="$1"
  local destination="$2"
  shift 2
  case "$destination/" in
    "$root/"*) ;;
    *)
      echo "refusing sync destination outside repository: $destination" >&2
      exit 2
      ;;
  esac
  mkdir -p "$destination"
  rsync "$@" "$source/" "$destination/"
}

sync_dir "$HOME/.agents/skills" "$root/skills" -aL --delete --delete-excluded \
  --exclude='.git/' \
  --exclude='node_modules/' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='*.bak' \
  --exclude='*.bak-*' \
  --exclude='.DS_Store' \
  --exclude='.consult/' \
  --exclude='.omx/' \
  --exclude='.consult-backup-*'

install -m 0644 "$HOME/.claude/CLAUDE.md" "$root/global/claude/CLAUDE.md"
install -m 0644 "$HOME/.claude/settings.json" "$root/global/claude/settings.json"
sync_dir "$HOME/.claude/agents" "$root/global/claude/agents" -a --delete \
  --exclude='__pycache__/' --exclude='*.pyc' --exclude='.DS_Store'
sync_dir "$HOME/.claude/hooks" "$root/global/claude/hooks" -a --delete \
  --exclude='__pycache__/' --exclude='*.pyc' --exclude='.DS_Store'

install -m 0644 "$HOME/.codex/AGENTS.md" "$root/global/codex/AGENTS.md"
install -m 0644 "$HOME/.codex/config.toml" "$root/global/codex/config.toml"
sync_dir "$HOME/.codex/agents" "$root/global/codex/agents" -a --delete \
  --exclude='*.bak-*' --exclude='.DS_Store'
sync_dir "$HOME/.codex/rules" "$root/global/codex/rules" -a --delete \
  --exclude='*.bak-*' --exclude='.DS_Store'

sync_dir "$HOME/.codex/memories" "$root/memory/codex" -a --delete --delete-excluded \
  --exclude='.git/' \
  --exclude='.omx/' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='.DS_Store'

# Keep the memory, but never copy the third-party API credential recorded in it.
maplescouter_note="$root/memory/codex/extensions/ad_hoc/notes/2026-07-08T20-43-09+0900-maplescouter-api-tooling.md"
if [[ -f "$maplescouter_note" ]]; then
  sed -E -i '' 's/(api-key: )[[:alnum:]-]+/\1[redacted]/g' "$maplescouter_note"
fi

sync_dir "$HOME/.claude/projects" "$root/memory/claude/projects" \
  -a --delete --delete-excluded --prune-empty-dirs \
  --exclude='.DS_Store' \
  --include='*/' \
  --include='*/memory/***' \
  --exclude='*'

sync_dir "$HOME/.rubato/memory/agents" "$root/memory/rubato/agents" \
  -a --delete --delete-excluded --prune-empty-dirs \
  --exclude='*/repo/.git/***' \
  --exclude='.DS_Store' \
  --include='*/' \
  --include='*/repo/***' \
  --exclude='*'

echo "synced global config into $root"
