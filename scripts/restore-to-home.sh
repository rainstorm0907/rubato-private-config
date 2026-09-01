#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
apply=false

case "${1-}" in
  "") ;;
  --apply) apply=true ;;
  *)
    echo "usage: $0 [--apply]" >&2
    exit 2
    ;;
esac

rsync_args=(-a)
if [[ "$apply" == false ]]; then
  rsync_args+=(--dry-run --itemize-changes)
  echo "dry run only; pass --apply to write"
fi

if [[ "$apply" == true ]]; then
  mkdir -p \
    "$HOME/.agents/skills" \
    "$HOME/.claude/agents" \
    "$HOME/.claude/hooks" \
    "$HOME/.codex/agents" \
    "$HOME/.codex/rules"
fi

rsync "${rsync_args[@]}" "$root/skills/" "$HOME/.agents/skills/"
rsync "${rsync_args[@]}" "$root/global/claude/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
rsync "${rsync_args[@]}" "$root/global/claude/settings.json" "$HOME/.claude/settings.json"
rsync "${rsync_args[@]}" "$root/global/claude/agents/" "$HOME/.claude/agents/"
rsync "${rsync_args[@]}" "$root/global/claude/hooks/" "$HOME/.claude/hooks/"
rsync "${rsync_args[@]}" "$root/global/codex/AGENTS.md" "$HOME/.codex/AGENTS.md"
rsync "${rsync_args[@]}" "$root/global/codex/config.toml" "$HOME/.codex/config.toml"
rsync "${rsync_args[@]}" "$root/global/codex/agents/" "$HOME/.codex/agents/"
rsync "${rsync_args[@]}" "$root/global/codex/rules/" "$HOME/.codex/rules/"

if [[ "$apply" == true ]]; then
  echo "restored global config from $root"
fi
