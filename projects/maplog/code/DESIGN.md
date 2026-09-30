# Maplog Design Contract

**현재 적용 안내 (2026-09-29):** 먼저 [CURRENT](../record/CURRENT.md)와 [PRODUCT](../record/PRODUCT.md)를 읽는다. 아래의 모임 중심 정체성·고정 토큰은 6~7월 옛 앱(`code/Maplog/`)의 디자인 자산 기록이며 새 제품 정의를 덮지 않는다. 관련 화면의 이유와 보호할 경험에 맞는 부분만 재사용하고, 과거 화면 계약·검사 통과를 새 표현의 채택으로 승계하지 않는다. 친구·모임 기능은 이번 출시에 없다([PRODUCT 이번 출시에서도 안 하는 것](../record/PRODUCT.md#not-this-release)).

**9/24 갱신:** 한 화면의 정보량은 최소로 둔다(사용자 확정, 아래 6장 10항과 [PRODUCT 화면 규칙](../record/PRODUCT.md#screen-rule)). Recap 탭(기간 모음)은 어두운 사진 감상 표면(Ambient Dark)이다. 아래 2장의 밝은 방향은 지도·앨범 화면 기준이고, Recap 탭 합의는 [PRODUCT Recap 모음 화면](../record/PRODUCT.md#recap-collection)을 따른다.

이 문서는 관련 디자인 자산과 세부 계약을 찾는 입구다. 특정 화면의 수치와 과거 QA 이력은 필요한 범위에서만 읽는다.

## 읽는 순서

1. 현재 상태·승인·잠금은 [`record/CURRENT.md`](../record/CURRENT.md)를 봅니다.
2. 제품 정체성·감성·보호 조건·열린 판단은 [`record/PRODUCT.md`](../record/PRODUCT.md)를 봅니다.
3. 지금 유효한 사용자 결정은 PRODUCT에 있고, 6~9월의 흐름은 [RETRO](../record/RETRO.md)에 요약돼 있습니다.
4. 이 문서의 기존 디자인 방향 중 현재 목적에 맞게 재사용할 부분을 확인합니다. 현재 사용자 결정과 충돌하면 원문·상태부터 대조합니다.
5. 승인된 UI 작업에서 아래 trigger에 해당하는 세부 계약을 읽되, 옛 기능을 자동 재개하지 않습니다.

| 건드리는 범위 | 반드시 읽을 계약 |
| --- | --- |
| 색·글꼴·radius·depth·glass·motion token | [`design/visual-system.md`](design/visual-system.md) |
| 지도 홈·사진핀·선택 상태·map overlay | [`design/map-home-and-photo-pins.md`](design/map-home-and-photo-pins.md) |
| 사진 선택·grouping·location segment·cover·album flow | [`design/import-and-album-flows.md`](design/import-and-album-flows.md) |
| 하단 navigation·로컬 앨범 탐색 | [`design/navigation-and-album.md`](design/navigation-and-album.md) |
| 여러 화면을 가로지르는 정보 계층·표면·행동·공용 UI | [`design/app-wide-design-language.md`](design/app-wide-design-language.md) |
| Recap 탭(기간 모음)·Recap 카드 | [PRODUCT Recap 모음 화면](../record/PRODUCT.md#recap-collection) + [`design/app-wide-design-language.md`](design/app-wide-design-language.md) |
| 사용자 확정사항이나 제품 전략을 바꿀 가능성 | [PRODUCT](../record/PRODUCT.md) |
| 과거 결정 근거나 회귀 여부 | git 기록의 옛 작업 일지(2026-09-29 정리로 지움) 중 필요한 것 하나 |

한 변경이 여러 화면을 가로지르거나 shared token·data meaning을 바꾸거나 현재 artifact와 충돌하면 인접한 세부 계약도 구현 전에 읽습니다.
6. 수치의 채택 근거와 실행 증거가 필요할 때만 QA 폴더나 git 기록에서 찾습니다.

문서보다 현재 코드가 구현 수치의 단일 출처인 경우 코드가 우선합니다. 문서와 코드가 의미 수준에서 충돌하면 조용히 섞지 말고 차이를 드러냅니다.

## 1. Product Identity

> 조용한 지도 위에 친구 모임 사진이 작은 유리 스티커처럼 붙는 지도앨범 앱.

Maplog는 기존 갤러리 사진을 고르면 과거 추억이 지도 위에 바로 펼쳐지고, 이후 친구들과 모임 사진을 간편하게 함께 쌓는 비공개 지도앨범입니다.

사용자가 느껴야 할 것:

- `어? 여기 갔었지`
- `사진첩보다 찾기 쉽다`
- `지도 위에 추억이 붙어 있다`
- `귀찮지 않은데 예쁘다`

Maplog가 아닌 것:

- 공개 피드 중심 SNS
- 여행 플래너나 장소 토론 채팅
- 실시간 위치추적 앱
- 꾸미기 중심 다이어리
- 네이버지도 복제품

주요 진입 뒤 홈에서는 권한과 사용 가능한 데이터가 허용하는 가장 이른 시점에 실제 지도와 사용자 사진을 만납니다. empty·permission·failure 상태는 없는 콘텐츠를 가장하지 않고 목적에 맞는 대안을 보여줄 수 있습니다. 지도는 기억을 받쳐주는 조용한 바닥이고, 사진은 주요 기억 콘텐츠이므로 map chrome·label·control·decoration이 지속적으로 사진보다 강해지지 않습니다.

## 2. Current Visual Direction

현재 채택된 방향은 `시크하고 세련된 새 iPhone 기본앱 감성`입니다.

- calm, bright, photo-first, warm white, quiet Korean map
- native control behavior와 읽기 쉬운 soft glass
- 작은 coral/pink accent와 warm ink
- 스케치 감성은 얇은 선, wordmark, 작은 marker 디테일에만 제한
- 귀여움은 핀 꼬리, 작은 반응, 빈 상태처럼 좁은 곳에서만 사용

화면은 맑고 바로 조작할 수 있어야 합니다. 병원·금융앱처럼 차갑거나, 꾸민 다이어리·카페 템플릿·AI glassmorphism처럼 보이면 현재 방향에서 벗어난 것입니다.

구조 제목은 실제로 여러 콘텐츠를 묶을 때만 둡니다. 제목·본문·배지·꼬리말이 같은 뜻을 반복하지 않으며, 사용자가 눌러야 할 주 행동·보조 행동·파괴 행동과 결정에 필요한 조건을 낮은 대비 설명문보다 먼저 읽히게 합니다. 직관은 설명을 더 붙이는 것이 아니라 구역과 시각적 무게로 만듭니다.

현재 앱 전체 디자인 언어의 기준은 사진이 깔린 메인 지도와 기간 Recap(모음·재생)입니다. 앞은 지도 위 사진을 둘러보는 밝은 표면, 뒤는 사진을 감상하는 어두운 표면(Ambient Dark)을 대표합니다. 7월의 `모임 상세 추억 타임라인`·`멤버 초대 sheet` 기준은 옛 앱 기록입니다. 다른 화면은 배치를 복사하는 대신 [`app-wide-design-language.md`](design/app-wide-design-language.md)의 콘텐츠 우선순위·정보 계층·행동 문법을 자기 목적에 맞게 적용합니다.

기준 이미지: `/Users/wooojin/Downloads/생성된 이미지 3.png`

## 3. Fixed, Flexible, Exploratory

모든 문장은 같은 강도의 규칙이 아닙니다. 변경 권한과 필요한 검증 수준에 따라 아래처럼 구분합니다.

### Fixed

`Fixed`는 비판할 수 없는 영구 진리가 아니라, 변경 권한이 현재 작업에 위임되지 않은 항목입니다. 반대 근거가 있으면 영향·근거·migration 범위를 갖춘 제안으로 올릴 수 있지만 사용자 확인 없이 구현을 바꾸지 않습니다.

- 제품 약속: 지도앨범이라는 정체성, 비공개 기본값, 주요 진입 뒤 실제 지도와 사용자 사진을 가능한 이른 시점에 보여주는 경험
- 플랫폼·상호작용 계약: native Naver map gesture·camera behavior, marker가 지도 좌표에 붙는 의미
- 안전 불변조건: 선택한 사진 범위, 접근성, 개인정보, data semantics
- 명시적 사용자 결정: `record/PRODUCT.md`에 `사용자 확정`으로 적힌 결정

Native marker의 radius·scale·stack 표현 같은 시각 파라미터는 Fixed 자체가 아니라 아래 Flexible 계약입니다.

### Flexible

현재 구현의 일관성을 위해 우선 따르되, 실제 화면 근거가 있으면 조정할 수 있습니다.

- 시각 표현: 색상·타이포 처리·radius·depth·카드 구성·간격·지도 라벨과 사진핀의 광학적 대비
- 조정 가능한 행동 수치: zoom·hit geometry·marker scale·selection expansion·motion timing

시각 표현은 현재 화면과 비교합니다. 행동 수치는 interaction, accessibility, occlusion, data meaning 영향을 함께 확인합니다. Shared SSOT나 화면 간 계약을 바꾸면 구현 SSOT와 세부 계약을 맞추고 재사용 가치가 있는 근거를 worklog에 남깁니다. 단일 화면의 local padding 같은 광학 보정은 별도 이력 문서가 필요하지 않습니다.

### Exploratory

새 화면, 홍보 웹, 리캡 테마, 사용자가 명시적으로 요청한 리디자인에서는 자유롭게 제안할 수 있습니다.

- 새로운 구성, 이미지 언어, 전환, 타이포 조합
- 현재 토큰을 확장하거나 대체하는 시각 방향
- 익숙한 패턴과 표현적인 패턴 중 제품 목표에 맞는 선택

탐색은 기존 장식을 무작위로 섞는 일이 아닙니다. 대상 사용자, 전달할 메시지, 기억에 남을 아이디어 하나를 정하고 실제 렌더로 비교합니다. Fixed 항목을 바꾸는 안은 구현하지 않고 제안으로 명시합니다.

## 4. Visual System

현재 토큰은 구현 호환성을 위한 기본값이며 보편적 미감 규칙이 아닙니다.

정확한 radius, shadow, motion, glass fallback 수치는 [`design/visual-system.md`](design/visual-system.md)에 둡니다. 토큰 작업이 아니라면 이 snapshot을 미리 읽을 필요가 없습니다.

### Color

- surfaces: `mapPaper #F8F4EC`, `surface #FFFDF9`, `surfaceGlass #FFFFFFCC`
- text: `ink #191817`, `inkSoft #4B4945`, `caption #7B7770`
- lines: `hairline #D8D0C4`, `hairlineStrong #B9AA99`
- accents: `memoryPink #EF7898`, `softCoral #F28B72`, `warmGold #E7B84D`
- map context: `parkSage #A9C59B`, `waterMist #CFE8EE`, `stationBlue #5D8DD7`
- semantic: `success #65A77A`, `warning #D9A441`, `danger #D96A5E`

넓은 면은 warm surface가 맡고 accent는 선택 상태와 핵심 행동에 집중합니다. 색 수를 기계적으로 제한하기보다 한 화면에서 무엇이 주도색인지 분명하게 만듭니다.

### Typography

iOS 시스템 폰트와 SwiftUI 기본 San Francisco 계열을 사용합니다. 한국어 본문에는 손글씨 폰트를 쓰지 않고, 별도 wordmark가 필요할 때만 브랜드 표현을 탐색합니다. 화면의 정보 단계는 콘텐츠가 한눈에 읽힐 만큼만 둡니다.

### Surface and Motion

- 사진, 지도, 기본 콘텐츠에는 glass를 씌우지 않습니다.
- glass는 top controls, 주요 추가 버튼, 선택 카드, sheet·tab navigation처럼 조작 계층에 사용합니다.
- glass가 글자를 흐리게 만들면 opacity를 높이거나 solid surface로 바꿉니다.
- motion은 상태 변화와 공간 관계를 설명해야 하며 지도 pan·zoom·rotate 동기화보다 앞설 수 없습니다.
- Reduce Motion과 Reduce Transparency에서 의미와 조작성이 유지되어야 합니다.

## 5. Interaction and Accessibility

- 현재 활성 surface가 입력을 소유하고 배경 gesture와 scroll을 일관되게 처리합니다.
- 지도핀 선택, 빈 곳 탭 해제, 상세 진입은 세부 계약과 실제 상태가 같은 의미를 보여야 합니다.
- 주요 touch target은 최소 44pt를 유지합니다.
- Dynamic Type, VoiceOver, 대비, reduced motion, reduced transparency를 affected flow에서 확인합니다.
- mock map과 live map은 가능한 한 같은 marker renderer와 상태 의미를 공유합니다.
- 실제 참여자·공개 범위·장소 공급자가 없을 때 가짜 production 데이터를 표시하지 않습니다.
- 대표사진 선택은 일반 설정 form이 아니라, 사용자가 고른 **한 장**이 실제 지도핀의 첫 카드로 들어가는 짧은 경험이어야 합니다. 뒤 카드는 위치·촬영시간 규칙으로 자동 구성하며, user-facing slot·순서 조립 UI는 두지 않습니다. hand fan·motion의 구체 계약은 [`design/import-and-album-flows.md`](design/import-and-album-flows.md)를 따릅니다.
- 친구 초대는 주소록을 수집하는 검색 화면이 아니라, 초대자 정체·상호 수락·참여 모임 경계를 먼저 읽게 하는 짧은 카드 경험이어야 합니다.

## 6. Design Working Agreement

디자인 작업에서는 이 문서를 스타일 생성 공식으로 쓰지 않습니다.

1. 현재 artifact와 실제 콘텐츠를 먼저 봅니다.
2. 새 화면이나 의미 있는 재구성은 `누가 / 무엇을 하려는지 / 주 행동 / 성공 신호`를 한 문장씩 먼저 적습니다. 화면에서 이 경로와 관계없는 요소는 만들지 않거나 약하게 둡니다.
3. 로그인·친구·공유·사진 선택처럼 이미 성공한 소비자 앱의 관습이 있는 화면은 실제 동종 앱 1~3개와 iOS 기본 패턴을 확인합니다. 브랜드 외형을 복사하지 않고 정보 계층·행동 수·피드백 방식을 Maplog 언어로 번역합니다. 이미 확정된 Maplog 컴포넌트를 그대로 재사용하는 작은 수정은 같은 조사를 반복하지 않습니다.
4. Fixed 항목과 이번 작업에서 열려 있는 선택을 구분합니다.
5. 결정이 high-impact이고, 요구가 실질적으로 덜 정해졌으며, 비교 렌더 비용이 낮을 때만 두 방향을 비교합니다. 그 외에는 가장 잘 맞는 한 방향을 선택해 구현합니다.
6. 표현적이거나 정체성을 담당하는 화면은 한 가지 authored visual idea를 유지합니다. Utility 화면은 clarity, continuity, state completeness를 우선합니다.
7. 구현 뒤 target viewport에서 진입 → 주 행동 → 결과·오류·복구를 실제로 걷고, 코드가 아니라 렌더 결과를 비평합니다. 마지막에는 보이는 모든 요소가 사용자 행동에 필요한지 한 번 덜어냅니다.
8. 가입·개인정보·결제·공유처럼 고위험 화면이나 위임 구현은 가능할 때 구현 맥락을 모르는 fresh-eyes 검토를 추가합니다. 독립 검토를 못 했으면 자체 렌더 검토와 구분해 기록합니다.
9. 직관을 높인다는 이유로 제목을 소제목·본문·배지·꼬리말에서 반복하지 않습니다. 사용자가 결정하거나 행동하는 데 필요한 조건은 작은 회색 문단에 숨기지 않고, 실제 구역·항목·행동의 시각적 무게로 드러냅니다.
10. 한 화면의 정보량은 최소로 둡니다(사용자 확정 2026-09-24, [PRODUCT 화면 규칙](../record/PRODUCT.md#screen-rule)). 문제를 풀 때 요소를 더하기 전에 기존 요소의 무게·자리로 풀 수 있는지 보고, 보여주기 전에 한 화면에서 읽을 글씨·아이콘·사진 수를 세어 이전 판과 비교합니다.

시스템 폰트, 대칭, 절제, 익숙한 레이아웃도 맥락에 맞으면 좋은 선택입니다. 반대로 custom type, 비대칭, overlap, texture, 강한 motion도 제품과 메시지가 비용을 정당화하면 사용할 수 있습니다. `AI 티 제거`를 이유로 어느 쪽도 자동 선택하지 않습니다.

## 7. Completion Gate

디자인 구현을 완료했다고 말하기 전에 다음 중 이번 변경에 해당하는 항목을 관찰합니다.

- target device 또는 viewport의 렌더 결과
- 기본·선택·빈·로딩·오류·권한 상태 중 영향받은 상태
- 긴 한국어, 작은 화면, Dynamic Type과 text clipping
- 지도 gesture와 native marker 동기화
- glass 위 가독성, focus/VoiceOver, reduced motion/transparency
- mock과 live behavior의 의미 일치

빌드 성공만으로 화면 품질을 완료 처리하지 않습니다. 비교 근거와 남은 한계는 QA 폴더(`/Users/wooojin/Downloads/maplog-qa/`)에 남깁니다.
