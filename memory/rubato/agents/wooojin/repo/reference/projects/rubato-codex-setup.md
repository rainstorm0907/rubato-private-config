---
description: 2026-09-10 Rubato Codex (the existing ChatGPT.app Codex with --target codex laid on top) install state, the co-thinking v0.3 overlay method, the Codex↔Rubato memory-sharing rule, and where to roll back.
---
# Rubato Codex install state (2026-09-10)

Status: user confirmed · implemented · verified (queried the actual home with the Codex CLI).

## Structure

- Method B: laid onto the existing `ChatGPT.app` Codex (`~/.codex`) with `rubato-codex/install.sh install --target codex --providers cursor,xai --migrate-legacy`. A separate Rubato.app (isolated profile) was discarded because projects and records did not show. Woojin: "내 프로젝트랑 로컬 기록 다 안뜨는데" → "b로 해줘".
- Proxy: global opencodex (`~/.npm-global/bin/opencodex`) 2.76 (2026-10-03). **If a new model does not show in Codex, suspect the opencodex version first** — an old version does not know the new model, so it does not put it in the catalog (`~/.codex/opencodex-catalog.json`) (9/10 Astra, and on 10/3 both `gpt-6.1-sol` and `gpt-6-luna` had this cause). `opencodex update` stops with `cache_entry_foreign_owner` because of root-owned files under `~/.npm`, so run it as `npm_config_cache=/tmp/npm-cache-ocx opencodex update`. The old homebrew copy (2.23) was deleted on 10/3 — this is the only install. Subagent roster, repository basis: Sol, Fable, Opus, Grok (xai), Gemini Flash.
- The 8 old `~/.codex/skills` copies are `enabled=false` only (files not moved).

## How to lay co-thinking v0.3 onto Codex

- Canonical: `/Users/wooojin/App/rubato-private-config/scripts/apply-rubato-codex-overlays.sh --apply`. Into the plugin cache (`~/.codex/plugins/cache/rubato/rubato-codex/<ver>/skills`), the 5 skills whole (`metaFrame`→`metaframe` name substitution) + the dispatching Open variables hunk + the AGENTS.md personal block + a patch of the honorific sentence in the root instructions (`model-instructions.md`) to the "반말" (informal speech) of voice.md.
- A rubato-codex reinstall resets the cache, so run this script again after that.
- Codex sees `codex-discusser` twice (the `~/.agents/skills` copy + the `rubato-codex:` copy). The contents must be kept the same.

## Global instructions and memory

- `~/.codex/AGENTS.md` dropped the old "Codex Execution Charter" (from the worker days) and kept only the personal part (speech = voice.md, 3 lines of what to keep, owner connection, the four working-rules paragraphs, msearch, stance, folder conventions). The work-method contract is owned by the rubato-codex root instructions. Woojin: "rubato식 관점으로 봤을때 좀 줄여도 되지 않아?"
- Speech style does not take from AGENTS.md alone; the root-instruction sentence wins → the overlay patches that line.
- Memory: Codex also retrieves Rubato memory with the same `msearch` (an independent shell script, Redis 6380), and writes directly to `~/.rubato/memory/agents/wooojin/repo` only when it has durable value (read memory-discipline → edit → commit immediately, excluding `system/`). If the Codex sandbox is read-only, Redis is blocked; the actual setting is danger-full-access, so it works.

## v0.4-r2.1 small supplement (2026-09-16 bundle)

Replaced only 3 paragraphs with `patch.py` from `rubato-v0.4-r2.1-targeted-update.zip` (not a full overwrite). Targets: `codex-discusser/references/co-thinking.md` (retrieve precedents connected to the current material), `dispatching/SKILL.md` (ordinary implementation is the owner's discretion; only a tradeoff that sacrifices an important advantage goes to the lead), `dispatching/references/bounded-follow-through.md` (a numeric pass does not judge a tradeoff in its place). Three copies (active `~/.agents/skills`, `rubato-private-config/skills`, `overlays/skills`), 9 files in total. The Codex layer reflects only co-thinking via `apply-rubato-codex-overlays.sh --apply` — Codex's `dispatching/SKILL.md` is the public rubato-codex copy, so the r2 paragraph itself is absent and is not a target this time.

Restore: `python3 patch.py rollback --plan ~/Downloads/rubato-r2.1-local-plan --confirm` (the plan folder must be kept).

## Rollback

`/Users/wooojin/App/rollback/co-thinking-v0.3-2026-09-10/README.md` (prior copies and commands for each of the Rubato layer, the Codex layer, and the proxy).
