---
description: 2026-09-17 disk at 100% → Rubato session "Disk I/O error" → cause, recovery procedure, and recurrence prevention of the three-layer incident up to the record chain breaking.
---
---
description: 2026-09-17 disk at 100% → Rubato session "Disk I/O error" → cause, recovery procedure, and recurrence prevention of the three-layer incident up to the record chain breaking.
---
# When the disk fills, the session record chain breaks (2026-09-17)

Status: cause confirmed · recovery in progress. Maplog lead session `01a0a908-083f-708f-b820-7437cf1b6e39` (app thread `a62e4f8a-cfbe-4c03-8c10-de13734280d3`, gpt-6-astra xhigh).

## Symptom and misdiagnosis

After "Worked for 1.0s" in the app, `Disk I/O error` repeated for 3 lines. It looked like 9 and a half hours of work in progress, but in fact every turn was `stopReason: aborted` in 350ms, with 0 tokens.

## Three-layer causes

1. **Disk at 100%** — 430MB free. The culprit is `~/Downloads/maplog-qa` at 20GB, of which `2026-09-16-recap-connected-motion/runs/` is 7.6GB. The QA script (`capture_runs.py:61`) left a 122-second `full.mov` of 320MB on every attempt, 7GB over 23 rounds in one night.
2. **The SQLite connection froze** — Even after freeing space, the pi-server that had been up for 20 hours kept the poisoned connection. Restarting the app cleared it.
3. **The session record chain broke (the real cause)** — ENOSPC meant one line, entry `3e0bec63`, was not written, and the next line `a57b85b8` points at a parent that does not exist. Following ancestors from the leaf breaks after 24 lines and never reaches the compaction and context-window records → context-notes extension init fails → `새 문맥 관리 확장이 준비되지 않았어요. 요약 방식으로 전환하지 않고 요청을 중단했어요.`

The third is the core. Stopping instead of quietly switching to summary mode is the correct behavior as designed (if it had gone through, 9 hours of context would have silently vanished).

## How to diagnose

- A session jsonl is a linked tree of `id`/`parentId`. Read the whole thing and count `parentId not in ids`, and the break shows up immediately. Comparing the chain length from leaf to root with the total entry count is the same verdict.
- Pinning the failure point was narrowed in this order: confirm the open DB with `lsof -p <pi-server>` → `pragma quick_check` on each sqlite → `errorMessage` at the end of the session jsonl.
- Grep the original error wording in `~/.rubato-pi/stock-engine` and it goes straight to the code for the condition (`context-notes/engine-gate.mjs`, `extensions/context-notes.mjs`).

## Recovery

Set the broken line's `parentId` back to the id of the last intact entry. Both ids are 8 characters, so **the byte length is the same** and an in-place overwrite is possible (temp+rename is dangerous because the server has the file open and is appending). Keep the original as `.bak-<날짜>-chainfix`.

```python
with open(p,'r+b') as f:
    f.seek(off); assert f.read(8)==b'3e0bec63'
    f.seek(off); f.write(b'09c6ee14')
```

**After fixing the file, always restart the app/pi-server.** The server caches the session tree in memory, so fixing only the file keeps producing the same error. This time the order was reversed (restart → file edit) and one attempt spun for nothing.

## Preventing recurrence (Open)

- Fix the QA script to delete `full.mov` after the verdict. If not, 9.7GB is 30 rounds, so the disk bottoms out again in a day and a half.
- Remaining cleanup candidates: past session videos in `maplog-qa` (09-14 2.7G, 09-16-evidence-loop 2.0G, 09-16-reactive 1.5G), and old session and log DBs in `.codex`.
