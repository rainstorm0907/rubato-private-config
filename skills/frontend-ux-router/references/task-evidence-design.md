# Task Evidence Design

Use this reference when a user must inspect, compare, classify, approve, correct, or judge evidence before acting. It applies to review tools, moderation, labeling, forms with previews, generated results, calculations, media, charts, timelines, and other interfaces whose value depends on a relationship between evidence and action.

## Contents

- [Frame the decision](#frame-the-decision)
- [Present decision evidence](#present-decision-evidence)
- [Keep the decision loop together](#keep-the-decision-loop-together)
- [Use familiar encodings](#use-familiar-encodings)
- [Prototype one complete unit](#prototype-one-complete-unit)
- [Verify dynamic relationships](#verify-dynamic-relationships)
- [Preserve the loop across viewports](#preserve-the-loop-across-viewports)
- [Return to the task model](#return-to-the-task-model)
- [Completion evidence](#completion-evidence)

## Frame the decision

Use the path already established under `frontend-creation.md`; keep notes only when needed. For this evidence-driven task, pay attention to:

- the actor's goal in familiar language;
- the evidence required for a valid decision;
- the primary action and visible result;
- a legitimate uncertainty action;
- mistake recovery, interruption, resume, and completion.

Resolve available facts yourself and make reversible choices within authority. Ask with a recommendation when an unresolved user choice changes the outcome or consequential action. Sending, publishing, charging, deleting, approving, reserving, committing and undoing retain their actual permissions. Pause only work that depends on the missing authority; an uncertain preference can be explored in an authorized prototype rather than blocking all preparation.

Start from the user's verb: inspect, compare, choose, correct, approve, listen, retry, or continue. Map internal categories to the concrete judgment the actor can make.

## Present decision evidence

- Present evidence in the medium where the actor can genuinely decide.
- Use the actual editable object and its result for editing tasks.
- Show comparison states together when the decision depends on differences.
- Present source content together with the relevant policy or criteria for moderation and review.
- Present calculation inputs together with the resulting value and consequence.
- Present temporal evidence through synchronized source media and visualization when timing matters.
- Use summaries, counts, metadata, and diagnostics as orientation or secondary detail.
- Keep internal taxonomy, confidence semantics, storage fields, and pipeline categories in development and expert surfaces.

## Keep the decision loop together

Keep the following together where relevant; they are not a mandatory screen order:

1. task orientation;
2. current state;
3. decision evidence;
4. current question;
5. available actions;
6. visible feedback;
7. recovery or continuation.

- Keep transient evidence, the question, and its actions in one working context.
- Preserve playback, selection, comparison, or preview context when the layout stacks.
- Provide a plain uncertainty action when the evidence supports more than one interpretation.
- Provide undo, correction, retry, resume, and completion paths according to the task.
- Keep advanced diagnostics behind a deliberate expert entry while preserving primary-task prerequisites in the initial view.

## Use familiar encodings

- Use color, icons, sound, motion, and labels with familiar domain meaning.
- Use one neutral emphasis when the user needs to notice a moment or object.
- Introduce a distinct encoding when the distinction itself supports the user's decision.
- Keep each encoding adjacent to the evidence, persistent while needed, immediately understandable, and accessible through more than one sensory channel.
- Confirm through the rendered task that the encoding reduces cognitive work.

## Prototype one complete unit

- Choose a representative judgment unit: an item, comparison or connected sequence. Include the before/after relationship the question needs.
- Exercise the relevant action or viewing experience and its resulting state. Repair known omissions within scope before asking the user to judge it.
- Use an independent comprehension check when required or materially useful, under `frontend-creation.md` §10; not every comparison needs another agent.
- Expand unrelated batch mechanics only when the assigned outcome needs them.

## Verify dynamic relationships

Verify product verbs as observed state transitions:

| Relationship | Evidence |
|---|---|
| selection -> preview | selected input and rendered preview correspond |
| edit -> result | visible result reflects the current input |
| action -> feedback | action produces clear progress and final status |
| error -> recovery | safe input and context remain available for retry |
| save -> resume | reload restores the confirmed state |
| source media -> visualization | playback, seeking, and end state remain synchronized |
| item change -> context | evidence and actions move to the same current item |

For temporal interfaces, exercise the supported transitions affected by the change, such as play, seeking, end/reset or resume. Do not invent controls just to complete this list. Measure relevant synchronization and distinguish sampled frames from full-speed observation.

## Preserve the loop across viewports

- Inspect the real target viewport and a materially narrower viewport.
- Keep evidence, question, and action together when the decision depends on transient context.
- Preserve content priority, playback or selection context, and the primary action while stacking.
- Check overflow, wrapping, sticky collisions, zoom, and viewport-specific controls.
- Keep progress proportional to the task and secondary to the current decision.

## Return to the task model

Revisit the task or implementation cause when the following evidence warrants it:

- the user asks what they are supposed to do;
- the task needs repeated verbal coaching;
- a legend or private encoding must be learned before acting;
- internal categories become prerequisites for a user decision;
- prose or metadata replaces evidence the product can present directly;
- evidence and action separate across the working view;
- related media, previews, calculations, totals, or states move independently;
- repeated explanatory copy changes leave the same task unclear;
- queue size or visual polish becomes the main response to a comprehension failure;
- the user identifies an obvious missing interaction step.

Use the specific failure to decide whether a local repair or a different task structure is needed. Repair inside scope and walk the affected relationship again; do not add an explanation layer to disguise a wrong model or restart the whole design for every local defect.

## Completion evidence

Keep decisive evidence in the existing result record as relevant to the assignment:

- route, fixture, target viewport, and narrow viewport;
- evidence presented and primary action performed;
- visible feedback and decision result;
- uncertainty, correction, recovery, resume, and completion paths;
- observed dynamic relationships and synchronization measurements;
- keyboard, focus, browser errors, overflow, screenshots, and traces.

Use the scoped completion reporting in `frontend-creation.md`; a new report or status ladder is not required.
