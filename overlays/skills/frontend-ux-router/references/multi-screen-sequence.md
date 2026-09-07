# Multi-screen sequence

Read this when the work is three or more surfaces built over more than one session, with one user judging them. A single screen does not need it; `frontend-creation.md` covers that.

The rule behind everything below:

> A surface only tunes fast after its role sentence has survived one user verdict. If it has
> not, you are tuning a guess.

Measured on two projects with the same lead: the one that shipped put the user on the rendered screen almost every turn and kept locked values as code; the one that failed kept the same rules in documents and showed the product on 6 of 14 days.

## Before the first screen

1. **Write the verdict vocabulary first.** In the design document, before any screen: five or six "good impressions" the product must give and five or six "failed impressions" it must never give, in the user's own words (for example: "feels like a bright desk", "feels like a review screen", "card inside a card"). Every later verdict from the user should map to one of these lines. When a verdict does not map, add the line before fixing the screen. If no design document exists, this is the first artifact of the project: write the two lists and get a one-line confirmation before the first screen.
2. **Agree mood on images, not code.** Three generated images, one variable each (mood, scale, whitespace), user picks. Record the winning sentence in the design document. Later code variants must not move the mood; if one does, that is the defect, not a new option. If you cannot generate images or cannot reach the user this turn, do not substitute code exploration: return one written mood sentence plus a reference and stop there.
3. **Freeze as checks.** Anything the user locks (a number, a feel, a composition, a copy line) is protected at the strongest level available and marked with source and date at the definition site; see non-negotiable 12 in `SKILL.md` for the levels and for what to return when no check can be written. Documents do not protect frozen things; checks do.

## For each new surface

4. **Write the surface's role sentence** before composing: what this surface is for, in the user's words, one line. ("This is where the user reads their own story back, not where they check 16 boxes.") The path card covers the product; the role sentence covers this one surface.
5. **Expect the first version of a new role to fail.** Build it at the normal quality bar but at the smallest scope that shows the role: one screen, one state, real content. Its job is to get the role sentence past the user, not to cover the surface. Do not tune a surface whose role sentence has not survived one user verdict; tuning a wrong role produces a polished wrong screen.
6. **Once the role survives, only tune.** Do not re-derive the frame. If a later turn wants to change the role, that is a new surface with a new sentence, and the user decides.
7. **Cut the judgment unit before showing.** One screenshot, one line, one tone, one spacing. Ask the user to point at the exact spot ("this line", "this gap"); fix only what was pointed at. A large judgment unit ("here is the whole flow, what do you think") produces a large, slow, and vague verdict.

## Between surfaces

8. **The user sees every surface before the next visual change to it.** This is a rhythm, not a final gate. If the user has not seen the rendered result of the last turn, the next action is to show it, not to build more. For a dispatched worker this means: stop at the first state that renders correctly enough to be judged (fixing your own errors to get there is part of the same turn) and return with screenshots; do not continue to "finish" the surface unseen. That return is a completed turn, not an empty one.
9. **Two rejections on feel means the role is wrong.** "Cluttered", "messy", "feels copied", "feels like a feature": on the second one for the same role sentence, stop tuning and go back to step 4. The count resets when a rewritten sentence passes.
10. **Nothing outside the agreed composition.** New surfaces or content added because they seemed helpful (banners, disclaimers, picker screens, explanations, states for flows the path cannot enter) are defects. Reachable states of the path are part of the composition. Report the idea; do not build it.
11. **Comparison chooses parts, not winners.** Present variants so the user can take the body of one and the copy of another. Do not build one variant to completion in the hope of whole adoption.

## Reporting to the user

12. **Screenshots with absolute paths, or a live URL, and the two or three points to judge.** No command logs, test counts, or file lists. Machine checks go in the dispatcher report with their scope written next to the PASS. With one output channel, use two headings in one return (`## For the dispatcher`, `## For the user`). The user report has one purpose: let the user judge in under a minute.
13. **Say which state each thing is in**: connected, implemented, checked, deployed, or not yet known. Never blend them into "done".

## Notes

Where the failed project broke: rules written in documents the worker never received, and a task in the brief that conflicted with a rule, so the task won. A frozen value left in a comment while the mechanism under it was replaced. A green contract check, an automated walkthrough, and a one-word `Ready` standing in for the user's verdict. Thirty-four sessions of worker briefs between six days of the user actually using the product.
