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

echo "synced global config into $root"
