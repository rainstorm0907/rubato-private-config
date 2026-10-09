# Cheap validation before building

Choosing **the most dangerous assumption × the cheapest discriminating experiment** takes priority over a fixed order. Below is a ladder roughly from cheapest.

The core question is not whether to build but this:

> Which explanation does this confirmation experiment distinguish? Or, in which real experience does this exploration experiment find judgment criteria not yet known?
> Can the observed result change the next choice?

`validation` sets the claim, the competing explanation and prior PASS·FAIL.
`discovery` is a cycle that compares a specific experience and finds criteria, setting the exploration question·scene·observation method·safety and stop conditions.
Both kinds set the budget and allowed range in advance, and exploration completion is not reported as product success.

## 1. Check current behavior traces

Real work flows, search history·documents·spreadsheets, inquiries·support tickets, competing-service reviews, recent failure cases, the reason for doing nothing.

Prioritize **"how did you actually solve it last time"** over "I'd probably use it if a product like this existed".

## 2. Past-behavior interview

Do not ask for an evaluation of the idea; reconstruct a recent concrete event: when the problem last occurred / what you did first / whom you asked / which tool you used / when you gave up / whether time·cost·risk actually occurred.

A "I'd probably use it" about a hypothetical situation is heavily swayed by context and assumptions. Past behavior is stronger than a statement about the future.

## 3. Message·offer test

A concrete value statement + a concrete segment + a clear CTA + action (booking, providing data, file upload, requesting a consultation).

You must not claim that clicks alone prove purchase intent, but you can cheaply filter out **which message gets no response at all**.

## 4. Concierge / Wizard of Oz

A person handles it behind the system while the user experiences it as a finished flow. Useful for checking real input, trust, correction points, and how it hands off to the existing work flow.

However, where deception·personal data·automated decisions are involved, disclose the experiment scope and human involvement appropriately.

## 5. Thin code prototype

Code is the cheapest experiment when:
- Real latency or API feasibility is the core risk
- The options cannot be distinguished without experiencing the feel
- The technical integration itself is the value mechanism
- The prototype can be discarded
- For a confirmation experiment there are prior success·failure criteria, and for an exploration experiment there are the experience to compare·observation method·stop conditions

## 6. Commitment test

Costly action over words: providing real data, booking a schedule, migrating files, connecting a contact, approving a pilot, an LOI, prepayment, repeated use. But discounts·refunds·curiosity purchases may be mixed in, so compare the evidence within the same hypothesis.

## 7. Real pilot and outcome measurement

Treat the product idea as a hypothesis and set the evaluation criteria in advance. Short-term metrics like clicks·usage can diverge from the long-term outcome.

---

# Conditions where "let's just build it" is reasonable

Even though AI made implementation cheap, what got cheap is **the marginal cost of a demo·UI·one-off prototype**, not the total cost of correctness validation·integration·operations·trust. And **the cost of choosing what to build wrongly accumulates faster as AI gets faster.**

Implementation-first is reasonable only when all hold:

1. The prototype is a cheaper and faster discriminating experiment than other research
2. It states which explanation it confirms or in which real experience it finds judgment criteria
3. The use·non-use results change the decision
4. It can be discarded without external harm
5. It writes the confirmation experiment's success·failure criteria or the exploration experiment's observation method before the code, and in both cases sets stop·protection conditions
6. It does not automatically treat the prototype as the start of the product

Signals it is not reasonable:
- You are asking about demand but only check whether the demo works well
- You code because you do not want to define the user·trigger·current alternative
- One prototype can be attached to several conflicting problem narratives
- The organizer link and buyer value are still only words
- You first commit real data·payment·safety·legal promises

# Problem-first vs prototype-first

"Build only after fully understanding the problem" is excessive too. For uncertainty in the **usage experience**, a tangible prototype may be the cheapest research tool. On the other hand, uncertainty in **demand·purchase·current workaround** is hardly resolved by a well-working prototype alone. Choose the tool by the kind of uncertainty.
