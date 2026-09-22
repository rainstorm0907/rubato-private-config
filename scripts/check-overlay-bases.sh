#!/usr/bin/env bash
# Warn for every overlay skill whose official counterpart changed after the
# commit recorded as `base=<sha>` in `overlays/skills/<name>/.rubato-private-overlay`.
# Exit 1 when at least one overlay is stale so callers can notice; never modifies files.
#
# After re-merging an overlay onto the current official skill, refresh its base:
#   scripts/check-overlay-bases.sh --mark <name>
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo="${RUBATO_REPO:-/Users/wooojin/dev/Rubato}"
ref="${RUBATO_BASE_REF:-rubato/base}"
head="$(git -C "$repo" rev-parse "$ref")"

if [[ "${1-}" == "--mark" ]]; then
  name="${2-}"
  [[ -n "$name" && -d "$root/overlays/skills/$name" ]] || {
    echo "usage: $0 --mark <overlay-skill-name>" >&2
    exit 2
  }
  printf 'managed by rubato-private-config\nbase=%s\n' "$head" > "$root/overlays/skills/$name/.rubato-private-overlay"
  echo "$name base=$head"
  exit 0
fi

stale=0
for dir in "$root"/overlays/skills/*/; do
  name="$(basename "$dir")"
  [[ -d "$repo/harness/skills/$name" ]] || continue
  marker="$dir.rubato-private-overlay"
  base="$(sed -n 's/^base=//p' "$marker" 2>/dev/null | head -1)"
  if [[ -z "$base" ]]; then
    echo "warning: overlay $name has no recorded official base; run: $0 --mark $name after merging" >&2
    stale=1
    continue
  fi
  if ! git -C "$repo" cat-file -e "$base^{commit}" 2>/dev/null; then
    echo "warning: overlay $name base $base is not in $repo" >&2
    stale=1
    continue
  fi
  changed="$(git -C "$repo" diff --name-only "$base" "$head" -- "harness/skills/$name" | wc -l | tr -d ' ')"
  if [[ "$changed" != "0" ]]; then
    echo "warning: official $name changed in $changed file(s) since overlay base ${base:0:9}; personal version stays active" >&2
    echo "  review: git -C $repo diff ${base:0:9} ${head:0:9} -- harness/skills/$name" >&2
    echo "  after merging into overlays/skills/$name run: $0 --mark $name" >&2
    stale=1
  fi
done
exit $stale
