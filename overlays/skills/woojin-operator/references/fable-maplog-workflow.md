# Fable Maplog Workflow Pattern

Use this reference when Woojin asks to reproduce, inspect, compare, or learn from the strong Fable-style workflow from the 2026-07-04 Maplog session. Treat it as evidence from one successful session and a menu of reusable moves, not as the default sequence for every Maplog or product-feel task.

## Evidence Snapshot

Primary local artifacts:

- `/Users/wooojin/.claude/projects/-Users-wooojin/6c1979d3-7a88-4e72-a96d-8215fd12bec4.jsonl`
- `/Users/wooojin/App/maplog/record/worklogs/2026-07-04_worklog.md`
- `/Users/wooojin/App/maplog/record/research/2026-07-04_karrot_map_review.md`
- `/Users/wooojin/App/maplog/record/design/2026-07-04-alive-review-evidence.md`

Outcome commits:

- `071005f` / `08a2977`: automatic photo clustering, batch approval, first-screen density, worklog/screenshots.
- `bd50dae` / `4d41ec1`: decoden recap card renderer, design/research artifacts, output snapshots.
- `86e7764` / `9a375df`: map-alive package, Karrot review, demo videos, evidence docs.

## What Fable Did Well

Fable treated Woojin's input as product intent, not just tickets:

- "딸랑 1핀" became the product gap `first-screen density`, solved by clustering plus batch approval.
- "Z세대 공유 카드" became a research-backed visual grammar, not a generic poster.
- "당근처럼 부드러움" became observable mechanics: gesture-time mini pins, idle promotion, spotlight/recall bubble, stack pins.

The workflow repeatedly used this chain:

```md
handoff/source artifact
-> current code contracts
-> product gap
-> external/reference decomposition
-> scoped implementation package
-> runtime screenshot/video evidence
-> independent review
-> fix/verify
-> worklog/handoff
```

## Reusable Moves

### 1. Product-Gap Reframing

Before implementation, restate the gap in product terms:

- literal request: "여러 장 사진 자동 클러스터링"
- product gap: "지도에 주인공이 없어 보이는 first-screen density failure"
- implementation package: clustering engine + approval sheet + camera fit + multi-pin seed + QA screenshots

Do this only when the user's language signals product feel, market fit, sharing, recap, density, smoothness, or "뭔가 별로".

### 2. Taste-To-Mechanics Translation

When the user gives taste words or examples, convert them into mechanics:

- "듬뿍", "키캡 키링", "데코덴" -> full-cover density, die-cut outline, charm hierarchy, constrained palette.
- "당근처럼 자연스럽게" -> gesture/idle states, zoom/center trigger, delayed promotion, one-at-a-time spotlight.
- "겹친상황" -> stack pins, not random displacement.

Keep the user-facing reply short, but make the implementation plan mechanical.

When a broad creative direction remains uncertain, explore concrete mechanics first, then add a Woojin taste checkpoint before committing. Treat taste uncertainty as evidence to resolve, not as a reason to avoid proposing options.

### 3. Bounded Fan-Out

Use parallel research or review only when independent branches would materially improve speed, coverage, or confidence:

- market/strategy evidence
- visual grammar/reference evidence
- technical feasibility
- independent code review

Each branch must have a narrow brief, source priority, non-goals, and a concise return format. Do not fan out just to look busy.

### 4. Proportional Verification

For risky Maplog or product-quality work, build success is not enough. Choose verification in proportion to uncertainty and user impact:

- run targeted tests
- capture screenshots or videos when UI feel matters
- run independent review when the scope, uncertainty, or failure cost warrants it
- fix blocking findings
- record the verdict and residual risks

Treat `NO-GO -> fix -> verify GO` as normal when an independent gate is justified, not as a mandatory ceremony.

### 5. Durable Worklog

When a session changes product direction or creates reusable design decisions that future work needs, update a worklog or handoff with:

- decisions Woojin made
- files changed
- verification evidence
- review findings and fixes
- known limits
- next candidates

## When Not To Use

Skip this loop for small direct edits, narrow bug fixes with an obvious root cause, pure code review, or tasks already covered by a more specific skill. In those cases route directly and keep the operator out of the way.
