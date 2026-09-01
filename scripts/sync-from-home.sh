#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

rsync -aL --delete --delete-excluded \
  --exclude='.git/' \
  --exclude='node_modules/' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='*.bak' \
  --exclude='*.bak-*' \
  --exclude='.DS_Store' \
  --exclude='.consult/' \
  --exclude='.omx/' \
  --exclude='.consult-backup-*' \
  "$HOME/.agents/skills/" "$root/skills/"

install -m 0644 "$HOME/.claude/CLAUDE.md" "$root/global/claude/CLAUDE.md"
install -m 0644 "$HOME/.claude/settings.json" "$root/global/claude/settings.json"
rsync -a --delete --exclude='__pycache__/' --exclude='*.pyc' --exclude='.DS_Store' \
  "$HOME/.claude/agents/" "$root/global/claude/agents/"
rsync -a --delete --exclude='__pycache__/' --exclude='*.pyc' --exclude='.DS_Store' \
  "$HOME/.claude/hooks/" "$root/global/claude/hooks/"

install -m 0644 "$HOME/.codex/AGENTS.md" "$root/global/codex/AGENTS.md"
install -m 0644 "$HOME/.codex/config.toml" "$root/global/codex/config.toml"
rsync -a --delete --exclude='*.bak-*' --exclude='.DS_Store' \
  "$HOME/.codex/agents/" "$root/global/codex/agents/"
rsync -a --delete --exclude='*.bak-*' --exclude='.DS_Store' \
  "$HOME/.codex/rules/" "$root/global/codex/rules/"

echo "synced global config into $root"
