---
name: agent-taskforce-setup
description: agent-taskforce 스킬의 정본·레포 위치와 claude-swap 프로필 간 심볼릭링크 공유 구조
metadata: 
  node_type: memory
  type: project
  originSessionId: 2bb1bd24-543b-4a63-9124-50ed4eee5ffa
  modified: 2026-08-06T13:43:42.318Z
---

`agent-taskforce` 스킬은 정본이 `~/.claude/skills/agent-taskforce/` + `~/.claude/agents/{workstream-owner,independent-verifier}.md` + `~/.claude/team-grid.sh`이고, 버전 보관 레포는 **private** `keepitmello/agent-taskforce` (로컬 클론 `~/dev/agent-taskforce`). 개선은 정본에서 하고 `GIT_OK=1 ./snapshot.sh` → commit → push 순서다. 레포에서 직접 고치지 않는다.

claude-swap 두 프로필(`1-laventador12`, `2-dalisalvador1231`)의 `skills/`·`agents/`는 **`~/.claude`를 가리키는 심볼릭링크**라 한 번 고치면 양쪽에 동시 반영된다. 반면 `settings.json`·`CLAUDE.md`는 프로필별 개별 파일이라 따로 맞춰야 하고, `statusline.sh`·`team-grid.sh` 같은 루트 스크립트는 swap 대상이 아니라 공유된다.

2026-08-06 기준 v5까지 복원 완료(그 전엔 정본이 v3 이전이라 v3~v5 개선이 빠져 있었다). 미복구 항목 하나: 케이스 스터디에 기록된 `statusline.sh`의 subagent 잔량 오표시 수정(`subagentStatusLine` payload의 `contextWindowSize` 사용)은 snapshot 대상이 아니어서 이 맥에 없다.

**Why:** 정본과 레포 방향을 거꾸로 잡으면 개선이 조용히 유실된다 — 실제로 v3~v5가 정본에 없었다.
**How to apply:** 스킬을 고치기 전에 `~/dev/agent-taskforce`에서 `git log`로 최신 버전을 확인하고, 고친 뒤엔 반드시 snapshot→push까지 한다. 관련: [[codex-claude-global-sync]]
