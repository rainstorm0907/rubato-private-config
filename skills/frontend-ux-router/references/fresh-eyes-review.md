# Fresh-Eyes Review Protocol

An optional comprehension check unless the user or release contract requires it. Use it for new or unclear interaction paths, not as a compulsory stage of every visual change. The reviewer infers how to use the rendered interface without implementation coaching; this is not a taste or whole-goal review.

Two roles use this file:

- **Implementer**: when the review is warranted and authorized, prepares the packet (`frontend-creation.md` §10). Does not label self-review independent.
- **Dispatcher / reviewer**: runs the review with zero implementation context.

## Why the roles must be separate

The builder can miss confusion because the intended meaning is familiar. A separate reader can expose that blind spot; it does not make either reader infallible. Preserve independence for this check while retaining the builder's duty to inspect and repair obvious problems.

## Contamination rules

The reviewer must receive ONLY:

1. one persona line (who the actor is, in product terms — e.g. "리듬게임을 아는 음악 검수자", never "a user reviewing detector output against chart actions");
2. screenshots of the rendered initial view at target and narrow viewports, or a live route/URL;
3. optionally, the post-primary-action screenshot when feedback is being judged.

The reviewer must NOT receive: the task brief, the path card, design rationale, internal terminology, the diff, or answers to their questions. If the reviewer asks "what is this supposed to be?", that is a FAIL finding, not a question to answer.

## Reviewer prompt (dispatch verbatim)

```text
You are a first-time user of this product. You are: {PERSONA_LINE}.
You have never seen this screen and nobody will explain it to you.
Look at the attached screenshot(s) (or open {ROUTE}) and answer using ONLY
what is visible:

1. What product or task is this?
2. What must you look at, listen to, or compare?
3. What is happening right now?
4. What would you do first (including simply watching), and what makes that clear?
5. What do you expect to happen after that action?

Then report:
6. Every element (text, control, badge, color, icon) whose purpose you cannot
   explain — list each one.
7. Every visible string that reads like a code comment, schema field, status
   enum, or developer note — quote each one.
8. Anything you would need to be taught before you could act confidently.

Verdict:
- PASS: you answered 1–5 confidently from visible content alone, and lists
  6–8 are empty or trivial.
- FAIL: any of 1–5 was a guess, or any list contains a blocking item. State
  which question numbers failed and why.

Answer honestly as a stranger. Do not be charitable. A guess counts as a
failure even if it happens to be right.
```

## Grading

- **PASS** requires confident answers to all five questions AND no blocking items in lists 6–8. "I guessed and got lucky" is a FAIL.
- On **FAIL**, use the concrete answers to identify the likely cause: evidence/orientation, action hierarchy, expected-result feedback or copy. This is a lead to check, not a required path-card rewrite.
- The implementer checks the reported cause and repairs the relevant path under `frontend-creation.md`. Do not coach the reviewer into a PASS or add a tooltip to disguise a wrong task structure. Fix a local defect locally.
- Re-review if required or if it can change the decision after repair. Repeated confusion is evidence to revisit the cause, not proof from a count alone. Return a consequential unresolved user choice with the specific evidence; do not make the user do routine diagnosis.

## Dispatcher notes

- Choose a capable reviewer under the active model and budget permissions. Observation quality matters; a model label alone does not certify it.
- Run the reviewer in a fresh context (new worker/session). Never reuse the implementer's session or a session that saw the brief.
- When the screen's actor is an expert (diagnostic tools, admin consoles), set the persona line to that expert. The gate tests fit-to-actor, not universal simplicity.
- Attach the findings to existing evidence. A required review must pass or remain pending. Otherwise say which checks were done; absence of this optional check does not force another agent. Its PASS is scoped to comprehension, not overall design quality or user preference.
