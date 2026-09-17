---
description: 2026-09-10 Rubato Codex(기존 ChatGPT.app Codex에 얹은 --target codex) 설치 상태, co-thinking v0.3 오버레이 방식, Codex↔Rubato 기억 공유 규칙, 되돌리기 위치.
---
# Rubato Codex 설치 상태 (2026-09-10)

상태: 사용자 확정·구현됨·검증됨(Codex CLI로 실제 홈에 질의).

## 구조

- 방식 B: 기존 `ChatGPT.app`의 Codex(`~/.codex`)에 `rubato-codex/install.sh install --target codex --providers cursor,xai --migrate-legacy` 로 얹음. 별도 Rubato.app(격리 프로필)은 프로젝트·기록이 안 보여서 폐기. 우진: "내 프로젝트랑 로컬 기록 다 안뜨는데" → "b로 해줘".
- 프록시: 전역 opencodex 2.23→2.48. 2.48이 `gpt-6-astra`를 네이티브로 찾음(Astra 안 보이던 원인은 8/17 고정 카탈로그). 서브에이전트 roster 레포 기준: Sol·Fable·Opus·Grok(xai)·Gemini Flash.
- 옛 `~/.codex/skills` 사본 8개는 `enabled=false`로만(파일 안 옮김).

## co-thinking v0.3을 Codex에 얹는 법

- 정본: `/Users/wooojin/App/rubato-private-config/scripts/apply-rubato-codex-overlays.sh --apply`. 플러그인 캐시(`~/.codex/plugins/cache/rubato/rubato-codex/<ver>/skills`)에 5개 스킬 통째(`metaFrame`→`metaframe` 이름 치환) + dispatching Open variables 헝크 + AGENTS.md 개인 블록 + 루트 지침(`model-instructions.md`)의 존댓말 문장을 voice.md 반말로 패치.
- rubato-codex 재설치는 캐시를 초기화하므로 그 뒤 이 스크립트를 다시 돌린다.
- Codex는 `codex-discusser`를 두 번 봄(`~/.agents/skills` 판 + `rubato-codex:` 판). 내용 동일하게 유지해야 함.

## 전역 지침·기억

- `~/.codex/AGENTS.md`는 옛 "Codex Execution Charter"(작업자 시절)를 버리고 개인 것만 남김(말투=voice.md, 지키는 것 3줄, 담당 연결, working-rules 네 단락, msearch, 스탠스, 폴더 관례). 작업 방식 계약은 rubato-codex 루트 지침이 맡음. 우진: "rubato식 관점으로 봤을때 좀 줄여도 되지 않아?"
- 말투는 AGENTS.md만으론 안 먹고 루트 지침 문장이 이김 → 오버레이가 그 줄을 패치.
- 기억: Codex도 같은 `msearch`(독립 셸 스크립트, Redis 6380)로 Rubato 기억을 회수하고, 지속 가치 있을 때만 `~/.rubato/memory/agents/wooojin/repo`에 직접 쓴다(memory-discipline 읽기 → 편집 → 즉시 커밋, `system/` 제외). Codex 샌드박스가 read-only면 Redis가 막힘; 실제 설정은 danger-full-access라 됨.

## v0.4-r2.1 소폭 보완 (2026-09-16 묶음)

`rubato-v0.4-r2.1-targeted-update.zip`의 `patch.py`로 문단 3개만 교체(전체 덮어쓰기 아님). 대상: `codex-discusser/references/co-thinking.md`(현재 자료에 연결된 전례 회수), `dispatching/SKILL.md`(통상 구현은 담당 재량, 중요한 장점을 희생하는 절충만 리드에게), `dispatching/references/bounded-follow-through.md`(수치 통과가 절충을 대신 판정하지 않음). 세 벌(활성 `~/.agents/skills`, `rubato-private-config/skills`, `overlays/skills`) 총 9파일. Codex 층은 `apply-rubato-codex-overlays.sh --apply`로 co-thinking만 반영 — Codex의 `dispatching/SKILL.md`는 공개 rubato-codex 판이라 r2 문단 자체가 없고 이번 대상이 아니다.

복원: `python3 patch.py rollback --plan ~/Downloads/rubato-r2.1-local-plan --confirm` (계획 폴더 보존 필요).

## 되돌리기

`/Users/wooojin/App/rollback/co-thinking-v0.3-2026-09-10/README.md` (Rubato층·Codex층·프록시 각각의 사전 사본과 명령).
