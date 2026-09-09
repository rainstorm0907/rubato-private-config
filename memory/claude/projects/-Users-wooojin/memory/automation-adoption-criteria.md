---
name: automation-adoption-criteria
description: 자동화·설정 채택 기준 — 리소스 최소(데몬·LLM 상시호출 금지)와 장기 유지성이 기능 수보다 우선
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ec8a2872-1e75-46c8-ae4c-f8b0590a87cc
  modified: 2026-08-12T03:10:01.548Z
---

2026-08-12 claude-ops 구축 지시: "리소스도 덜먹고, 나중에 유지성도 생각하면서 전부 해줘". 해커톤 우승자 레포 검토 결론("설정 늘리지 마라, 반복되는 것만 자동화해라")과 같은 방향으로 우진님이 확정한 기준.

**Why:** 기능을 많이 붙이는 것보다 상시 프로세스 없음·훅당 수십 ms·stdlib only·끄기 쉬움이 우진님의 acceptance 기준. 새 스킬·훅·자동화 제안 시 이 기준을 못 넘으면 제안 자체를 보류.

**How to apply:** 자동화 추가 전 체크: ① 반복 사용 근거가 있나 ② 데몬·상시 LLM 호출 없이 되나 ③ 한 줄 삭제로 끌 수 있나 ④ 6개월 뒤에도 이해 가능한가. 관련: [[claude-ops-toolkit]], [[session-analysis-pipeline]].
