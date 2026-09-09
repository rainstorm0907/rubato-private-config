---
description: 2026-09-05 Rubato oversized-session resume recovery and pre-push Git environment isolation incident, fixes, and removal conditions.
---
## 2026-09-05 oversized session resume

A persisted Sol session could not open because Senpi validated the full live history before constructing the TUI: target window 272,000, required 305,154, shortfall 33,154. The error advised `/compact`, but the user could not reach the command screen.

Resolution: official commit `58505dd7c` now skips the model-switch budget gate when resuming an existing session and adds broader resume paging/budget tests. The earlier public PR #6 was closed as superseded. The private `resume-recovery-register.mjs` shim was removed in private-config commits `ae731c4` and `8e32b60`; new sessions use only the official transform.

Runtime evidence: a copy of the previously rejected Sol session opened at 94% of 272K. A real Fable session copy opened on its stored Fable 5.1 model at 72% of 1M. Thus that sampled Fable session is safe, while the structural recovery applies to any model.

## Pre-push isolation incident

While pushing PR #6, the old `.githooks/pre-push` inherited Git's `GIT_DIR`/`GIT_WORK_TREE` environment into Stage 9. Temporary-repository tests then mutated the real shared repository, renamed the resume branch to `rubato/base`, created fixture worktrees/refs, and pushed fixture commit `b0c11df58` to the real origin `rubato/base`.

Recovery: force-with-lease restored GitHub and local `rubato/base` to `21777ffd5`; `core.bare` was restored to false; the resume branch/ref was restored to `231f690d5`; fixture worktrees and `memory/reflection-1` were removed. GitHub, local refs, and worktree metadata were revalidated.

Prevention: official commit `d32e35ee5` removed the slow pre-push gate entirely, so the leaking hook can no longer run. Public PR #5 was closed as superseded. As of official HEAD `5f3393e4d`, `/Users/wooojin/dev/Rubato` is clean and exactly matches `origin/rubato/base`.