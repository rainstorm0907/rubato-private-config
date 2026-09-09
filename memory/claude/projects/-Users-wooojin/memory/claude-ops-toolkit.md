---
name: claude-ops-toolkit
description: ~/dev/claude-ops — ECC 레포에서 채택한 5개 메커니즘(완료 게이트·교훈 수집함·drift doctor·compact 핸드오프·스킬 실적) 구현체와 운영법
metadata: 
  node_type: memory
  type: project
  originSessionId: ec8a2872-1e75-46c8-ae4c-f8b0590a87cc
  modified: 2026-08-13T15:54:34.706Z
---

2026-08-12 구축. 해커톤 우승자 레포(everything-claude-code) 검토 후 5개 메커니즘만 자체 구현해 `~/dev/claude-ops`(git)에 모음. 훅은 `~/.claude/settings.json`에 병합됨(두 swap 프로필 settings.json이 정본으로 심볼릭이라 전 프로필 적용). 데몬·LLM 호출 없음, python3 stdlib만.

- **완료 게이트**: 프로젝트 git root에 `VERIFY.md`가 있으면(옵트인) 편집 후 검증 증거 없이 완료 선언 시 Stop 훅이 1회 차단. 증거는 `python3 ~/dev/claude-ops/bin/verify.py <root>` 실행 → `.verify/last.json`. maplog에 VERIFY.md 적용됨(빌드 명령+영역별 테스트 매핑).
- **교훈 수집함**: SessionEnd마다 user 메시지들이 `state/inbox.jsonl`에 자동 축적. 주기적으로 읽어 진짜 교훈만 메모리로 승격(자동 승격 금지가 설계 원칙).
- **drift doctor**: `bin/doctor.py`가 `manifest.json`(agbrowse 0.1.18 고정, 프로필 심볼릭, meight ping 등 8항목) 읽기 전용 대조. consult npm 패치 유실·설정 리셋 감지용. 새 관리 항목 생기면 manifest에 추가할 것.
- **compact 대비**: Stop 훅이 autoCompactWindow 대비 70%/85% 경고, PreCompact 훅이 최근 대화를 `state/handoffs/`에 자동 저장(최근 20개 유지).
- **스킬 실적**: Skill 호출이 `state/skill-usage.jsonl`에 기록, `bin/stocktake.py`로 월 1회 미사용·중복 감사.
- **digest.py 모드 (2026-08-14 코덱스가 확장)**: 기본 lessons 외에 `--mode workflow`(지시별 도구·대상·반응 묶음)와 `--mode signals`(교정·흥미·이탈 등 행동 신호 스코어링) 추가됨. 단 코덱스 rollout 포맷(`~/.codex/sessions/**/rollout-*.jsonl`, payload 구조)은 세 모드 모두 파싱 불가(turns=0) — 코덱스 스레드 checkup은 포맷 지원 추가 전까지 수동 추출 필요.
- **/checkup 스킬 (2026-08-12 추가)**: doctor + [[session-analysis-pipeline]] 3단계를 한 명령으로 고정. `skills/checkup/`(레포) → `~/.claude/skills/checkup` 심링크, 증분 기준은 `state/checkup.json`의 last_run. 공개 배포판은 별도 레포 `~/dev/claude-checkup` = github.com/rainstorm0907/claude-checkup (MIT, luna 대신 Claude 서브에이전트, CLAUDE.md 제안 방식) — 개인판 수정 시 배포판에도 반영할지 확인할 것.

**Why:** 세션 학습이 수동 기억에 의존, 검증이 관례 수준, 환경 drift를 사후 발견하던 세 약점을 결정적(훅) 장치로 메움.

**How to apply:** 끄려면 settings.json에서 해당 훅 엔트리 삭제(README에 조각별 명시). 새 프로젝트에 게이트를 걸려면 `templates/VERIFY.md` 복사. inbox 검토 시 [[fable-token-routing-policy]]·기존 메모리와 중복 확인 후 승격. 관련: [[codex-meight-global-setup]], [[consult-chatgpt-research]].
