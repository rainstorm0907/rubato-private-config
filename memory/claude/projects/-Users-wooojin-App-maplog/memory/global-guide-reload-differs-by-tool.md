---
name: global-guide-reload-differs-by-tool
description: "Claude는 전역 지침을 세션 시작 시 1회만 로드하고, Codex는 world_state로 세션 도중 반복 재주입한다"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6e06b8f5-4258-455d-9bc2-1b3fc2eba7cb
  modified: 2026-07-27T13:54:32.586Z
---

전역 지침 파일을 고쳤을 때 적용 시점이 도구마다 다릅니다.

- **Claude Code**: `~/.claude/CLAUDE.md`는 세션 시작 시 컨텍스트에 박히고 도중에 갱신되지 않습니다. 실행 중인 세션은 옛 내용을 계속 씁니다. `claude --resume <id>`로 다시 열면 시스템 프롬프트가 재구성되며 새로 읽습니다.
- **Codex CLI**: `~/.codex/AGENTS.md`는 프로젝트 `AGENTS.md`와 병합돼 rollout jsonl의 `world_state.payload.state.agents_md.text`로 **세션 도중 반복 재주입**됩니다. 2026-07-27 확인: 7/19에 시작한 세션 하나에서 34회가량 재스냅샷. 따라서 장기 resume 세션도 다음 턴부터 새 지침을 받습니다.

확인 방법: 해당 세션에 "지금 로드된 전역 지침 첫 줄"을 물어봅니다.

**Why:** 지침을 고친 뒤 "세션을 새로 파야 하나"를 도구마다 다르게 판단해야 합니다.
**How to apply:** Claude 지침 변경은 resume 또는 새 세션이 필요하고, Codex 지침 변경은 그냥 다음 턴부터 적용됩니다.
