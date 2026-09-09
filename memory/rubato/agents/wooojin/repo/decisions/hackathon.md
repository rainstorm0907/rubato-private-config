---
description: 해커톤·공모전 운영 방식 — proof spine, 문서 구조, 릴리스 검증.
---
해커톤·공모전 운영 워크플로우. `~/.codex/memories`에서 옮겨왔다. 우진이 Cofathon의 동결·재현 규율과 KB AI Challenge의 제품 서사를 하나의 운영 방식으로 합치기로 한 결과다.

다음 대회부터 쓰기로 한 방식이라 지속 의도가 강하지만, "대회 참가 중"이라는 맥락에서만 켜지는 조건부 규칙으로 둔다.

## Proof spine

"한 줄 → 한 사용자 경로 → 한 코드 경로 → 한 검증 명령 → 한 제출 주장."

입력 1건부터 결과 복귀까지 실제로 연결한 뒤에만 병렬 확장을 시작한다.

## 3층 문서 구조

- 개인 skill
- 프로젝트 문서: START_HERE / DECISIONS / CONTRACT / RELEASE
- AGENTS.md는 안전 규칙만

## 협업과 릴리스

- 독립 worktree + integration owner + clean release worktree. GitHub는 마일스톤 백업 전용. 통합은 60~90분 단위.
- Release 단계에서는 정확한 제출 ZIP을 **새 디렉터리에서 재검증**한다: install / build / test / hero smoke / PDF render / claim-evidence.

## 지난 대회 기록

- Cofathon 원티드 AI 해커톤 수상 뱃지는 수령 완료 (2026-08-28 우진 확인: "원티드뱃지 이미 수령했어"). 관련 원티드 회신 메일도 8/5 발송 완료 — 이 건은 종결.

- KB AI Challenge 최종 제출물은 비공개 `keepitmello/KB-hackaton` 저장소의 `KB이음케어_우브라더스_제출_최종.zip`(2026-08-03 커밋 확인). GitHub 검색 시 collaborator·organization 저장소까지 포함해야 찾힌다.
- Morrow(Cofathon-Full-Mock-02) 피부 궁합 판정 엔진: `DECISION_THRESHOLD=50`, `NEGATIVE_EVIDENCE_THRESHOLD=0.12`는 당시 임시값이고 최종 확정이 아니다. 판단보류는 근거 부족에만 쓰고, 긍정·부정 충돌은 맞음/안맞음으로 판정한 뒤 경고를 노출한다. 오버엔지니어링 금지, 우진이 짚지 않은 규칙을 임의로 추가하지 않는다.
