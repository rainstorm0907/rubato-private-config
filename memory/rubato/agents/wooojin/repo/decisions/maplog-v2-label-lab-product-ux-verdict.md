---
description: LabelPartition's review-unit UI failed as a product. The map shows an automatic Place; the user does not build places by hand, and merge/split is not a 1.0 surface.
---

## Conclusion

- The Lab review UI is not a product surface. Six-strata sampling and a fixed review unit (`N번째 자리`) are an internal diagnostic, not how the user sees their photos. A grouping mechanic that worked is not a product UX success.
- The product shows an automatic Place on the map. The user does not select photos to assemble a correct place. Merge, split, and undo are not a 1.0 surface. If that screen is opened later, succession is in [[decisions/maplog-place-visit-correction-lineage.md]] and `/Users/wooojin/App/maplog/record/PRODUCT.md`.
- Place first, capture-local day second, still holds. See [[decisions/maplog-v2-place-first-map-day-second-journey.md]].

## Rationale

- Chose throwing out the review UI. The screen hid why a group existed and dropped the intent of choosing on a map.
- Rejected: a product feature where the user selects photos and groups them into a new place, and reviving the six-strata review UI because the mechanic worked. Later verdict: the map shows the automatic result, and the user does not do classification labor beside a correct result. See [[decisions/maplog-v2-place-audit-experiment.md]].

## Symptom

> “묶이는데 이거 실제 유저한테 배포할때는 이 기능은 가만히 두면서 UI는 진짜 다 갈아엎어야할수준이야. 일단 6자리라고 못박아둔것도 너무 불편하고 무슨 기준으로 나눠진지도 모르겠고, 지도에서 고르려는 의도도 사라지고 그냥 왜 만든건지 거의 모를정도로 이질감 들어”
