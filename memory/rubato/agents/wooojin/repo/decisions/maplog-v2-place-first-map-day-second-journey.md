---
description: Maplog V2에서 장소를 지도 grouping 1순위, 날짜를 2순위로 두고 Stage 3 전에 선택 피로와 display-only cluster를 해결하자는 사용자 방향과 열린 해석.
---
# Maplog V2 장소 우선 지도·날짜 차선 Journey

- 날짜: 2026-09-02
- 맥락: Stage 2 조작·capture-day occurrence·production timezone resolver의 실기기 관문을 닫고, Stage 3 Recap 전에 날짜 장면을 지도에 표현하는 다음 관문을 논의했다.

우진 원문:

> “날짜 장면을 지도에 제대로 보여주기 위해, 복잡한거 말고도 제일 중요한 사용자 입장에서는 : 같은 장소 1순위로 묶이길 원하고 2순위가 같은 날이야. 근데 지금같은 구조에서 하나하나 다 추가하기 솔직히 조금 귀찮은 상태거든? 이건 조금 대책이 필요할거같아. 외부 의견 들어봐야되나.. 'cluster를 ‘데이터 묶기’가 아니라 ‘화면 정리’로 바꿔야 해' 이건 진짜 필수야 꼭 해내야돼. 일단 stage3 조금만 뒤에 하자 이것들부터 제대로 완벽하게 끝내자 너가 말한것들까ㅈ지”

현재 확정된 방향:

- Stage 3 Recap은 잠시 더 잠근다.
- 사용자 관점의 지도 grouping 우선순위는 같은 장소가 1순위, 같은 날이 2순위다.
- 사진을 한 장씩 Journey에 추가해야 하는 현재 상호작용의 피로를 줄이는 대책이 필요하다.
- cluster는 membership이나 장면 정체성을 다시 계산하는 데이터 grouping이 아니라, stable한 단위를 화면에서 정리하는 display-only 규칙이어야 한다.
- 외부 의견을 받아 product model과 선택 상호작용을 검토한다.

열린 해석:

- map entity를 장소 stack, Journey selection unit을 장소×날짜 visit, Recap section을 day로 둘지 아직 확정하지 않았다.
- 같은 장소를 여러 날 방문했을 때는 날짜별 Visit으로 나누고, 같은 날 여러 장소를 한 번에 담는 명시적 bulk action을 제공한다.
- 관련 장면을 자동 선택하지 않는 기존 원칙을 유지하면서, 추가 전에 범위·장소 수·사진 수를 보여주는 방문 전체/같은 날 일괄 추가 UX가 필요하다.

외부 검토 뒤 정리된 모델:

- `Photo → Place → VisitOccurrence(Place + capture-local day)`로 둔다.
- 지도 entity는 Place, Journey의 ordered selection unit은 Visit, LocalDay는 여러 Visit을 묶어 보는 색인·일괄 추가 범위다.
- 기존 day occurrence는 폐기하지 않고 날짜 근거·색인으로 강등한다.
- DisplayCluster는 viewport·zoom에 따른 일시적 표현이며 Place/Visit/Journey identity나 membership에 절대 관여하지 않는다.

같은 장소를 같은 날 오전·저녁에 다시 간 경우에 대한 우진 결정:

> “한 방문으로 보자”

맥락: 2026-09-02, `Visit = Place + capture-local day`와 별도 `VisitSession` 도입 여부를 정하는 자리. 따라서 같은 Place와 같은 capture-local day의 사진은 시간 간격과 무관하게 하나의 Visit으로 보고, 방문 안 사진 순서로 시간 흐름을 보여준다. 시간 간격 기반 자동 분할은 만들지 않는다.

추가 진행 결정:

> “ㅇㅋ 그럼 consult까지 나오면 내가 판정 해줄게 지금은 섵불리 판정하기 힘들다”

맥락: 2026-09-02, 같은 Place 판정 정책과 `r_v1`을 synthetic/local 분석만으로 확정할지 논의한 자리. user-provided 기존 ChatGPT 세션의 unbiased consult와 real-library adjudication 설계가 모두 나온 뒤 우진이 판정한다. 그 전에는 Place formation algorithm·거리값·POI 계층을 구현 결정으로 승격하지 않는다.

same-session consult 결과:

- 사용자가 지정한 기존 `Maplog V2 전환 자문` 대화에서 2026-09-02 unbiased 후속 검토를 완료했다.
- 좌표 결과를 Place로 직접 취급하지 말고 `PhotoLocationObservation → PlaceInferenceProposal → 사용자 소유 Place → Visit → Journey`로 한 층 더 분리하라고 권고했다.
- 초기 그림자 추론은 가까운 좌표 병합에 전체 지름 상한과 모호한 외곽점의 단일 부착 조건을 두며, 첫 버전부터 사용자 Place 합치기·분리를 포함하라고 권고했다.
- raw 좌표를 외부로 보내지 않는 device-side Place Lab에서 사진 쌍이 아니라 주변 구역의 Place partition을 라벨링하고, 조정 집합과 잠근 검증 집합을 분리하라고 권고했다.
- local synthetic analysis는 connected-components chaining, fixed-grid boundary split, full-library reclustering의 threshold sensitivity를 기각하고 persisted Place를 재계산하지 않는 frozen-authority runtime을 권고했다.

사용자 판정:

> “어 그게 맞는거같아.”

맥락: 2026-09-02, same-session consult와 local synthetic analysis를 비교한 뒤 다음 합성안을 확인한 자리.

확정된 Place 정책 방향:

- Place는 좌표 군집이나 외부 POI가 아니라 사용자가 같은 장소로 다루는 영속적인 기억 단위다.
- 좌표 정책은 버전이 붙은 `PlaceInferenceProposal`을 만들 뿐 Place identity를 만들지 않는다.
- 최초 그림자 분석은 가까운 좌표 병합에 전체 지름 상한과 모호한 외곽점의 단일 부착 조건을 둔 compact 추론을 비교한다.
- device-side Place Lab에서 주변 구역의 사진과 지도를 보며 사용자가 실제 Place partition을 합치고 나눈 뒤 bootstrap 정책을 고른다.
- Place가 확정되면 runtime은 persisted Place를 전체 재clustering하지 않는다. 새 사진은 보수적으로 attach하거나 reconciliation proposal을 만든다.
- false merge를 false split보다 비싼 오류로 다루며 사용자 merge/split은 fallback이 아니라 Place v1의 기본 기능이다.
- 기존 v2 날짜 Journey는 새 의미로 마이그레이션하지 않고 v3 Place/Visit 표와 Journey order를 병렬로 만든다.
- DisplayCluster는 Place presentation을 viewport에서 정리하는 일시 객체이고 persistence·membership·Journey 명령 권한이 없다.
- 첫 구현은 Place Lab 하나이며, 실제 보관함 판정 전에는 meter 값을 제품 상수로 확정하지 않는다.

구현 진행 승인:

> “답변 오면 적당히 이제 수정할거 수정하고 굳힐거 해서 구현들어가보자 내 응답은 ㅇㅋ. 에이전트 안 헤매게 잘 교정해줘”

맥락: 2026-09-02, Anthropic Opus 5가 Place Lab 성공 기준과 implementer contract를 독립 감사하는 동안의 사전 승인. 답변이 오면 리드가 발견된 빈칸·충돌을 교정하고, binding law·가설·사용자 판정 지점을 분리한 구현 계약으로 고정한 뒤 추가 승인 대기 없이 Place Lab 구현에 들어간다. 에이전트가 meter 값·Place 의미·privacy boundary·merge/split 범위를 임의로 결정하지 않게 한다.

상태: **사용자 방향 확정 / Opus 계약 감사 대기 / 감사 뒤 Place Lab 구현 승인 / algorithm meter 값 미확정 / Stage 3 잠금 유지**.