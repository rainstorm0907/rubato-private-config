---
description: Maplog V2 production resolver 법적 고지 표면을 Settings.bundle에서 인앱 정보 sheet로 바꾸기로 한 사용자 승인과 구현 상태.
---
# Maplog V2 법적 고지 표면

- 날짜: 2026-09-02
- 맥락: signed V2 앱에는 `Settings.bundle`과 license 파일 4개가 포함됐지만, 실제 iPhone의 설정 → Maplog 화면에는 Siri·검색·셀룰러 데이터만 보였고 custom notice는 표시되지 않았다. 우진도 직접 “설정엔 보이지 않아”라고 확인했다.
- 원래 방향: V2 전용 시스템 설정 pane에서 ZoneDetect·SwiftTimeZoneLookup·timezone-boundary-builder 2026c ODbL·Natural Earth 고지를 노출한다.
- 변경 방향: `MapFeatureRootView`의 기존 overlay 층에 작은 `ⓘ` 진입점을 두고, 지도·renderer·Journey 동작을 바꾸지 않는 독립 인앱 고지 sheet에서 attribution과 전체 license text 4개를 오프라인으로 읽게 한다. 검증 뒤 dead `Settings.bundle` surface는 제거한다.

우진 승인 원문:

> “ㅇㅇ 다해줘 그냥”

구현·검증 결과:

- `MapFeatureRootView`의 safe-area 안에 44×44 `info.circle` 진입점을 두고 `오픈소스 및 데이터 고지` native sheet를 연결했다.
- ZoneDetect, SwiftTimeZoneLookup, timezone-boundary-builder 2026c ODbL, Natural Earth 네 전문은 vendor 원본과 byte-identical한 `LegalNotices/*.txt`를 오프라인으로 읽는다.
- 실제 Release bundle이 blue-folder `LegalNotices/` 경로를 보존하므로 production loader도 그 subdirectory를 먼저 찾는다. nested·flat·missing·whitespace Bundle과 승인 summary 전체 문자열을 focused test로 고정했다.
- 실제 iPhone 설정에서 보이지 않던 `Settings.bundle`과 `Root.plist`는 V2 target에서 제거했다.
- 2026-09-02 signed app을 기존 bundle 위에 설치한 뒤에도 occurrence 7개, assignment 187개, Journey 4개가 복원되고 `skipped-existing`으로 끝났다. 설치 전후 SQLite SHA-256은 `3079725ef81e21b0e26eb4f7a654445ce9266f9eb9b1fd10d4c374250867337d`로 byte-identical했다.

실기기 확인 원문:

> “ㅇㅇ 다 보인다”

맥락: 2026-09-02, iPhone 14의 지도 오른쪽 위 `ⓘ`를 열고 네 고지 항목 전문이 모두 보이는지 확인한 뒤의 답.

상태: **사용자 확정 / 구현됨 / 독립 검토됨 / 실기기 검증됨**.