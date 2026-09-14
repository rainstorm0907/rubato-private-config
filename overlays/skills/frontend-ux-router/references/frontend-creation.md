# Frontend Creation

Use this workflow for new pages, flows, dashboards, landing pages, first drafts, redesigns, and frontend implementation that combines UX, content, interaction, and visual direction.

The durable rule behind everything below:

> Start from the user's evidence-action-result path. Never start from the available
> fields, model outputs, audit labels, or internal taxonomy. Available data is an
> implementation input, not an information architecture.

For a concrete recorded failure (seven patch attempts that never fixed the task model), read `task-design-failure-case-study.md`.

## Contents

- [1. Frame the path](#1-frame-the-path)
- [2. Hard budgets](#2-hard-budgets)
- [3. Compose content and hierarchy](#3-compose-content-and-hierarchy)
- [4. Copy rules](#4-copy-rules)
- [5. Visual concept](#5-visual-concept)
- [6. Model interaction and reachable states](#6-model-interaction-and-reachable-states)
- [7. Implement the complete path](#7-implement-the-complete-path)
- [8. Deletion pass](#8-deletion-pass)
- [9. Render and walk the path](#9-render-and-walk-the-path)
- [10. Fresh-eyes gate](#10-fresh-eyes-gate)
- [Stop-and-redesign triggers](#stop-and-redesign-triggers)

## 1. Frame the path

Start from the current request, existing product and real examples. Identify the actor,
intended experience/result, evidence needed and consequential actions. Use the answers
already available; do not make the user restate them or fill an intake form.

For work that needs a durable plan or delegation, keep this in existing work notes or a
brief: goal, meaningful action or viewing experience, required evidence, preserved behavior,
open choices and relevant recovery/resume. It is not a required report template. A passive
recap has an experience to sustain, not an action to invent.

Inspect the routes, components, design language, contracts and tests that can change the
plan. Keep the user's constraints separate from your method. Existing code is a reusable
asset, not proof that its current parameters define the only possible experience.

An authorized exploration may use provisional visual choices to help form a criterion.
Record the source-backed extent of exploration in the existing brief/path notes; do not
infer permission to change Frozen items, send data, delete, charge, publish or expand the
product. Ask only about consequential unresolved choices, with a recommendation. An
isolated route does not require a substitute design language or replacement chat UI.

Translate a proposed experience into behavior before splitting work: what must the person
actually be able to see or do, and what must work together to make that possible? Check
those relationships against the current code and real material. If a claimed scene cannot
arise from the plan, change the plan inside scope before presenting it as ready to build.
There is no mandatory architecture diagram, state schema or extra planning stage.

## 2. Hard budgets

Only budgets from the user, product contract, platform or accepted work boundary are hard
limits. Preserve and check them. Do not invent a universal count of visible controls or
require a primary button for a viewing experience.

Keep a clear hierarchy; place evidence and relevant controls together; avoid unfamiliar
encodings and internal identifiers that make the user learn the implementation. Follow
accessibility and actual platform constraints. Dense tools may legitimately need several
controls. If a real constraint conflicts with the proposed experience, resolve that conflict
rather than weakening the test or deleting approved content to produce a green result.

## 3. Compose content and hierarchy

- Use realistic domain content to shape the page before choosing components.
- Arrange content in the order the actual task or viewing experience needs. Orientation, evidence, action and recovery are useful roles, not a mandatory sequence of visible sections.
- Show decision evidence in its native medium: real chart for chart judgment, real audio for music judgment, synchronized playback for timing judgment, both states together for comparison, the actual editable object for editing. Counts, ticks, and summaries are secondary orientation, never the evidence.
- Keep the main path focused on the intended activity or viewing experience. Put unrelated diagnostics and research detail behind an appropriate secondary entry.
- Make the unit of judgment understandable. It can be an item, transition or connected sequence; do not cut away the before/after context needed for the question. Reducing item count does not repair an incomprehensible task.
- Ground prices, counts, timelines, policies, and impact claims in supplied evidence; label sample values in fixtures.

For action-oriented interfaces, useful first-view questions include (adapt them for viewing or exploration):

1. What product or task is this?
2. What must I look at, listen to, or compare?
3. What is happening now?
4. What is the primary next action?
5. What result should that action produce?

For review, comparison, labeling, moderation, generated evidence, or synchronized media, read `task-evidence-design.md` before choosing components.

## 4. Copy rules

Every visible string must serve at least one purpose: orient, describe current evidence/state, state an available action, explain what just happened, or offer recovery/continuation. A string that serves none of these is deleted in the [deletion pass](#8-deletion-pass).

**Ban list — never in visible copy** (mechanically checkable):

- `snake_case`, `camelCase`, or dotted identifiers
- raw enum values (`pending`, `abstain`, `select`, `PROCESSING`)
- ids, hashes, UUIDs
- raw ISO timestamps (`2026-07-12T05:53:34Z`)
- schema/storage/pipeline nouns, prompt or model terminology, confidence semantics
- meaningless headings: `Data`, `Info`, `Details`, `Item 1`, `Section`
- form-label copy where a sentence belongs: `확인한 이의제기: 보완 요청`, `상태: 진행 중`. A person reads a sentence, not a key-value pair.
- **In Korean copy**, typographic connectors people do not type: `·`, `—`, `→`, `|`, emoji, and mixed-in English words. Join with a period or a comma. Number only where order carries meaning. In other languages, follow that language's ordinary punctuation; the check is still "would a person type this in a sentence".
- mixed speakers in one screen: the service, the user, and a third party (a bank, a reviewer) must not share one voice. Decide who is speaking on each surface and keep it.

**Comment-copy test:** read every visible string as a first-time user. Rewrite or delete anything that reads like a code comment, schema field label, experiment note, commit message, or spec fragment.

Transformation examples (adapt to the product's domain language; do not apply mechanically):

| Internal or comment-like copy | User-facing direction |
|---|---|
| `자동 판단을 보류한 것이 맞나요?` | Ask about visible evidence: `이 소리를 따라가는 노트가 있었나요?` |
| `채보 행동`, `음악 후보` | The familiar object: `노트`, `공식 채보` — or no label at all |
| `고정 표본 42개 중 3번` | Bounded current session, shown after one item is understandable |
| `판정 저장됨` | `답을 저장했습니다.` |
| `pending` / `abstain` | `잘 모르겠어요` / `나중에 다시 볼게요` |
| `현재 항목의 noteKinds: [tap, hold]` | Show the actual notes |

## 5. Visual concept

Read the current product and relevant reference examples before choosing candidates. Take
relationships that serve the goal, not just a color name or isolated effect. Identify what
will become easier to follow, read, compare or feel, and where the analogy stops. Keep the
existing product language unless the task opens it; neither novelty nor fidelity to a
reference is evidence of quality by itself.

When the question is an overall composition, make its necessary parts work together.
Preserve a good baseline separately without locking every alternative to its values.
When the question is one known variable, keep other relevant conditions stable. A quick
concept comparison need not prove which component caused every reaction. Report coupled
changes honestly instead of removing a necessary relationship for experimental tidiness.

Use the cheapest medium that can actually expose the uncertainty: existing artifacts,
sketches, generated images, working UI or clips. A fixed number of generated images, a
pre-code image gate and one-variable-only variants are not universal requirements. Prepare
credible candidates and a recommendation, not an intentionally weak opponent for a favorite.
Parts may be combined after checking their fit; the baseline may remain the best result.

Do not ask the user to imagine a missing core scene. If timing or an interactive relation
matters, prepare that behavior in the allowed prototype. Verify what can be observed and
state the limits of the medium. The designer owns the preparation; the user need not invent
the concept or repair the fixture just to have an opinion.

## 6. Model interaction and reachable states

Cover the states the changed path can enter:

```md
State -> Trigger -> Visible meaning -> Available action -> Recovery or resume
```

Choose among default, in-progress, success, first-use empty, no-results, error, permission, and offline states according to actual behavior. Give every included state a clear meaning, useful action, and visible transition. If evidence can be genuinely ambiguous, provide a plain uncertainty action — do not force a guess or hide uncertainty behind an internal status.

## 7. Implement the complete path

- Semantic structure, accessible names, visible labels, logical focus order, readable contrast, keyboard operation.
- Preserve user input across recoverable failures when safe.
- Immediate feedback for consequential actions.
- Respect reduced-motion preferences when motion is present.
- Responsive behavior around the content and task, not a named device.

## 8. Deletion pass

Use the rendered view to remove or demote clutter that does not serve the experience,
evidence or action. Keep intentionally approved content and meaningful expressive details.
Do not require an element-by-element ledger, deletion quota or a separate report. Explain
only material changes. Do not strip away what makes the product distinctive merely because
it is not a control or a prerequisite input.

## 9. Render and walk the path

Use the real rendered interface as the completion gate:

1. Start from a realistic route and state.
2. Complete the primary action with the actual control.
3. Observe feedback, dependent relationships, and the success state. Verify product verbs as observed state transitions (selection→preview, edit→result, action→feedback, error→recovery, save→resume, media→visualization sync). A loaded component is not a working relationship.
4. Exercise a consequential recovery or resume path when relevant.
5. Inspect keyboard operation and focus.
6. Inspect the target viewport and a materially narrower viewport; confirm evidence and action remain co-located.
7. Read every visible string as a first-time user; re-check the copy ban list.
8. Check browser errors, overflow, clipping, contrast, and state transitions.
9. Confirm actual source-backed constraints still hold after all changes.

Keep enough commands, input/state, observations and artifact references to reproduce decisive checks in the existing evidence location. Exercise only affected paths and relevant platforms. Do not claim motion or interaction from stills alone. Repair missing promised behavior within authority; do not return only a warning when you can complete the assigned preparation.

## 10. Fresh-eyes gate

Use an independent comprehension review when required by the user/release contract, or
when new navigation, unclear evidence/action relationships or repeated confusion makes it
worthwhile. It is not required for every layout or color adjustment. Do not invent a review
team without the applicable staffing/model permission.

When used, `fresh-eyes-review.md` governs the comprehension-only packet: intended actor,
rendered view and relevant live path, without the builder's explanation. This tests what is
understandable without coaching. It does not determine whether the artifact satisfies the
whole project; a goal/quality review needs the real goal, constraints and relevant examples.
Do not blind a goal reviewer to the very requirements they must check.

Use the finding to make an in-scope repair or revise the task model when warranted. A
required pending review stays pending. Otherwise report the checks actually performed;
`VERIFIED` is never shorthand for the user's taste or a requirement to add another reviewer.

## Stop-and-redesign triggers

These observations can indicate that local polishing is missing the problem; inspect their cause:

- the user (or fresh-eyes reviewer) asks what they are supposed to do;
- the primary action makes sense only after reading a legend or learning an internal category;
- real evidence is replaced by prose, counts, logs, or metadata;
- evidence and answer controls cannot be seen together;
- related audio, animation, chart, preview, or state does not update together;
- the same interaction receives a second explanatory copy patch;
- reducing batch size is being used as the fix for confusion;
- a successful build or static screenshot is being offered as proof of interactive behavior.

Response: locate the actual cause in the request, artifact and evidence. Repair it within the assigned boundary and check the affected behavior. Rework the task model when that is the cause, not because a fixed number of attempts passed. Ask for the missing consequential decision if necessary; do not add a new interview, whole-project audit or unapproved redesign. Repeat an independent review only when required or likely to change the decision.

## Research basis

- `task-design-failure-case-study.md` (recorded incident, 2026-07-12)
- [GOV.UK: Learning about users and their needs](https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs)
- [NN/g: 10 usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [W3C: WCAG 2.2](https://www.w3.org/TR/WCAG22/)
