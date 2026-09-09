---
name: delegated-work-status-reporting
description: "위임 작업이 길어지면 \"아직도 안됨?\" 전에 상태·막힌 곳·다음 확인 시점을 선제 보고"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ec8a2872-1e75-46c8-ae4c-f8b0590a87cc
  modified: 2026-08-12T03:09:53.609Z
---

2026-08-12 메이트 리뷰 대기 중 우진님이 "아직도 안됨?"라고 물음 — 기다리게 만든 것 자체가 마이너스.

**Why:** 워커·메이트가 수 분 이상 돌 때 조용히 있으면 우진님은 멈춘 건지 도는 건지 알 수 없음. 폴링 결과를 내가 먼저 알고 있어도 전달 안 하면 없는 것과 같음.

**How to apply:** 위임 작업 시작 시 예상 소요를 한 줄 알리고, 오래 걸리면 물어보기 전에 "현재 상태 + 그동안 내가 병행 중인 것"을 짧게 업데이트. 완료 보고에는 결과 파일 경로·검증 증거를 같이. 관련: [[codex-meight-global-setup]].
