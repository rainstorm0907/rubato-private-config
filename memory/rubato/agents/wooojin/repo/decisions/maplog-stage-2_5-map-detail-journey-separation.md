---
description: Maplog main map is place first, and a place's photo detail splits by capture-local day. Recap is a period, not an open journey-staging choice.
---

## Conclusion

- On the main map, Place is first.
- In a Place's photo detail, photos inside the same place are shown split by capture-local day.
- Recap starts from a period on its own tab. A saved Journey, and the choice of staging it as a one-day chapter or as per-place scenes, is outside 1.0. Do not ask that question as if it were still open. Scope is `/Users/wooojin/App/maplog/record/PRODUCT.md`. See [[reference/projects/maplog-seed-first-decision.md]].

## Rationale

- Chose to separate the storage unit from the screen that stages a Journey, so the map and the photo detail could be confirmed without freezing Recap.
- A Visit, `Place + capture-local day`, stays the smallest stable group. Do not freeze a screen's staging unit onto that storage unit.
- Rejected: leaving Stage 3 Journey/Recap staging awaiting confirmation. Recap's entry is a period, and 1.0 excludes a saved Journey.

## Symptom

같은 장소가 먼저고, 같은 날이 그다음 이 맞긴한거같아. 그리고 journey를 어디에서 보냐에 따라 다른거같아. 메인 지도화면이라면 최신버전이 확실해. 그렇게 나눈다음, 사진 상세 누르면 같은 장소 내부에 같은 날끼리 묶인 사진들이 나눠져서 보이는거지.
