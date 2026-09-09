---
name: session-analysis-pipeline
description: 세션 교훈 분석 표준 파이프라인 — 로컬 digest로 공짜 압축 → 코덱스 luna 추출 → Claude가 승격 판단
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ec8a2872-1e75-46c8-ae4c-f8b0590a87cc
  modified: 2026-08-12T04:40:57.329Z
---

2026-08-12 우진님 승인("지금 방법 이거 좋은거같은데")된 세션 분석 표준 절차. transcript(수 MB)를 LLM에게 직접 읽히는 것 금지 — 토큰 수십만 낭비.

1. **로컬 압축 (토큰 0)**: `python3 ~/dev/claude-ops/bin/digest.py <transcript.jsonl> <출력.md>` — user 메시지 전부 + 교정 직후 assistant 답변 앞부분 + 에러 지점만 추출해 수십 KB로 축소.
2. **추출 분석 = 코덱스 luna**: 다이제스트를 luna 워커에게 주고 "교정·반복 마찰·선호 표현 → 교훈 후보 목록 파일" 요구. 정답이 명확한 잔바리 작업이라 [[fable-token-routing-policy]] 그대로 luna. terra 이상 금지(과함).
3. **승격 판단 = Claude 본인**: 후보 목록만 읽고 기존 MEMORY.md와 중복 대조 후 진짜만 메모리 승격. 자동 승격 금지([[claude-ops-toolkit]] 설계 원칙).

**Why:** 세션 분석을 자주 할 예정인데, 원본 직독은 클로드 토큰을 태우고 luna 전체 읽기도 낭비. 압축은 공짜, 판단은 위임 불가.

**How to apply:** 진행 중 세션은 transcript 경로(`~/.claude-swap-backup/sessions/<프로필>/projects/<slug>/<session-id>.jsonl`)에서 직접, 지난 세션들은 `state/inbox.jsonl`(SessionEnd 자동 축적)에서. 월 1회 inbox 검토 때도 동일 3단계. **[갱신 2026-08-12] 이 절차는 `/checkup` 스킬로 고정됨** — 정기 실행은 스킬을 부르면 되고, 이 메모리는 배경 원리 기록.
