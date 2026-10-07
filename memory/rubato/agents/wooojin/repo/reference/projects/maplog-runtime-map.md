---
description: Map runtime principles to use in Maplog map mocks and implementation.
---
## Naver map usage principle

- Status: user confirmed · 2026-08-30.
- Context: the point of redesigning after a journey-selection mock made on an HTML OSM still background failed to verify real coordinates, camera, and map quality.
- Woojin's original: “앞으로 naver 연동 키고 작업해.”
- Application: Maplog map UI mocks, implementation, and visual QA are done on a real map surface with Naver map integration on. If a key or server state is blocked, report it as a blocker; do not close it out with a static substitute map.
