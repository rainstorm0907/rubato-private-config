---
description: Woojin's Codex CLI actual-record home. CodexBar must look here.
---
---
description: Woojin's Codex CLI actual-record home. CodexBar must look here.
---
# Codex CLI actual-record home

Status: user confirmed · verified. 2026-09-13, Woojin gave the path directly.

Canon: `/Users/wooojin/App/codex-plain-home`
- Sessions: `sessions/YYYY/MM/DD/rollout-*.jsonl`
- Tokens: `last_token_usage` of `event_msg` / `token_count`
- config `model = "gpt-6-astra"`

`~/.codex` is a separate record. Do not put luna/terra from OpenCodex `~/.opencodex/usage.jsonl` in as yesterday's usage. Woojin's original: "어제 luna terra 쓴적없으니까 제대로 방금 아스트라같이 로컬에 존재하는 경로만 전부 다 찾고서 전부 재갱신해"

A 76MB rollout is cut by CodexBar's file size limit. A workaround was needed: put only that day's token_count into `~/.codex/sessions` as a small extract.
