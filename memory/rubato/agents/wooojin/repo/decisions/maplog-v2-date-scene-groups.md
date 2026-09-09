---
description: Maplog V2에서 지도 장면과 Journey 노드를 개별 사진이 아닌 고정된 날짜별 사진·동선 묶음으로 정의한 사용자 결정.
---
## 결정 상태

- 상태: **사용자 확정 / 도메인 계약 구현·검증됨 / runtime 연결 전**
- 날짜: 2026-09-01
- 맥락: iPhone 14 실제 보관함 2,835장으로 photo-first screen-collision planner를 검증한 뒤.

## 사용자 원문

> “전체 사진 다 보여주지 말고, 날짜별로 묶어서 보여주기”

> “이것도 장면을 원하는게 아니라 날짜별로 묶은거를 잇고싶어. 예를 들어 서울 여행이면 : 첫날 강북 논 사진 묶음 > 다음 유저의 선택은 다음날 강남을 간 사진 묶음. 이렇게 이틀치의 이동 동선을 묶고 싶어할거야. 단 한개씩 사진을 연결하는게 아니라.”

> “이거 너가 완벽히 이해해야돼. 핵심 문장에 이어지는 감성이야 이거”

## 제품 해석

- 사진 한 장은 기억의 증거이자 내용이지 Journey의 노드가 아니다.
- 날짜별 장면 묶음이 사진들과 그날의 이동 동선을 소유한다.
- Journey는 개별 사진이 아니라 날짜별 장면 묶음을 순서대로 잇는다.
- 지도 축척과 screen-space 충돌은 날짜 묶음의 identity, membership, 사진 수를 바꿀 수 없다.
- screen-space 충돌은 고정된 날짜 카드들을 잠시 포개는 표현 규칙으로만 쓴다. 서로 다른 날짜의 사진을 동적으로 하나의 그룹으로 합치지 않는다.
- `+n`은 현재 확대율에서 우연히 겹친 사진 수가 아니라, 대표 사진 뒤에 들어 있는 같은 날짜 묶음의 나머지 사진 수여야 한다.
- 겹친 카드 tap은 전체 사진을 평평하게 섞지 않고 날짜별 묶음을 먼저 보여 준다.

## 2026-09-01 probe 판정

- 통과: 실제 사진 카드, `+n` 즉시 감상, 사진 상세, Journey add/remove/cancel, marker pool.
- 반려: 화면 충돌로 grouping을 재계산하는 방식. 확대할 때 `+519 → +1229 → +781/+416 → +603 → +75/+24`처럼 소속과 개수가 바뀌고 “우수수”가 “팟 팟 팟”으로 바뀌었을 뿐이다.
- 성능도 반려: camera-change p95 85.3ms, idle p95 88.8ms, 최악 106.9ms.
- 결론: 고정할 절대값은 pixel/meter threshold가 아니라 날짜 장면 묶음의 identity와 membership이다.

## 확정된 날짜 경계

2026-09-01 우진:

> “어 그게 맞아. 같은 날 강북과 강남을 모두 갔어도 하루 묶음 하나로 보는게 맞아. 그리고 '날짜 묶음의 ID와 그 안에 들어 있는 사진들' 이걸 고정하는게 맞아.”

- 로컬 날짜 하루는 Journey 노드 하나다.
- 같은 날짜 안의 큰 장소 이동으로 장면을 자동 분할하지 않는다.
- 강북→강남처럼 멀리 이동해도 사진들과 그날의 내부 이동 동선으로 보존한다.
- 고정되는 값은 날짜 묶음 ID, 사진 membership, 그날의 내부 이동 동선이다.
- 지도 축척, 화면 충돌, 대표 사진 변경은 이 값을 바꿀 수 없다.

## 2026-09-01 도메인 체크포인트 결과

구현됨:

- `DayBucketPolicy`: Gregorian 달력 + 명시적 IANA 시간대 + 양수 정책 버전. 암묵적인 current/default 시간대 없음.
- `DaySceneGroupID`: 로컬 날짜와 정책 지문으로만 생성. membership·대표·route·지도 상태와 독립.
- `DaySceneGrouping`: 같은 날의 먼 장소를 한 그룹으로 유지. 위치 없는 사진은 membership에 남고 route에서만 제외.
- 명시적 예외 결과: 날짜 없음 `ungrouped`, 유효하지 않거나 달력 표현 범위 밖인 날짜 `invalidDated`, 같은 asset ID의 상충 metadata `conflictingIDs`.
- `OrderedJourneyDraft<ID>`: 기존 사진 Journey와 날짜 묶음 Journey가 add/remove/order/zero/duplicate 계약을 한 구현으로 공유.

검증됨:

- 날짜 도메인·compile probes `204 PASS`
- 기존 Journey `124 PASS`
- 기존 photo-card `113 PASS`
- V2·기존 Maplog simulator build 성공, V2 source warning 0
- 독립 negative review가 BCE/CE, 비유한·Foundation 범위 밖 Date, 잘못된 좌표, 상충 duplicate, compile-fail 검증 결함을 찾았고 보정 뒤 최종 `Ready`, 새 P0–P2 없음.

아직 구현하지 않음:

- PhotoLibrary source 연결과 실제 runtime 시간대 정책
- 위치 없는 사진의 실제 scan 유입
- 대표 사진 규칙
- `invalidDated`·`conflictingIDs`의 사용자 표현
- 지도 renderer·`+n`·실제 Journey 화면 전환
- catalog/RTree, persistence, Stage 3

## 실제 시간대 정책 검증 표본

- 상태: **사용자 제공 / metadata 추출 전**
- 2026-09-01, runtime 시간대 정책을 실제 사진으로 검증하는 맥락에서 우진: “아마 위치 찾아보면 일본 다녀온 사진이 있어서 추출하기 편할거야. 25년 8월쯤이야”
- 첫 실제 표본은 2025년 8월 전후의 일본 위치 사진과 시간상 인접한 무위치 사진을 함께 찾는다.
- 사진 원본은 외부로 보내지 않고 기기·로컬에서 `creationDate`, 위치 유무, 좌표, 촬영 간격만 분석한다.

## 2026-09-01 runtime 시간대 감사 결과

- 상태: **실기기 감사 완료 / 리드 정책 권고·독립 검토 Ready / 사용자 확인 대기 / 구현 전**
- DEBUG-only audit로 2025-06-01..<2025-11-01 image asset 825장을 읽었다: 위치 610, 무위치 215, screenshot 154. 원본·thumbnail·EXIF·asset identifier는 읽지 않았다.
- 0.5도 coarse 좌표의 offline 분석은 `Asia/Seoul` 422장, `Asia/Tokyo` 188장을 파생했다.
- 일본 direct anchor 사이의 무위치 사진 10장은 nearest located anchor가 앞뒤 모두 `Asia/Tokyo`였다. 최대 nearest-side gap 183.2분, 최대 total anchor span 958.4분이었다.
- 한국과 일본이 모두 UTC+09라 current-device와 capture-local 날짜 차이는 0장이었다. 이 표본은 neighbor 후보를 지지하지만 cross-offset 날짜 의미를 증명하지 않는다.

리드 최종 권고:

1. 사진별 capture-local day assignment와 evidence를 저장한다.
2. Journey 장면은 `LocalDay` 값이 아니라 시간순으로 한 번 발생한 local-day occurrence다.
3. `DayOccurrenceID`는 날짜·시간대·membership에서 계산하지 않는 persisted opaque UUID다.
4. split·merge·날짜 편집·권한 확장·policy migration은 silent regroup이 아니라 proposal·alias·tombstone으로 처리한다.
5. 같은 label의 occurrence 연결은 pairwise equality가 아니라 timezone-specific absolute day interval 전체의 running intersection으로 판단한다.
6. 사용자 override는 `(instant, timezone)` 또는 `(localDay, timezone, ordering relation)` 중 하나만 허용한다.

현재 코드 판정:

- `DayBucketPolicy.localDay(for:)`의 Gregorian·명시적 timezone·유효성 검사는 per-assignment helper로 재사용한다.
- catalog 전체에 timezone 하나를 적용하는 grouping API와 timezone-bearing `DaySceneGroupID`는 PhotoKit source integration 전에 교체한다.
- persistence는 stable identity의 선택 기능이 아니라 필수 경계다.

Consult의 6시간 one/two-sided anchor, device fallback, 2% 폐기선은 beta 가설로만 보존한다. 실제 cross-offset 보관함과 사용자 판정 전에는 제품 계약이나 출시 수치로 확정하지 않는다.

## 2026-09-01 capture-day occurrence 도메인 체크포인트

- 상태: **사용자 승인 / 구현됨 / 검증됨 / runtime 연결 전**
- 우진은 정책 권고 브리프 뒤 “ㄱㄱ”로 다음 순수 도메인 체크포인트 진행을 승인했다.
- 기존 `시간대+정책 지문+LocalDay` 계산형 `DaySceneGroupID` probe는 교체됐다.
- 현재 계약은 `사진별 capture-local assignment → 시간순 local-day occurrence → persisted opaque DayOccurrenceID`다.

구현:

- `DayCalendar`가 사진별 명시적 IANA 시간대와 Gregorian 달력으로 canonical day interval을 만든다.
- settled assignment만 occurrence membership이 될 수 있다. provisional·unresolved·undated·conflicting asset은 별도로 남는다.
- 같은 local-day label은 모든 timezone-specific day interval의 running intersection이 남을 때만 같은 occurrence가 된다.
- `DayOccurrenceID`는 날짜·시간대·정책·membership에서 파생하지 않고 materialization 때 발급·저장한다.
- instant override와 day-only `within/before/after`는 모순 없는 별도 형태다.
- 저장 provenance·current intersection·권한 상태를 기준으로 drift를 비교하고 silent regroup 대신 proposal을 만든다.
- transaction seam은 settled evidence, canonical day interval, origin anchor, intersection, 중복 사진·ID를 원자적으로 검증한다. 실제 저장소는 구현하지 않았다.

검증:

- day-scene host harness `515 PASS` (32 compile probes·13 source scans 포함)
- Journey `124 PASS`, photo-card `113 PASS`, metadata-audit `143 PASS`
- V2 clean simulator build와 기존 Maplog simulator build 성공, V2 first-party warning 0
- 독립 Sol negative review가 target source 등록, provisional membership, day-only ordering, provenance drift, current intersection, transaction authority, ID·evidence validation, canonical interval, neighbor bracketing과 guard-isolation fixture를 반복 보정한 뒤 최종 `Ready`

의도적으로 남긴 경계:

- production timezone resolver와 neighbor threshold
- 실제 persistence 저장소와 migration executor
- PhotoKit source integration
- unresolved/proposal 사용자 표현, 지도·Journey runtime, catalog/RTree, Stage 3