---
description: The multi-direction controlled-experiment decision for the Maplog V2 Place audit, and the audit/product boundary.
---
## Decision

The audit is not the product. The product shows an automatic Place result. See the measurement conclusion below and `record/PRODUCT.md`.

2026-09-02, in the context of discarding the existing LabelPartition Lab UI and choosing the detailed interaction of a map-based Place audit, Woojin:

> "그럼 그 실측을 보다 객관적으로 볼 수 있게 여러 방향으로 테스트하는게 어때? 세부적인건 어떻게해볼 생각이야?"

Then, while discussing with Opus High, confirmed making an experiment build:

> "알겠어 그러면 opus high링 의논하면서 실험판 한번 만들어봐"

## Confirmed boundary

- Separate audit from product UX. Audit is a small unbiased judgment experiment, and the product is a flow that fixes only exceptions in an automatically organized Place result.
- Make it a DEBUG-only sibling route on the real Naver map, and do not put a map on top of the existing map-less LabelPartition Lab.
- Change only the entry method, and keep the map, photos, selectable range, and post-entry behavior the same. Compare only one variable at a time.
- The experiment build uses in-memory state only, and does not touch Lab JSON, product SQLite, PhotoKit, or CP-2 labels.
- Do not show progress, remaining count, next task, automatic promotion, prediction, or existing labels.
- A synthetic fixture experiment is for disproving incomprehensibility and inexpressibility, and does not claim which is better on real photos, or CP-2 answer quality.
- Existing family/viewport/display clusters are not authority for Place membership.

## Implementation status

The `MaplogV2/PlaceAudit` DEBUG experiment and the three entry modes (`mapSeed`, `photoSeed`, `area`) were a comparison device. They are not a product queue.

On 2026-09-02, on the real Naver map, walked `mapSeed` through folded card → overlap drawer → selecting two photos → `장소 1곳 · 방문 2일 · 사진 2장` → an exact undo, and also rendered the `photoSeed` and `area` openings on the same map/fixture. `모르겠어요` remains a distinct visual state, and an off-arm folded-card tap on the photoSeed/area opening is inert. Per the SDK contract, `NMFMarker` must have position and icon set and then be attached to the map for the actual marker to appear.

This experiment can disprove whether the framing is incomprehensible and whether the interaction is expressible, but it does not pick a winner of real-photo performance from synthetic photos. Removed the `reachedOutsideOpeningCards` metric, which could not be compared across arms.

## User measurement conclusion

2026-09-02, after directly using the `mapSeed / repeat` experiment build, Woojin: "그냥 다른 ui 다 필요없고 지금 띄운 ... 이화면 만 쓸모가 있는거같아. 자동으로 클러스터 된걸 저렇게 보여주고, 저거보단 더 크게. 그리고 왜 클러스터 과정을 유저한테 시키는거야?"

Discard the three entry arms and the blank audit as product candidates. The map shows an automatically made Place result. The user does not approve or rebuild a correct result. Merge, split, and undo of a wrong place are not a 1.0 surface; the succession rules, if that screen is opened later, are in [[decisions/maplog-place-visit-correction-lineage.md]] and PRODUCT. The blank audit stays an internal diagnostic only.
