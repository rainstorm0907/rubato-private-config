---
name: codex-claude-global-sync
description: "코덱스 전역세팅(~/.codex)이 업스트림, 클로드(~/.claude)로 주기 동기화하는 구조와 이식 규칙"
metadata: 
  node_type: memory
  type: project
  originSessionId: 86b32449-8bc2-4c2c-919d-62cbfc1d5e69
---

2026-07-03에 `~/.codex` 전역세팅을 `~/.claude`로 이식 완료. 우진님은 코덱스 쪽을 먼저 다듬고 클로드로 가져오는 흐름을 씀 — **코덱스가 업스트림**.

**Why:** 두 CLI의 전역 지침/스킬이 갈라지면 같은 요청에 다른 품질이 나옴. 동기화 방향과 변환 규칙을 알아야 다음 동기화가 빠름.

**How to apply:**
- 스킬: `~/.codex/skills/` → `~/.claude/skills/` rsync (`.DS_Store` 제외). 도구 중립적이라 거의 무수정.
- AGENTS.md → CLAUDE.md 병합 시 변환: 서브에이전트 표는 클로드 체계로 (explorer→내장 Explore, general-*→general-purpose+model 지정, worker→[[codex-meight-global-setup]], researcher/reviewer→`~/.claude/agents/*.md` 커스텀 에이전트).
- meight·codex-reviewer/discusser MCP 라우팅 섹션은 클로드 전용이므로 보존.
- config.toml의 hooks(cmux/oh-my-codex/eclam)·플러그인은 코덱스 앱 전용, 이식 금지.
- 백업 위치: `~/.claude/backups/codex-port-20260703/`
- 미이식 잔여(보류): `~/.codex/prompts/speckit.*`·`DEBUG.md` 슬래시 커맨드화. (context7 MCP는 2026-07-04 user scope로 추가 완료)
- 2026-07-04 추가 세팅: permissions allowlist(읽기전용 MCP 6종), 전역 PostToolUse prettier 훅(프로젝트 로컬 바이너리 있을 때만), CLAUDE.md 다이어트(329→217줄, pre-diet 백업 있음), "2회 교정 실패→새 세션" 규칙.
- 2026-07-04 역방향(클로드→코덱스) 동기화: ① prettier 훅을 `~/.codex/hooks/prettier-post-tool.py` + hooks.json PostToolUse(matcher `apply_patch`)로 이식 — patch원문/changes/상대경로 3형태 파이프 테스트 통과, 실제 apply_patch 페이로드 필드명은 [Unverified](다음 코덱스 편집 세션에서 확인). ② consult 스킬 라우팅 문구를 AGENTS.md·CLAUDE.md 리서치 행에 추가. ③ "2회 교정 실패→리셋" 규칙 AGENTS.md Context Resilience에 추가. 스킬 디렉토리는 meight(클로드 오케스트레이터측)/meight-worker(코덱스 워커측) 분리 빼고 동일 유지가 정상.
