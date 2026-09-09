---
name: verify-before-done
description: 완료 주장은 런타임·화면·실데이터 증거로만 — 워커의 PASS/COMPLETE는 주장이지 사실이 아님
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ec8a2872-1e75-46c8-ae4c-f8b0590a87cc
  modified: 2026-08-12T03:40:38.529Z
---

7~8월 4개 배치 전부에서 반복된 마찰: "Codex의 'COMPLETE/통과' 보고가 실측과 달랐던 게"(7/28), "내 사진 넣어보니까 이렇게 뜨는데? 왜 기본이랑 추천이 안뜨고"(7/21), "아니 멍청아 지금 크롬 창이 두개잖아"(7/28), 리뷰 브리프 30개 세션에 "정적 추측보다 렌더 근거 우선·추측은 실패로 처리" 명시.

**Why:** 빌드 성공·정적 검사·워커 보고는 런타임·시각 품질의 증거가 아님. 특히 UI는 실제 데이터(위치 있는 사진 등)로 실제 화면을 봐야 하고, 브라우저 작업은 지금 보이는 창 상태부터 확인해야 함. 확인 못 한 영역을 PASS로 포장하는 순간 우진님이 직접 발견하게 되고 그게 최악.

**How to apply:** 완료 보고 전에 ① 대표 사용자 경로 실제 실행 ② UI 변경은 스크린샷 ③ 워커 PASS는 재현하거나 증거 파일 확인 ④ 못 본 범위는 "확인 못 함"으로 명시. 기계적 반쪽은 [[claude-ops-toolkit]]의 VERIFY.md 게이트가 담당 — 이 메모리는 행동 반쪽. 관련: [[delegated-work-status-reporting]].
