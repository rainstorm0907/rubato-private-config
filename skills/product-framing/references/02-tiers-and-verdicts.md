# Operating tiers, verdict states, evidence grades

## Operating tiers in detail

Weight is decided not by project duration but by **irreversibility, external commitments, user harm, data·legal·brand exposure, operational continuity**.

### Practice (PROBE)

Applicability conditions (all must hold):
- Disposing of the output causes almost no external loss
- No user-data·payment·brand·legal risk
- The purpose is not shipping the product but confirming a fixed claim, or finding judgment criteria by experiencing a fixed scene
- The code is disposable as an experiment device too

Required fields: user and moment / current alternative / desired change / the uncertainty that would change the choice / experiment / scope and time·resource caps / user approval.
`experiment_kind: validation` needs prior PASS·FAIL and a competing hypothesis.
`experiment_kind: discovery` needs the exploration question, the scenes to compare, the observation·recording method, what will not be touched, and the stop conditions.
Product success criteria not yet formed are marked as such. Exploration approval and completion are not a product success verdict.

Pass = **experiment approval (PASS-PROBE)**. Only the disposable experiment is allowed, and it is not approval to start the whole product.

### Stage (STANDARD)

Applicability conditions (one or more):
- Receives external evaluation, like a hackathon·contest
- Multiple AI implementation workers move in parallel
- Invests several days or more, or demo completeness matters
- An organizer service·data link is subject to evaluation

Required: all 8 fields (§5 adoption path required, and the organizer link chain `N/A + reason` if not applicable) + evidence grades + frame freeze + **one independent red team and one blind review**.

The independent reviewers (both red team and blind review) are new sessions that took no part in writing the draft. If they are unavailable, record the user's exception approval in checklist §8 or hold. A self-red-team in the same session does not meet the STANDARD requirement.

Pass = **build approval (PASS-BUILD)**. Allows the demo·product implementation of the defined scope.

### Live (COMMITMENT)

Raise to this tier if **any one** of the following is present. Do not average one high-risk condition with lower conditions to bring it down.

- Paying customers
- Real personal·sensitive data
- Automated decisions or the possibility of user harm
- Contract·partner·legal responsibility, or brand responsibility where an official external commitment could cause real harm to customer trust (an ordinary hackathon judging·demo release is STANDARD)
- Ongoing operation responsibility after launch
- An expensive-to-reverse architecture or external commitment

Additional required: a condensed PR-FAQ / an owner and evidence for each of the 4 risks / an operations·failure·rollback plan / separation of buyer·user·approver / an evidence-based business viability review. All are recorded in the checklist's **live appendix (§9)**.

Passing COMMITMENT is also build approval, but it is issued only when every appendix item and the **signature of the approver per risk** are present. Incomplete items are human decision required (NEEDS-HUMAN, approver designated) or hold (HOLD).

## The verdict (gate_verdict) and the document state (status) are separate

`gate_verdict` is the result of this verdict, `status` is the lifecycle state of the frame document. The strings below are canonical and are used verbatim everywhere, including in JSON.

**gate_verdict:**

| verdict token | meaning |
|---|---|
| **PASS-PROBE** | experiment approval — only the disposable experiment is allowed |
| **PASS-BUILD** | build approval — allows the demo·product implementation of the defined scope |
| **HOLD** | hold — the structure exists but the evidence or dependencies are lacking |
| **KILL** | drop — a core assumption was refuted or there is no comparative value |
| **NEEDS-HUMAN** | human decision required — designates an approver for a judgment AI cannot own |

Reopening a frozen frame is not a verdict but a **separate freeze-release decision**. Submitting a request can only cause a transition to the intermediate state (REOPEN_REQUESTED), and **only the decision record in `templates/reopen-request.md` (APPROVED/REJECTED + approved_by·approved_at) can cause a terminal transition** that leaves or returns to LOCKED.

**status transitions (there are no transitions outside this table):**

| transition | condition |
|---|---|
| DRAFT → LOCKED | only when gate_verdict is PASS-PROBE or PASS-BUILD and there is a user approval record (approved_by, verdict_at) |
| DRAFT kept | HOLD, NEEDS-HUMAN — until what is lacking is resolved |
| DRAFT → RETIRED | KILL |
| LOCKED → REOPEN_REQUESTED | immediately upon submitting `REOPEN_REQUEST`. New implementation that depends on the invariants stops, and in-progress work on variable elements may be finished |
| REOPEN_REQUESTED → SUPERSEDED (+ new version DRAFT) | the freeze-release decision record is APPROVED (approved_by·approved_at required). **The only moment the previous frame becomes SUPERSEDED** |
| REOPEN_REQUESTED → LOCKED | the freeze-release decision record is REJECTED — the existing gate_verdict and freeze are restored as they were |
| REOPEN_REQUESTED → RETIRED | the freeze-release decision is APPROVED but it is decided to fold without a replacement frame (e.g. a core assumption refuted) — approved_by·approved_at required |
| LOCKED, EXPIRES_AT elapsed | the freeze expires and new delegation stops until re-judged by a mandatory review |

**Only one** frame with status LOCKED exists per repository. A new version's freeze is issued only when the previous frame is in SUPERSEDED status.

## Evidence grades E0–E4

It is not an absolute score. It marks **what kind of evidence** each core claim has, and **it is attached per claim** — not "there is E2" but "on which claim, a person in which role gave E2, in which context". You must not fill a buyer's willingness-to-pay claim with the user's praise (E2), and competing-service·review material a research agent collected on the web is E1, not E2.

- **E0 — estimate**: only the team's estimate
- **E1 — circumstantial**: indirect traces like documents, market data, reviews, support tickets, public logs
- **E2 — observation**: recent past-behavior interviews, direct work-flow observation
- **E3 — commitment**: costly action like providing data, booking a schedule, a pilot/LOI, payment
- **E4 — in-use performance**: real repeated use·payment·change in work results

Weak evidence is not automatically a failure:
- **Practice (PROBE)**: even with only E0 hypotheses, PASS-PROBE is possible if there is a valid confirmation experiment or a scoped exploration experiment and user approval.
  Just because the source is the model does not make it E0, and just because the user adopted it does not raise the grade.
  Discovery results alone cannot substitute for STANDARD·COMMITMENT's external claims or risk approval.
- **Stage (STANDARD)**: at least E1 or above on the applicable core claims + independent blind review
- **Live (COMMITMENT)**: E2 or above or E3 regarding value, and the main business-viability obstacles resolved

## AI verdict output format

```json
{
  "gate_verdict": "PASS-PROBE | PASS-BUILD | HOLD | KILL | NEEDS-HUMAN",
  "hard_failures": [],
  "field_checks": [
    {
      "field": "actor_and_moment",
      "status": "FILLED | PARTIAL | MISSING | CONTRADICTORY",
      "evidence_quote": "quoted verbatim from the document",
      "reason": "reason for the verdict",
      "human_review_required": false
    }
  ],
  "cross_field_conflicts": [],
  "unsupported_claims": [],
  "reopen_triggers_detected": [],
  "allowed_next_commitment": "The maximum scope allowed in the next stage. Even under hold, may state up to scaffolding as allowed"
}
```

Operating rules:
- Do not infer content not in the document and treat it as "filled"
- Attach a quote from the source text to every verdict
- Classify factuality only as CLAIMED / EVIDENCED / CONTRADICTED (no VERIFIED)
- Do not pass by averaging numeric scores. Check disqualifying reasons by whether they apply, and the human signs the strategic judgment
- `allowed_next_commitment` is the place to write the ceiling on the next action, separate from the verdict. Even under a hold verdict, it may allow reversible scaffolding like project skeleton·types·synthetic data prep, and implementation that depends on the outcome·completion conditions·user experience is left behind the freeze
