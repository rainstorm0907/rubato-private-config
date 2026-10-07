---
description: Same-place verdict defaults Woojin confirmed for Maplog real photos — 40m link, 100m maximum width.
---

## Conclusion

- A same-place verdict starts at a photo link distance of 40m and a maximum width of 100m per place. `SceneSpatialGrouping.swift` still states that policy (`coreDistanceMeters == 40`, `diameterCapMeters == 100`).
- DEBUG comparison ranges stay wide: link 20–60m, width 70–300m. Those ranges are for a later look, not a second default.

## Rationale

- Chose 40m/100m after Woojin tried the real-photo verdict screen and replaced his own looser guess. Outside densely packed zones the old 18m/45m range made almost no difference.
- Rejected: 18m/45m as the default. Rejected: 30m/100m as the lasting default. He floated 30m, then fixed 40m the same day.
- Do not retune these from a synthetic fixture or from this file's earlier guess. Reopen only with another real-photo verdict.

## Symptom

다 해봤는데, 일단 9, 10 , 11, 12 같이 다닥다닥 붙은거 아니면 거의 의미가 없네. 그냥 널널하게 30m / 100m정도로 하면 좋을거같은데?

40m / 100m가 최적인거같아 일단 이거로 고정하고 마무리 해도 되럭같아

폭 넓게 수정하게 해줘. 20에서 60. 70에서 300정도까지 그냥 다 해보게
