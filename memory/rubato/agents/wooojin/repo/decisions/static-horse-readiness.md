---
description: Static horse room implementation-readiness context and spatial-contract decisions
---

# Static horse room readiness

> **STALE (2026-08-28):** v2 종결과 함께 이 pre-code 패키지·공간 계약은 이력이 됐다. v3는 회색 충돌판부터 재착수하므로 이 문서의 계약을 현재 지시로 읽지 않는다.

After an earlier FAIL, the spatial contracts are now being closed through an approved pre-code package rather than immediate implementation. The current stage is deliberately limited to the horse scale, cloth entrance, corridor widths, branch/rejoin relationships, and relative measurements; defer actual flight/collision replay and large failure fixtures until the isolated implementation stage. This scope reduction was explicitly approved by the user on 2026-08-23.

The approved pre-code package is intentionally small:

1. `world.json` as the single numeric source of truth, including provenance and ranges.
2. A full-stage technical section SVG with a visual dressing layer inspired by ImageGen references, but no copied image scale or perspective.
3. A linked horse-room detail SVG.
4. A small read-only validator plus browser rendering and independent visual QA.

The technical diagram must remain coordinate-bearing (for example, JSON-driven SVG), not another unconstrained ImageGen concept image. The purpose is to make the stage's spatial contract inspectable before code, not to increase checklist volume. Do not invent undecided large obstacles or add an editor/generator as part of this stage.
