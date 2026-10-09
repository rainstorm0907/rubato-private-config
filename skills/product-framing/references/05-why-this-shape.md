# How to read this background document in the experimental version

Below is background material preserving the earlier design reasoning of this skill. Actual operation follows the current SKILL.md and the 01–04 reference documents and forms.
The current experimental version does not fix the order of free conversation, distinguishes proposal source·evidence·adoption,
and splits discovery, which forms criteria, from validation, which confirms criteria.
If an old explanation shows a fixed conversation stage or a prior product PASS requirement for every experiment, recheck the current rules.

---

# Why this structure looks this way — a methodology map

Full text of the original research report (author-kept raw material): if it is local, at `~/.claude/roo-channel/.consult/product-framing/response.md` (including source·evidence levels marked [A]–[D]).

## The methodologies are not substitutes but different layers

Arranging them in this order greatly reduces conflicts. This skill's checklist fields compress these layers into one.

1. **JTBD / Design Thinking POV** — who, in what situation, is trying to achieve what → field 1 (user and moment)
2. **Current-alternative research** (Lean Canvas's Existing Alternatives) — what are they making do with now → field 2
3. **Value Proposition Canvas** — which pain/gain is turned into which value → field 3
4. **April Dunford-style Positioning** — why this and not another alternative → field 4
5. **Logic Model / Theory of Change** — how a feature leads to a behavior·result change → the causal chain in fields 3·4
6. **Cagan 4 risks / Lean Startup** — what the most dangerous assumption is and how to test it → field 6
7. **PR-FAQ / staged investment review** — should the next investment be approved → operating tier and verdict
8. **PRD** — what to implement within the approved frame → a **downstream** artifact of this checklist

What has the strongest empirical grounding is not a particular canvas but the common behavior underneath: **explicit hypotheses, prior predictions, behavior observation, comparative experiments, staged investment.** Canvas·POV·PR-FAQ only externalize thinking and do not validate the truth of a sentence — so this skill separates document completeness from evidence grade (E0–E4).

## When to use the heavy archetypes

| archetype | condition under which the archetype pays off |
|---|---|
| Full PR-FAQ | external launch, multi-department collaboration, large customer-support·legal·brand impact |
| Full Business Model Canvas | must decide the real revenue model·acquisition channel·partners·cost structure together |
| Positioning workshop | multiple segments·competing alternatives and sales·marketing messaging matter |
| The full Customer Discovery process | paid service, recurring business, market selection matter |
| The full staged investment review | large cost increase per stage and multiple decision-makers |
| Detailed PRD | the frame is frozen, multiple implementers work in parallel and rework cost is high |

Forcing the nine BMC boxes for a several-day hackathon makes you document what you do not know as if it were fact. Conversely, demanding a long PR-FAQ for a disposable one-hour experiment makes the checklist cost exceed the failure cost.

## Why value blurs once you enter implementation (named phenomena)

- **Implemental mindset**: after a decision, attention narrows to execution·breaking through obstacles. The ability to question "why this choice" and the ability to focus on "how to finish it" are not maximized at the same moment
- **Design fixation**: the early implementation·example·architecture limits the later scope of thinking
- **IKEA effect**: you rate what you made yourself higher than its objective quality
- **Continuing investment due to sunk cost**: after investing, you keep investing even when there are failure signals
- **Goal displacement**: instead of the user outcome confirmed later, the immediately confirmed feature completion·working demo becomes the real goal

All are problems of structure, not will. So the prescriptions are also **protocols** like separating role·time, prior criteria, freeze and blind review.

## Anti-pattern checklist

```text
[ ] Does the problem statement contain a product·AI·platform name
[ ] Do "everyone", "convenient", "innovative", "efficiency" replace a concrete explanation
[ ] Did you not use a fake persona made without research as if it were fact
[ ] Is there recent real behavior or a trace
[ ] Was "doing nothing" considered as an alternative too
[ ] Did you distinguish outcome from output
[ ] Did you explain which outcome the differentiating feature leads to
[ ] Is there credible evidence
[ ] Did you not attach only the organizer's name (trigger→processing→handoff→outcome chain)
[ ] Did you distinguish hypothesis from evidence
[ ] Did you write PASS/FAIL before seeing the result
[ ] Is the MVP not a "small product" but a "minimum learning experiment"
[ ] Does only one active frame exist (do the plan·presentation·implementation spec assume the same user)
[ ] Can the implementation agent not silently change the frame
[ ] Are you not holding on due to sunk cost when a refutation signal appeared
[ ] Are you not demanding excessive documentation for a disposable experiment
[ ] Did you not count praise ("nice", "I'd use it if it existed") as behavior evidence
```
