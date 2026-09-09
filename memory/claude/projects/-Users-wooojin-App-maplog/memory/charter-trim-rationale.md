---
name: charter-trim-rationale
description: "전역 헌장 축소(2026-07-28)의 유지 원칙 — Claude엔 검증 지시를 다시 넣지 않고, Codex엔 반대로 유지한다. 안전 절 삭제는 우진님 확정"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9aa53213-c216-4d8f-a0a9-b18cf7126ab9
  modified: 2026-08-06T07:38:44.214Z
---

2026-07-28 전역 헌장 두 개를 축소했다 (`~/.claude/CLAUDE.md` 75→56줄, `~/.codex/AGENTS.md` 103→57줄, 백업 `.bak-20260728`). 결과물은 파일 자체가 정본이고, 여기 남기는 건 다시 되돌리지 않기 위한 원칙이다.

- **Claude 헌장에 검증 강제 지시를 다시 넣지 않는다.** 공식 Opus 5 프롬프팅 처방("스스로 검증하니 명시 지시를 빼라")에 따라 삭제한 것.
- **Codex 헌장의 Verification 절은 유지한다.** OpenAI GPT-5.6 공식 가이드는 반대로 검증 지시를 넣으라고 처방한다. Anthropic 처방을 Codex에 이식하면 안 된다.
- **안전 게이트(production 사인오프·파괴적 작업 게이트) 삭제는 우진님 사용자 확정.** 하네스 기본 프롬프트가 이미 강제하므로 중복이라는 판단. 단 Codex의 비밀 유출 금지 1줄은 우진님 지시로 유지.
- Codex 삭제 기준은 "기본 프롬프트(base_instructions) 중복". 위임 보고는 기본 평문 — 고정 형식(STATUS/EVIDENCE/UNVERIFIED)은 위임 브리프가 명시할 때만.
- 주입 경로는 CLAUDE.md 단일 소스 — `--append-system-prompt` 슬롯은 실행별 delta 전용으로 비워둠 (CLAUDE.md는 compaction 후 재로드되므로 이중 주입은 낭비).

관련: [[code-review-agent-uses-opus5]]
