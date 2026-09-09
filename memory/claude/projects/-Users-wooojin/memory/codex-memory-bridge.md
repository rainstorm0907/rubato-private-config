---
name: codex-memory-bridge
description: 코덱스 자동 메모리(~/.codex/memories/memory_summary.md)와 상호 참조 — 세션 시작 시 필요하면 읽기
metadata: 
  node_type: memory
  type: reference
  originSessionId: a87a3b3d-2107-4dc7-b8cd-e29491a12b20
  modified: 2026-08-13T09:35:21.697Z
---

코덱스(Codex CLI)에도 자체 자동 메모리 시스템이 있다: 세션을 로컬 파이프라인(sqlite jobs)으로 압축해 `~/.codex/memories/memory_summary.md`(~9KB)를 생성·주입한다. 원본 후보는 같은 폴더의 `raw_memories.md`·`MEMORY.md`(대용량 — 직접 읽지 말 것, [[session-analysis-pipeline]] 원칙 동일).

**How to apply:**
- 우진님 최근 활동 맥락(Maplog 진행, 시간표, 대회 등)이 내 메모리에 없으면 `~/.codex/memories/memory_summary.md`를 읽어 보충한다 — 코덱스 쪽이 더 최신일 수 있음.
- 역방향: `~/.codex/AGENTS.md`에 내 메모리 인덱스(MEMORY.md) 참조 섹션을 넣어둠(2026-08-13) — 코덱스 워커도 필요 시 내 메모리를 읽는다.
- 이 폴더는 자동 생성물(.git 관리) — **쓰기 금지**, 읽기 전용.
