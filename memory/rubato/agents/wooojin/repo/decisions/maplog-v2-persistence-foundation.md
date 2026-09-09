---
description: 2026-09-01 Maplog V2 capture-day occurrence persistence foundation의 구현·검증 결과, 저장 계약, 100k 측정과 잠긴 후속 범위.
---
# Maplog V2 persistence foundation

날짜: 2026-09-01

상태: **구현됨·검증됨 / 독립 P0–P3 closure `Ready` / runtime source 연결은 사용자 확인 대기**

## 사용자 경계

우진은 다음 단계에서도 프레임을 좁히지 말라고 직접 요청했다.

> “우리가 정한 엄격한 경계와 매몰되지 않는 시각을 유지하면서 진행해보자.”

> “특히 너가 직접 구현하는게 아니니까 조금 더 한 차원 뒤에서 봐줘야해.”

그래서 persistence만 구현했고 PhotoKit source, production timezone resolver·neighbor 수치, 지도 UI·renderer, Journey runtime, catalog/RTree, split/merge executor·alias/tombstone lifecycle, Stage 3은 잠갔다.

## 선택한 계층

- exact `GRDB 7.11.1`
- 파일 기반 SQLite
- store당 단일 `DatabaseQueue`
- 기본 delete journal
- WAL·`DatabasePool`·observation 없음

Core Data·SwiftData·SQLite3는 macOS host에서 모두 동작했다. host harness 우위는 선택 근거가 아니었다. direct SQLite3는 같은 엔진을 쓰면서 C statement lifecycle, binding, migration, queue와 오류 변환을 프로젝트가 직접 소유해야 해서 제외했다. SwiftData/Core Data는 ORM identity·change tracking·opaque migration이 이미 완결된 pure `validatedApply` 위에 두 번째 상태 기계를 얹어 제외했다.

## 검증된 저장 계약

- opaque `DayOccurrenceID`
- occurrence 최초 materialize 구성원과 당시 unavailable bit
- 현재 assignment membership
- evidence·provenance·user override
- assignment·occurrence exact interval
- origin unavailable
- day-only relative ordering
- reconciliation에 필요한 저장 정본

정확한 transaction replay는 0행·writer generation 불변의 no-op 성공이다. 일부·중복·변형 replay와 conflicting ID reuse는 거절한다. stale instance의 exact no-op도 `staleWriter`로 실패한다.

Occurrence·assignment delta, origin unavailable 전파, writer generation 증가는 한 SQLite transaction에서 전부 반영되거나 전부 롤백된다. 같은 store의 commit/load/reload/export는 cache·generation과 DB 전이를 함께 직렬화한다.

앱이 모르는 migration, 잘못된 migration prefix, newer schema generation, unsupported payload version, metadata 손상, foreign key·cross-record 관계 손상, relative-order cycle, record decode 실패와 물리 파일 손상을 빈 snapshot으로 바꾸지 않는다. 새 빈 store는 application schema·data가 없을 때만 유효하다.

## 최종 검증

- persistence harness: `219 PASS`, exit 0, warnings-as-errors
- day-scene: `516 PASS`, exit 0
- Journey: `124 PASS`
- photo-card: `113 PASS`
- metadata-audit: `143 PASS`
- V2 clean simulator build: 성공, first-party warning 0
- 기존 Maplog clean simulator build: 성공
- exact GRDB pin 추가 외 기존 NMapsMap·Supabase pin 불변
- 독립 Sol negative review: P0–P3 없음, 최종 `Ready`
- write fence 밖 변경 없음

## 최종 synthetic 측정

각 tier를 별도 process에서 실행하고 seed store를 해제한 뒤 cold reopen했다. 출시 임계값이 아니다.

| assets | cold reopen + load | post-load RSS | process peak RSS | DB |
|---:|---:|---:|---:|---:|
| 10,000 | 0.231초 | 48.3MB | 61.7MB | 5.8MB |
| 50,000 | 1.271초 | 93.3MB | 262.0MB | 28.8MB |
| 100,000 | 2.685초 | 273.1MB | 505.5MB | 57.7MB |

100,000장에서 non-origin unavailable은 1행·0.014초, origin unavailable은 2행·0.014초였다. 100회 작은 commit p50/p95/max는 0.027/0.043/0.056초, deterministic export는 1.348초·48.3MB였다.

## 남은 관문

100,000장 post-load RSS 273.1MB와 process peak 505.5MB는 실제 iPhone 합격선으로 해석하지 않는다. 다음 source 연결 전에 출시 대상 iPhone에서 memory·startup을 다시 측정할 계획을 먼저 합의한다. 실제 v1→v2 migration은 아직 존재하지 않으며 현재는 `v1-initial`과 실패·미래 schema 경계만 검증했다. 실제 resolver·PhotoKit source·UI/runtime은 연결하지 않았다.

프로젝트 정본: `/Users/wooojin/App/maplog/record/v2/PRODUCT.md`, `/Users/wooojin/App/maplog/record/v2/CURRENT.md`, `/Users/wooojin/App/maplog/record/v2/FOLLOWUPS.md`.