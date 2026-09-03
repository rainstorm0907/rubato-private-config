#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo="${RUBATO_REPO:-/Users/wooojin/dev/Rubato}"
updater="$repo/harness/scripts/rubato-update.sh"

[[ -x "$updater" ]] || {
  echo "Rubato updater not found: $updater" >&2
  exit 2
}
[[ "$(git -C "$repo" branch --show-current)" == "rubato/base" ]] || {
  echo "Rubato must be on rubato/base before updating" >&2
  exit 2
}
[[ -z "$(git -C "$repo" status --porcelain)" ]] || {
  echo "Rubato worktree is not clean; refusing to update" >&2
  exit 2
}

before="$(git -C "$repo" rev-parse HEAD)"
"$updater" "$@"
after="$(git -C "$repo" rev-parse HEAD)"

"$root/scripts/apply-rubato-overlays.sh" --apply

if [[ "$before" != "$after" ]]; then
  changed="$(
    git -C "$repo" diff --name-only "$before..$after" -- harness/skills |
      awk -F/ 'NF >= 3 { print $3 }' |
      sort -u
  )"
  overlap=""
  while IFS= read -r name; do
    [[ -n "$name" && -d "$root/overlays/skills/$name" ]] && overlap+="${overlap:+, }$name"
  done <<< "$changed"
  if [[ -n "$overlap" ]]; then
    echo "warning: official updates also changed personal overlay skills: $overlap" >&2
    echo "the personal versions remain active; review and merge those upstream changes separately" >&2
  fi
fi

[[ -z "$(git -C "$repo" status --porcelain)" ]] || {
  echo "Rubato update left a dirty worktree" >&2
  exit 1
}

echo "Rubato updated; personal overlays remain active"
