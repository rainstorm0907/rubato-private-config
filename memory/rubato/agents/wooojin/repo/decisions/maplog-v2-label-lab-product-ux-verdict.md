---
description: 2026-09-02 CP-1 physical-device verdict: LabelPartition mechanics worked, but the review-unit UI failed the product goal and must be replaced by a map-first Place-first/day-second experience.
---
# Maplog V2 LabelPartition Lab 제품 UX 판정

- 날짜: 2026-09-02
- 맥락: iPhone 14 실제 사진 보관함에서 LabelPartition Lab의 첫 장소 묶기를 수행했다.
- 관련 결정: [[repo/decisions/maplog-v2-place-first-map-day-second-journey.md]]

우진 원문:

> “묶이는데 이거 실제 유저한테 배포할때는 이 기능은 가만히 두면서 UI는 진짜 다 갈아엎어야할수준이야. 일단 6자리라고 못박아둔것도 너무 불편하고 무슨 기준으로 나눠진지도 모르겠고, 지도에서 고르려는 의도도 사라지고 그냥 왜 만든건지 거의 모를정도로 이질감 들어”

상태: 사용자 확정 · 기능 경계는 구현·실기기 확인됨 · 제품 UI는 폐기·재설계 대기.

판정:

- 사진을 선택해 새 장소로 묶는 기능과 LabelPartition 저장 구조는 유지한다.
- 현재 `N번째 자리`/고정 review-unit 중심 UI는 제품 표면으로 사용하지 않는다.
- six-strata sampling은 내부 진단 장치이며 사용자 정보구조가 아니다.
- 제품 표면은 지도를 출발점으로 장소를 고르고, 그 장소의 사진을 확인한 뒤 같은 날을 2순위로 다루는 흐름으로 다시 설계한다.
- 현재 Lab UI의 기계적 성공을 제품 UX 성공으로 번역하지 않는다.
- CP-2 정책 채점보다 먼저 이 UX 실패를 명시적으로 보존한다.