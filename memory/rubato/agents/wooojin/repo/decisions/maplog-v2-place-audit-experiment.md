---
description: Maplog V2 Place audit의 다방향 통제 실험 결정과 audit/product 경계.
---
## 결정

상태: 사용자 확정·구현됨·검증 진행 중

2026-09-02, 기존 LabelPartition Lab UI를 폐기하고 지도 기반 Place audit의 세부 상호작용을 고르는 맥락에서 우진:

> "그럼 그 실측을 보다 객관적으로 볼 수 있게 여러 방향으로 테스트하는게 어때? 세부적인건 어떻게해볼 생각이야?"

이어 Opus High와 논의하면서 실험판을 만들도록 확정했다:

> "알겠어 그러면 opus high링 의논하면서 실험판 한번 만들어봐"

## 확정된 경계

- audit과 제품 UX를 분리한다. audit은 편향 없는 작은 판단 실험이고, 제품은 자동 정리된 Place 결과에서 예외만 고치는 흐름이다.
- 실제 Naver 지도 위의 DEBUG 전용 sibling route로 만들며 기존 map-less LabelPartition Lab에 지도를 얹지 않는다.
- 진입 방식만 바꾸고 지도·사진·선택 가능 범위·post-entry 행동은 같게 유지한다. 한 번에 변수 하나만 비교한다.
- 실험판은 in-memory 상태만 쓰고 Lab JSON·제품 SQLite·PhotoKit·CP-2 label을 건드리지 않는다.
- 진행률·남은 수·다음 작업·자동 진급·예측·기존 라벨을 보이지 않는다.
- 합성 fixture 실험은 이해 불가·표현 불가를 반증하는 용도이며 실제 사진에서의 우열이나 CP-2 정답 품질까지 주장하지 않는다.
- 기존 family/viewport/display cluster는 Place membership 권위가 아니다.

## 구현 상태

`MaplogV2/PlaceAudit` DEBUG 실험판과 세 진입 모드(`mapSeed`, `photoSeed`, `area`)가 구현됐다. 상태: 구현됨·기계/Simulator 검증됨·사용자 비교 실측 대기.

2026-09-02 실제 Naver 지도에서 `mapSeed`의 folded card → overlap drawer → 두 장 선택 → `장소 1곳 · 방문 2일 · 사진 2장` → 정확한 되돌리기까지 걸었고, `photoSeed`·`area` opening도 같은 지도/fixture에서 렌더했다. `모르겠어요`는 distinct visual state로 남으며, photoSeed/area opening의 off-arm folded-card tap은 inert다. `NMFMarker`는 SDK 계약대로 position/icon을 넣은 뒤 map에 attach해야 실제 marker가 보인다.

이 실험은 framing이 이해 불가능한지와 상호작용이 표현 가능한지는 반증할 수 있지만, 합성 사진으로 실제 사진 성능의 승자를 정하지 않는다. arm 간 비교 불가능했던 `reachedOutsideOpeningCards` 지표는 제거했다.

## 사용자 실측 결론

상태: 사용자 확정·제품 방향 확정·구현 대기.

2026-09-02, `mapSeed / repeat` 실험판을 직접 만진 뒤 우진: "그냥 다른 ui 다 필요없고 지금 띄운 ... 이화면 만 쓸모가 있는거같아. 자동으로 클러스터 된걸 저렇게 보여주고, 저거보단 더 크게. 그리고 왜 클러스터 과정을 유저한테 시키는거야?"

세 진입 arm과 blank audit를 제품 후보에서 폐기한다. 제품은 자동으로 만든 Place cluster 결과를 지도에서 더 크게 보여주고, 사용자는 정상 결과를 승인·재구성하지 않는다. 틀린 cluster가 있을 때만 결과 화면에서 예외를 합치거나 나누거나 되돌린다. blank audit는 내부 진단 도구로만 남긴다.