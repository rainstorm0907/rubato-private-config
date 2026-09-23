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

before="$(git -C "$repo" rev-parse HEAD)"
bun_was_clean=false
[[ -z "$(git -C "$repo" status --porcelain -- bun.lock)" ]] && bun_was_clean=true
"$updater" "$@"
after="$(git -C "$repo" rev-parse HEAD)"

# The public installer currently installs harness/rubato-pi but can leave the
# live profile server without its own dependencies. Repair only an incomplete
# tree so ordinary up-to-date launches do not hit the network.
server_root="$repo/harness/pi-server"
if [[ -f "$server_root/package.json" ]] \
  && ! npm ls --prefix "$server_root" --depth=0 >/dev/null 2>&1; then
  npm install --prefix "$server_root"
fi

"$root/scripts/apply-rubato-overlays.sh" --apply

# Each overlay skill records the official commit it was last merged against in
# `.rubato-private-overlay` (`base=<sha>`). Compare that base, not the commit this
# run started from: a delta that fell behind on an earlier update must keep
# warning until it is actually re-merged, even when HEAD did not move today.
"$root/scripts/check-overlay-bases.sh" || true

# `bun install` can refresh workspace resolution rows even when the fetched commit
# already carries its intended lockfile. Only clean a new unstaged drift; preserve a
# bun.lock change that belonged to the user before the official updater ran.
bun_after="$(git -C "$repo" status --porcelain -- bun.lock)"
if [[ "$bun_was_clean" == true && "$bun_after" == " M bun.lock" ]]; then
  git -C "$repo" restore --worktree -- bun.lock
  echo "cleaned updater-generated bun.lock drift"
fi

echo "Rubato updated; personal overlays remain active"
