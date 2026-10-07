---
description: Maplog legal notices live in the in-app settings sheet, not iOS Settings. The summary must not claim the whole app never sends a location.
---

## Conclusion

- Notices are an in-app screen, `LegalNoticesView`, opened from the settings sheet (⚙) by `NavigationLink("오픈소스·데이터 고지")` in `MapHomeChrome.swift`. They are not an iOS Settings pane.
- Full texts are read offline from the blue-folder `LegalNotices/` resources (`LegalNoticeCatalog.subdirectory`). The loader checks that subdirectory first, then a flat layout. A missing or whitespace-only file stays missing; it is not shown as an empty notice.
- The catalog is `LegalNoticeCatalog.all`: NAVER 지도 SDK, GRDB.swift, google-timeline-visualizer, ZoneDetect, SwiftTimeZoneLookup, timezone-boundary-builder 2026c, Natural Earth, 행정동 경계 (통계청 SGIS · admdongkor). Bodies stay in the bundle, byte-matched to the vendor originals, not pasted into Swift.
- The summary may say timezone lookup is on-device. It must not say the app never sends a location. The map is an online `NMFMapView`, so camera and tile requests leave the device. The current summary is the 해요체 paragraph in `LegalNoticeCatalog.summary`.

## Rationale

- Chose an in-app sheet because a signed build's `Settings.bundle` did not appear on the real iPhone. Settings → Maplog showed only Siri, Search, and Cellular Data.
- Rejected: `Settings.bundle` and `Root.plist` as the production surface. They were removed from the V2 target.
- Rejected as the current entry: a map-overlay `ⓘ` on `MapFeatureRootView`. The screen now pushes in from the settings sheet. The code comment still calls that overlay the old seat.
- Rejected: a summary that says the whole app does not send location. That sentence is false for the Naver map. Only the timezone calculation is offline.
- The sheet does not change map, renderer, or Journey behavior. URLs are shown as text and are not opened.

## Symptom

> “설정엔 보이지 않아”

> “ㅇㅇ 다해줘 그냥”

> “ㅇㅇ 다 보인다”
