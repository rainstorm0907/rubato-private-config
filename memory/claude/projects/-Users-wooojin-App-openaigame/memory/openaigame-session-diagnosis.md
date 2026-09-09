---
name: openaigame-session-diagnosis
description: "8/13~8/16 코덱스 세션(맵 구조 설계) 전수 분석 결과 — 문서 SSOT 부패와 [100]~[102] 표류가 핵심, compaction 자체는 무죄에 가까움"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9c613d64-6082-498f-ad87-c033e08c9f51
  modified: 2026-08-17T16:25:30.344Z
---

2026-08-18 checkup에서 코덱스 세션(019ffad1, 8/13~8/16, 105발화·compaction 29회)을 digest.py 강화 후 grok-4.6 워커 5개로 전수 분석한 결론.

- **최대 실패**: e25 압축+ABORT 직후 [100]에서 "좌표 띠(공중 궤적)"가 "충돌 지형 구현"으로 재서술 → docs/26 `floorTop` 지상 코스(Hill Climb) 구현 → [103] 전면 폐기. 허가의 빈칸은 사용자 [100]("다음 단계 가보자")과 [102]의 이중 명사(길/지형지물/구현).
- **문서 부패가 주범**: 결정을 그 턴에 문서에 박은 것(docs/23)은 생존, 대화에만 있으면 소실. START_HERE.md는 결정 원장이 아니라 "현재 단계 전광판"이 되어 11개 에폭 재작업. 폐기된 구현 허가(docs/24~26, START_HERE)가 회수 안 된 채 세션 종료 — 다음 세션이 START_HERE만 읽으면 실패한 지상 맵을 재개할 위험.
- **compaction은 거의 무죄**: 발화 15 영구 소실은 AGENTS.md 주입문이라 설계 영향 미미. 이중 compaction 구간도 단절 약함. 진짜 단절은 압축 직후 assistant의 "단계 재진술" 1건.
- **환경**: 8/15 01:06 sol(high)→daybreak-blue(medium) 전환 후 맵 국면 전체가 medium으로 진행. 인과 단정은 불가하나 "혼난 직후 + effort 하락 = 범위 축소 습관 강화" 패턴 관찰.
- **반복 패턴**: 사용자 "크게"([44][55][59]) vs assistant "한 조각만" 축소 습관; 짧은 교정 발화 오독이 가장 비싼 실패([58][61][65][98][103]).
- 미완 검증 2건: [99] 밸런스 4조합 판정 비행 스킵, 음향 3번 재수정 미청음.
- 분석 원본: `~/dev/claude-ops/state/digests/checkup/20260818-openaigame/analysis-b1~b5.md` (에폭 다이제스트 동봉). digest.py는 코덱스 에러/마커/에폭 분할/ENV·INSTR 추적으로 강화됨(v2).

관련: [[rocket-playtest-round1-verdict]]
