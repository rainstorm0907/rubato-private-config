---
description: Maplog capture-day persistence is one file-based SQLite DatabaseQueue, default journal, no WAL. This file is not a work queue.
---
# Maplog V2 persistence foundation

## Conclusion

- The store is still one file-based SQLite `DatabaseQueue` per store, default delete journal, no WAL, `DatabasePool`, or observation (`SQLiteDayOccurrenceStore.swift`).
- PhotoKit, the map, and Recap are connected. Do not read the old checkpoint boundary below as a current lock. Product scope is `record/PRODUCT.md`.

## User boundary

Woojin directly asked not to narrow the frame in the next step either.

> “우리가 정한 엄격한 경계와 매몰되지 않는 시각을 유지하면서 진행해보자.”

> “특히 너가 직접 구현하는게 아니니까 조금 더 한 차원 뒤에서 봐줘야해.”

Rejected as a current stop: locking PhotoKit, the timezone resolver, the map renderer, and Recap behind this persistence checkpoint. That was the cut for the day persistence landed, not a standing ban.

## Chosen layer

- exact `GRDB 7.11.1`
- file-based SQLite
- a single `DatabaseQueue` per store
- default delete journal
- no WAL, `DatabasePool`, or observation

Core Data, SwiftData, and SQLite3 all worked on the macOS host. A host-harness advantage was not grounds for the choice. Direct SQLite3 was excluded because, while it uses the same engine, the project would have to own the C statement lifecycle, binding, migration, queue, and error translation itself. SwiftData/Core Data were excluded because ORM identity, change tracking, and opaque migration would put a second state machine on top of an already complete pure `validatedApply`.

## Verified storage contract

- opaque `DayOccurrenceID`
- the members of an occurrence's first materialize, and the unavailable bit at that time
- current assignment membership
- evidence, provenance, and user override
- assignment and occurrence exact interval
- origin unavailable
- day-only relative ordering
- the stored source of truth needed for reconciliation

An exact transaction replay is a no-op success of 0 rows and an unchanged writer generation. Partial, duplicate, and altered replays, and conflicting ID reuse, are rejected. An exact no-op from a stale instance also fails as `staleWriter`.

An occurrence and assignment delta, origin-unavailable propagation, and the writer-generation increase are all applied in one SQLite transaction or all rolled back. Commit, load, reload, and export on the same store serialize the cache and generation together with the DB transition.

A migration the app does not know, a wrong migration prefix, a newer schema generation, an unsupported payload version, metadata corruption, a broken foreign-key or cross-record relationship, a relative-order cycle, a record decode failure, and physical file corruption are not turned into an empty snapshot. A new empty store is valid only when there is no application schema or data.

A host measurement of a large synthetic library is not a release threshold. PhotoKit and the map are connected. Do not treat "source not connected yet" as current. Product scope is `record/PRODUCT.md`.
