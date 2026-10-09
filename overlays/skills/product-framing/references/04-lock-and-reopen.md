# Frame freeze, drift prevention, freeze release

## What to freeze and what to open

What gets frozen is not the truth of the product but **the frame to hold during the next experiment**.

- **Freeze (invariants)**: user, trigger, current alternative, committed outcome, comparative value, adoption path·ecosystem link chain — **the canonical source is the 6-item list in `templates/frame-lock.md`**
- **The most dangerous assumption is not frozen** — it is managed by experiment cycle in the frame-lock template's EXPERIMENT_CONTRACT. Moving to the next assumption after the experiment passes is normal learning, not a freeze release
- **Open (variable elements)**: UI, feature combination, technical implementation, prototype form
- **Conditions to reopen**: when there is a new observation that conflicts with an invariant condition, or when the decision-maker states a goal·value·scope they want to change. In either case, follow the existing approval transitions.

## Frame freeze conditions

1. The decision question is stated — not "what kind of user is this product for?" but "which of frame A and frame B do we adopt for the next experiment?"
2. Actually important alternatives were compared on the same criteria. You do not fill a candidate count, and keeping the current direction and not executing are also comparable options.
3. The chosen frame avoids all disqualifying reasons **applicable to that operating tier** (the PROBE and STANDARD lists are in SKILL.md under "Write the checklist and judge it")
4. The remaining uncertainty can be expressed as an experiment
5. The next experiment gives more discriminating information than further brainstorming
6. The decision-maker approves the frame version

The freeze is issued in the `templates/frame-lock.md` format. But **PROBE may skip issuing it** — the checklist's experiment contract (§6) and caps (§7) serve as the freeze (canonical: the rule at the top of the frame-lock template).

## Operating rules during implementation

Before the freeze, reversible scaffolding like a project skeleton, types and synthetic data prep is allowed. Implementation that depends on the outcome·completion conditions·user experience starts after the freeze.

1. **Separate the time·role of value judgment and implementation judgment.** Even for the same person, split the exploration prompt and the implementation prompt, and the implementation worker cannot modify the frame document. To an invariant change request, return `FRAME_CONFLICT`.
2. **Write the confirmation experiment's success criteria before the code and do not change them after the result.** For an exploration experiment, first write the exploration question·comparison scenes·observation method·stop and protection conditions in §6. Use newly obtained product criteria in the next cycle and do not rewrite past results as a success.
3. **Attach an outcome link to every implementation task:**
   ```text
   task:
   frame_id:
   supported_hypothesis_or_discovery_question:
   user_outcome_link:
   acceptance_test_or_observation_plan:
   ```
4. **Re-judge when new evidence appears, not by progress.** Look at "has new ground for the value hypothesis appeared", not "the feature is 80% done, so continue".
5. **Put an external blind reviewer in place.** Someone (or a new session) who does not know the implementation process reconstructs the user, problem, alternative, differentiator and organizer link from the document·demo alone.
6. **Declare the prototype disposable.** Do not let experiment code automatically promote into the seed of product code.

## Freeze-release signals — reopen only then

An experiment failure itself is not a freeze release. Record the result in checklist §6 and, in the next experiment cycle, replace the assumption, redesign the experiment or drop it. Request a freeze release **when a new observation conflicts with one of the 6 invariants, or when the decision-maker states a reason to change that condition**. Mere fondness or an agent's guess is not treated as approval to change. Observation-based examples are:

- Actual behavior observation repeatedly refutes the core problem·workaround hypothesis
- Usability·technology works but there is no intent to use·purchase
- The organizer API·service cannot provide the trigger information needed
- A stronger alternative is found and the differentiator disappears
- The core mechanism does not hold due to legal·data·operations constraints
- The user·buyer·evaluator demand different outcomes
- Team members and agents explain the same product as different users·problems
- There is no way at all to observe the outcome

## What is not a reason for freeze release

- The implementation is more annoying than expected
- A new UI idea looks cooler
- An agent recommends a different technology
- A new narrative added right before the presentation would seem more impressive

However, if the implementation difficulty collapses the core mechanism or the feasibility itself, that is a legitimate reason for freeze release.
The decision-maker may request a change of goal through experience or by their own value judgment.
Record which invariant condition and external commitment it affects, and approve or reject it with the existing decision record.
A new goal is not disguised as an observed market fact, and contract·personal-data·safety responsibility is not waived by consent alone.

The freeze-release request is made in the `templates/reopen-request.md` format. The state rules between submission and approval (stop starting new implementation during REOPEN_REQUESTED, SUPERSEDED on approval, return to LOCKED on rejection) also follow that template and the transition table in `references/02-tiers-and-verdicts.md`.

## Measuring the performance of this workflow itself

If you measure by "wrote more documents", goal displacement happens again.

**Top-priority measurement — blind frame relay** (from the first COMMITMENT): before starting, freeze the original text of the raw brief as `raw-brief-<frame_id>.md`. Give a new session that did not see the writing conversation the original raw brief and the frozen checklist separately, and have it reconstruct the user·trigger / current alternative / outcome / reason it is better / adoption path / next validation. Compare MATCH / PARTIAL / MISSING / INVENTED per item, and the checklist side's MATCH should rise and INVENTED fall. Check the 30-second pitch the same way.

Other metrics:

- **Frame clarity**: does the blind reviewer accurately reconstruct the user·trigger, current alternative, outcome, reason for differentiation, organizer link
- **Frame drift**: the number of times the 6 invariants changed after implementation began without a version increase. The most dangerous assumption is excluded because it is normally replaced
- **Waste before learning**: implementation time invested before the first external evidence·refutation
- **Evidence latency**: the time from frame freeze to the evidence that influenced the first decision
- **Unlinked work**: the fraction of implementation work not linked to any outcome·hypothesis
- **Checklist burden**: checklist writing·review time relative to the whole. If it keeps growing on a highly reversible project, the operating tier is too heavy

## Signals that this workflow should be changed

- The document passes but the blind reviewer cannot explain the value
- Even after writing the checklist, the frame keeps changing right after implementation starts
- Phrases without evidence automatically pass every time
- Matching the document format takes more time than a good experiment
- Every project is classified into the same operating tier
- The checklist blocks even a valid ultra-low-cost experiment / conversely, a real customer·data project passes as PROBE
