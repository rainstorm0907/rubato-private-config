---
description: 비행운(Maplog) 화면 시안·레퍼런스 작업에서 실제로 통한 도구 경로(2026-09-29): Dribbble 수집, 이미지 생성, HTML 시안 렌더, 네이버 지도 제약
---
# 비행운 시안 작업 도구 (2026-09-29 확인)

- 레퍼런스: App Store 스크린샷(iTunes Search API)은 사용자가 "부족하다"고 봤다. Dribbble 검색 결과는 `abrowse`로 `li.shot-thumbnail` img src를 뽑아 CDN(`cdn.dribbble.com/userupload/...?resize=800x600`)에서 받는 방식이 됐다. Pinterest는 로그인 벽. Aside `exec` 긴 조사는 가짜 이미지 주소를 돌려줘서 버렸다.
- 이미지 생성: 세션의 `generate_image` 도구는 400("unknown image parameter stream")으로 실패했고, `gti --provider private-codex --model gpt-5.5 --prompt ... --output ...`가 됐다. 구름 소재는 검은 배경으로 만들고 밝기→알파로 바꿔 투명 PNG로 썼다.
- 시안: HTML/CSS를 Chrome headless(`--force-device-scale-factor=2 --window-size=402,874 --screenshot`)로 렌더하고 PIL로 비교판을 붙였다. 예: `/Users/wooojin/Downloads/maplog-qa/2026-09-29-card-style/v2/gen*.py`. 배경으로 쓰는 앱 캡처에 옛 카드·디버그 칩이 박혀 있지 않은지 먼저 본다.
- 네이버 지도: 지도 캡처를 앱에 이미지로 넣는 건 약관(결과 저장·가공·배포 금지)에 걸린다. 앱 안 그림은 손으로 못 움직이는 실제 지도 + 오버레이로. 지하철 노선은 SDK 층 끄기로 안 사라지고 스타일 편집기(사용자 계정)가 필요하다.
- 화면 디자인 원칙은 [[decisions/maplog-screen-design-by-purpose.md]]와 저장소 `record/PRODUCT.md` 화면 규칙.
