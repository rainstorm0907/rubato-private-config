---
description: 2026-09-02 CP-1 physical-device verdict: LabelPartition mechanics worked, but the review-unit UI failed the product goal and must be replaced by a map-first Place-first/day-second experience.
---
# Maplog V2 LabelPartition Lab product UX verdict

- Date: 2026-09-02
- Context: The first place-grouping of LabelPartition Lab was performed on the iPhone 14 real photo library.
- Related decision: [[repo/decisions/maplog-v2-place-first-map-day-second-journey.md]]

Woojin's original:

> “묶이는데 이거 실제 유저한테 배포할때는 이 기능은 가만히 두면서 UI는 진짜 다 갈아엎어야할수준이야. 일단 6자리라고 못박아둔것도 너무 불편하고 무슨 기준으로 나눠진지도 모르겠고, 지도에서 고르려는 의도도 사라지고 그냥 왜 만든건지 거의 모를정도로 이질감 들어”

The Lab review UI is not a product surface. The product surface is the map gallery in `record/PRODUCT.md`. Do not revive the six-strata, review-unit-centered UI because the grouping mechanic worked.

Verdict:

- Keep the feature that selects photos and groups them into a new place, and the LabelPartition storage structure.
- Do not use the current `N번째 자리` / fixed review-unit-centered UI as a product surface.
- Six-strata sampling is an internal diagnostic device, not the user's information structure.
- Redesign the product surface as a flow that starts from the map, chooses a place, checks that place's photos, and then treats the same day as second.
- Do not convert the current Lab UI's mechanical success into a product UX success.
- Explicitly preserve this UX failure before CP-2 policy scoring.
