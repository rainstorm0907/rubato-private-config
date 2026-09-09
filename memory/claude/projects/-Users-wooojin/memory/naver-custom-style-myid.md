---
name: naver-custom-style-myid
description: "NAVER iOS 지도 SDK setCustomStyleId에는 styleId가 아니라 \"My Style ID\"를 넣어야 함"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8e432a29-07cb-4e31-9b36-76148c1789b5
---

Maplog에서 NAVER 커스텀 지도 스타일을 iOS SDK에 적용할 때, `setCustomStyleId`(빌드 설정 `MAPLOG_NAVER_CUSTOM_STYLE_ID`)에 넣는 값은 **Style Editor URL/목록 API의 `styleId`가 아니라**, 에디터 **My Style → 메뉴(⋮) → "My Style ID 확인"** 에 나오는 별도 **My Style ID**다. SDK가 이 값을 `styleMetadataId`로 `maps.apigw.ntruss.com/.../styler/props`에 질의함. styleId를 넣으면 HTTP 400 → 기본 스타일(`NAVERMAP_MoblieApp_FullRaster`)로 폴백.

**증거:** 2026-06-12 live 검증. styleId `e79be47a…` → 400 실패. My Style ID `b3899177…`로 교체 → `[maplog] naver custom style loaded` 성공, 픽셀색이 레시피와 일치. 발행(자동화/CORS 우회) 자체는 무관했고 ID만 문제였음. `map.pstatic.net/.../MobileApp_Open_conv.json` 404는 정상(SDK가 직접 읽는 경로 아님). 출처: iOS SDK 가이드 2-4 커스텀 스타일링.

3종 My Style ID·발행본·비교는 `record/design/2026-06-11_map_style_editor_worksheet.md` 2.6 참조. 관련 [[hama-portfolio-pdf-pipeline]] 같은 도구 함정 메모와 성격 동일.

**색 변경 제약(2026-06-12 추가):** 스타일 색은 에디터 클라이언트가 만드는 `mediator`에만 존재하고 `GET /style/content?style=mediator`는 405(PUT 전용). 서버는 발행본을 에디터 저장상태에서 재생성하므로 **발행본 GL을 API로 색치환해 POST해도 앱엔 반영 안 됨**. 색은 에디터 UI(빠른 스타일링 카테고리별 Hex)로만 바꿀 수 있고 그 UI 자동화는 불안정. 새 톤이 필요하면 Light/Dark 테마로 새 프로젝트 만들어 정식 발행하는 게 확실(Night Album 다크 `6fdcbd6d…`가 그 방식). 현재 채택: Twilight(warm) + Night(dark) 2종.
