# Rules for writing each checklist field

Eight fields — the numbers are the same in templates/gate.md and in every document. Each field exists to prevent "the failure that occurs when it is missing" — filling in a box is not the purpose.

## Checklist metadata (outside the field numbers — the header)

frame_id, version, status (DRAFT / LOCKED / REOPEN_REQUESTED / SUPERSEDED / RETIRED), operating tier, decision-maker, validity period, gate_verdict, verdict_at, approved_by. The canonical source for the strings and the transition rules is `references/02-tiers-and-verdicts.md`.

If missing: multiple agents treat different frames as canonical, and changes get mixed in silently.

## 1. User and moment

Write: the user, the buyer/decision-maker, the evaluator/organizer, the specific trigger, a recent real example, the evidence grade.

- "General users", "companies", "when needed" are forbidden. Write a **person/role + situation + event**
- If the user and the buyer·evaluator differ, always separate them. Especially in B2B, the user, administrator, budget holder and legal are different people
- Do not get stuck only on the "moment of removal" — newly created gains like fun, achievement or trust are progress too
- STANDARD and above also write **problem pressure**: frequency·cycle of occurrence, loss when it occurs, why now, the first user group reached, verifiable scale metrics. This block distinguishes problems that are real but differ in investment value

If missing: it becomes a "platform for everyone" and feature priorities collide. Without problem pressure, a problem that is real but has no investment value passes.

## 2. Current alternative

Write: the current real behavior, the tools·manual work·competing products in use, **the case of doing nothing and its reason**, the current alternative's cost·failure.

- Do not write only competing products. Excel, KakaoTalk, asking a senior, giving up may be the real competitors
- Write the advantages of keeping the status quo too — there is a reason people do not switch
- **A risky workaround is strong demand evidence.** If the current alternative shows risk-taking like external payment, password·account sharing, scraping·macros, shadow Excel or policy violations, write it as evidence stronger than stated intent (E1 or above). Decompose it as `observed workaround = legitimate purpose + risky means + constraint handling missing from the product`, and the frame absorbs the purpose as a first-class feature with permissions·limits·audit, rather than making the means convenient
- STANDARD and above also write the **switching conditions**: the trigger to switch, the reason not to switch, the switching cost (procedure·money·trust·relationship), and who bears that burden. Product value must exceed the switching cost for people to move — you cannot predict a choice from "the outcome is better" alone. AI products especially often carry a trust cost of "accurate but not believed" and a double-entry cost

If missing: you imagine a nonexistent empty market and claim "it's convenient" without a comparison baseline. Without switching costs, a product that is "better but no one switches" passes.

## Distinguish writer, evidence and adoption

Distinguish the experience the user described, the external facts that were confirmed and the solution the model proposed.
Do not lower a claim grounded in real material to E0 just because the model wrote it.
Proposal-source tokens indicate writing and adoption; the evidence grade is attached separately to fit the claim and the material.
Do not expand the user's interest or partial agreement into final adoption·execution approval.

## 3. What changes

Write: the progress and outcome the user gains, the change to be observed, the baseline or proxy metric, the success criteria, the harm·safety criteria.
In `discovery`, write that the product success criteria not yet known are still forming, and connect the experience to be confirmed and the observation method to §6.
Safety, input preservation, data and scope conditions are still set in advance. When claiming external performance, do not declare success from exploration observations alone.

- Do not stop at the number of features, the number of screens or "AI accuracy"
- Write **what actually changes** among the user's behavior·time·errors·cost·risk·success rate

If missing: you mistake feature completion·a working demo for value.

## 4. Why this is better

Split "why it is better" into two:

- **Differentiation mechanism**: because we do something differently
- **Value created**: and so how the user's behavior·results change

Write: the real comparison target, our own mechanism, the causal chain (mechanism → behavior change → outcome), the credible evidence.

- Using "faster", "convenient", "innovative", "one-stop" alone is forbidden. The comparison target·conditions·mechanism·outcome must all be present

If missing: only unverifiable phrases like "fast because it's AI" remain.

## 5. Adoption path·ecosystem link

It splits into two parts. **The adoption path is required for STANDARD and above**: where the first user meets the product, who decides to start using it, who deploys·onboards, where it plugs into the existing work flow, and the evidence that this path is actually reachable. The cheaper implementation gets, the bottleneck is not building but **reaching** — a good product dies if there is no way to meet it.

**Only organizer dependence is conditional**: for a project with no dependence on an organizer or required partner, end only that part with `N/A + reason` — do not invent a fictional link. The adoption path must not become N/A too. Where an organizer applies, attaching only the name is judged as unwritten. The whole chain must be present:

```text
[user trigger occurs]
→ using [some existing data·service·API of the organizer]
→ [the product performs some judgment·transformation·action]
→ hands the result to [which existing screen·work·service] (handoff)
→ creating [the user outcome]
→ and [the organizer's business·operations·brand goals] also change
```

If any arrow is missing, it is judged as "attached only the name". If the same product works without the organizer's assets, state that relationship honestly.

Note — judging weights differ per contest, but the problem·value description cuts across several items: if what it solves is unclear, Impact weakens; if the organizer link is superficial, Relevance; if differentiation is unclear, Originality; if the outcome is unclear, Presentation weakens too.

## 6. The most dangerous assumption and the experiment contract

Write: `experiment_kind` (validation or discovery), the currently most important uncertainty, why to examine it first,
the experience to compare against the existing state, the observation method, the deadline·stop conditions, and the next choice the result will change.

- For `validation`, write a competing hypothesis that would explain the same observation as the core claim, and fix the PASS·FAIL criteria before the result.
  A high usage rate may be due to favor·free access·novelty, so do not interpret the observation only as the reason you want.
- For `discovery`, decide the reason you do not yet know the product criteria, which scene and difference you will experience, what to leave behind, and the stop conditions.
  The purpose is to find new criteria, and you do not insert fake PASS·FAIL. Two complete solutions are not strictly required, but
  there must be a current state or a real experience to distinguish.
- For both kinds, fix the safety·write·data boundaries and budget, and the user approval conditions. State separately any state that cannot be built or observed.
- After exploration, record observations, newly revealed differences and the next choice. Do not retroactively change new criteria on past cycles into a success.
  To claim product performance, you need a separate confirmation cycle with criteria set.
- This field is an **experiment contract** — unlike the frame, it is normal for it to be updated every experiment cycle
- For a frame that absorbs a risky workaround as an official feature, put "does the official path replace the workaround, or is it used alongside and actually amplified" among the most dangerous assumption candidates, and include distinguishing replacement/parallel/new abuse in the experiment and post-launch measurement
- After the experiment, fill in the result record (`observed_result`·`decision_taken`). Distinguish prior commitment from actual execution, and when raising the cycle, keep earlier records via `prior_cycle_ref`

If missing: coding becomes the automatic default, and you change the success criteria after the result comes in.

## 7. Scope and commitments

Write: what will be built in this stage / what will not be built / the disposable part / what is promised externally / the maximum time·cost·data exposure / the rollback method.

If missing: the implementation scope creeps up.

## 8. Frame selection and review record

Write: the chosen frame and the reason, the frames reviewed and rejected and the reason, the invariants to freeze (canonical source is the 6-item list in the frame-lock template), the variable elements to keep open, the freeze-release signals, the review record (reviewer·independence·findings·disposition).

If missing: you overturn a wrong frame too late, and no one can prove a blind review actually happened.

---

# Good example (fictional example — the numbers are examples only)

```markdown
frame_id: host-cs-delay-compensation
version: 2
status: LOCKED
tier: STANDARD

user: a new agent at the organizer's shopping-app night customer center
buyer/decision-maker: the customer center operations lead
trigger: during a live chat, the user asks whether an order with multiple carriers qualifies for delay compensation (seed)

problem pressure:
delay-compensation-related night inquiries run about 120 per week [E1: CS ticket tag tally].
A wrong answer causes a wrong compensation payment or a re-inquiry. The first user group reached is 8 new night-shift agents.
Why now: ahead of the Q4 logistics peak season, night new hires are increasing and wrong answers·escalations are rising.

current alternative:
The agent searches three policy wikis, then asks a senior whether an exception applies.
In three of the four recently observed cases, writing the answer draft took more than 3 minutes. [E2: work-flow observation record]

switching conditions:
switch trigger: at the moment the chat SLA warning appears, they press the draft button — starting in parallel with the existing wiki search. (AI proposal→edited)
The draft appears inside the existing support reply box, so no double entry. The reason not to switch is
distrust of the AI draft — the experiment under the most dangerous assumption below targets this directly. The switching burden (review time) is the agent's own.

user outcome: obtain an answer draft with cited sources within 60 seconds
success criteria: a supervisor approves 4 or more of 5 test scenarios without edits, and draft time is 60 seconds or less

comparison target: the existing wiki search, asking a senior, a general internal RAG
own mechanism: receive order·carrier·policy version·exception state together as CRM context,
select the applicable clause, and build the draft with its sources
causal chain: combining CRM context → not manually cross-checking documents against order information → reduced answer time and wrong compensation guidance

adoption path:
Since it is inserted into the existing support console, no separate discovery path is needed. Deployment·onboarding is decided by the customer center operations lead
[E2: the lead proposed the pilot conditions directly].

organizer link chain: delay-compensation inquiry chat starts → the organizer's CRM Order API passes the order·shipping status
→ policy judgment·evidence search → the draft is inserted into the existing support reply box → the handling reason code is saved
→ agent SLA and policy compliance improve

learning_cycle: 1
most dangerous assumption: VALUE — even if the AI draft is accurate, the supervisor may not trust it
competing hypothesis: even a high approval rate could be "they were lenient because it was an experiment" → distinguish: check up to whether actually sending was allowed
experiment: provide drafts for 5 realistic scenarios in a Wizard of Oz manner
PASS: 4 or more approved without edits + the supervisor allows the pilot
FAIL: 3 or more manually rewritten due to a trust problem, or the pilot is refused

scope: only one policy, delivery-delay compensation. No automatic sending. Not building a general chatbot
freeze release: the main trigger of real inquiries is not delivery delay (trigger invariant collapses) / required CRM fields are inaccessible (organizer link chain collapses)
(falling short of the approval criteria is not a freeze release — record the result in §6 and go to the next experiment cycle)
```

# Bad example

```markdown
user: all customer center staff
problem: there is a lot of repetitive work and no AI platform
current alternative: manual work
value: AI processes it faster, more accurately and more conveniently
differentiator: a one-stop platform that uses the organizer's API
validation: build an MVP and see the user response
```

Failure reasons: no user·trigger / problem written as the absence of a solution / current alternative not concrete / no observable outcome / no comparison target·mechanism·credible evidence / no input·processing·handoff for the organizer API / no most dangerous assumption and prior PASS/FAIL / no scope.
