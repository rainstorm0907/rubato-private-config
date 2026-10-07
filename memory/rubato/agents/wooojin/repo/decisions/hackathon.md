---
description: How hackathons and contests are run — proof spine, document structure, release verification.
---
Workflow for running hackathons and contests. Moved from `~/.codex/memories`. The result of Woojin deciding to combine Cofathon's freeze-and-reproduce discipline and KB AI Challenge's product narrative into one operating method.

It is the method agreed for use from the next contest on, so the lasting intent is strong, but it is kept as a conditional rule that turns on only in the "대회 참가 중" context.

## Proof spine

"한 줄 → 한 사용자 경로 → 한 코드 경로 → 한 검증 명령 → 한 제출 주장."

Start parallel expansion only after one input is actually connected through to a returned result.

## Three-layer document structure

- Personal skill
- Project documents: START_HERE / DECISIONS / CONTRACT / RELEASE
- AGENTS.md holds safety rules only

## Collaboration and release

- Independent worktree + integration owner + clean release worktree. GitHub is for milestone backup only. Integration is in 60~90 minute units.
- In the Release stage, **re-verify the exact submission ZIP in a new directory**: install / build / test / hero smoke / PDF render / claim-evidence.

## Past contest records

- Cofathon hiring perks (Krafton FDE and Olive Young AI engineer document screening passed) go only through TOP 3, so Woojin, who is TOP 6, is not eligible (Woojin 2026-10-01).
- The Cofathon Wanted AI hackathon award badge has been received (Woojin confirmed 2026-08-28: "원티드뱃지 이미 수령했어"). The related Wanted reply email was also sent on 8/5 — this item is closed.

- The KB AI Challenge final submission is `KB이음케어_우브라더스_제출_최종.zip` in the private `keepitmello/KB-hackaton` repository (commit confirmed 2026-08-03). A GitHub search has to include collaborator and organization repositories to find it.
- Morrow (Cofathon-Full-Mock-02) skin-compatibility verdict engine: `DECISION_THRESHOLD=50` and `NEGATIVE_EVIDENCE_THRESHOLD=0.12` were temporary values at the time and are not a final confirmation. Hold a judgment only for insufficient evidence; when positive and negative conflict, verdict as match/no-match and then show a warning. No overengineering, and do not arbitrarily add rules Woojin did not point out.
