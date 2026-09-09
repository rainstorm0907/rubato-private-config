---
description: Maplog Stage 2.5의 Place·Visit 합치기·나누기·Journey 승계 법률과 별도 UX 판정 필요성에 관한 사용자 확정.
---
# Maplog Place·Visit 교정 승계 법률

- 날짜: 2026-09-03
- 맥락: Stage 2.5에서 Place를 합치거나 나눈 뒤 기존 Journey와 Visit가 어느 쪽을 계속 가리킬지 정했다.
- 관련 기록: [[decisions/maplog-stage-2_5-map-detail-journey-separation.md]]

우진 원문:

> “어 ㅇㅇ ㅇㅋ 그 규칙들 합리적이다. 대신 그 합치고 나누는 ux 가 매우 중요할것으로 생각된다. 버튼이던지, 뭐 따로 기능이 있던지, 메인지도에서 편하게 드래그해서 묶던지. 일단 알겠어. 확정하자”

상태:

- **사용자 확정:** 합칠 때 사용자가 고른 대상 Place와 같은 날짜 target Visit가 살아남고, 흡수된 참조는 그쪽으로 이어진다.
- **사용자 확정:** 나눌 때 남겨 둔 사진 쪽이 기존 Place를 유지한다. Visit 사진 전체를 옮기면 Visit도 이동하고, 일부만 옮기면 남은 쪽이 기존 Visit를 유지한다.
- **사용자 확정:** 새 Visit는 기존 Journey에 자동 추가하지 않는다. 합치기로 중복된 Journey Visit는 앞 순서를 유지하며 교정 직후 feedback과 undo로 알린다.
- **사용자 확정:** 다음 attach나 교정 전까지 직전 교정 한 단계에 persistent undo를 제공한다.
- **사용자 확인 대기:** 버튼·별도 기능·메인 지도 drag 등 합치기·나누기 진입 UX. 이 예시는 후보이지 확정 방식이 아니다.

UX 제약:

- 합치기·나누기 UX는 데이터 법률과 별도로 핵심 제품 판정을 받아야 한다.
- 이전에 반려한 큰 합치기 행동을 메인 사진 감상 화면에 되살리지 않는다.
- 발견성, 오합치기 방지, 결과 이해, 즉시 feedback·undo를 실제 사진 지도 시제품에서 판정한다.
