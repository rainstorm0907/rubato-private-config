---
description: General lessons for agent workflows — extracted from the toyrocket v2 failure (2026-08-28). Refer to this before writing a brief, designing verification, or running workers.
---
# General lessons for agent workflows

Source: toyrocket v2 human-play verdict FAIL retrospective (2026-08-28, openaigame hackathon).
Status: user confirmed — "앞으로 범용으로 써야할 필수 교훈인거같아. 이거 나중에 어떻게 세팅 + 내 습관 만들지 고민해보자".
Current scope of application (v0.4-r2 wording; for what is actually applied, see the install record): what follows is a case that preserves the failure at the time and the original wording. Do not reapply the prescriptions of that time, such as "유일한 센서", "자주 참여", and "인간이 표준 순서를 소화", as execution rules for every task. The owner finds conception and production methods in the materials and prepares them, then continues the allowed follow-through while looking at the actual result. Experience only the user has is judged together, but basic preparation and checks are not handed off. Current behavior is owned by `system/working-rules.md`, `dispatching`, and `frontend-ux-router`. Existing protection conditions and meaningful checks stay. This case does not require a separate supervisor, a periodic audit, or a fixed production order.

Wording the user asked to record (original kept):

1. **"막힐 때마다 자기가 확실히 잘하는 일로 도망친"** — When stuck, an agent drifts into work it is reliably good at, such as organizing documents, building a validator, and infrastructure. Distinguish output growing from the product getting better, and the lead has to stop this gravity.
2. **"대리 지표를 에이전트가 스스로 골랐다"** — A proxy metric for unmeasurable quality (feel, readability, control feel) must be derived from a human verdict. Make the metric after a human has felt it and said so. If the order is reversed, the metric becomes self-certification.
3. **"핵심 품질 신호가 에이전트한테 없는 채널이면 경고"** — If the product's core quality arrives through a channel the agent cannot sense, such as real-time feel, the human is not the final approver but the only sensor. Do not use the sensor once at the end; put it in the loop often.
4. **"개발의 표준 순서 — 뭘 먼저 만드나"** — When entering a new genre or domain, investigate first "이 분야 사람들은 뭘 먼저 만드나" (consult and so on). The human writes the brief after digesting the standard order. (Games: greybox → playtest → art.)
5. **"에이전트는 재료의 품질을 올려주지, 재료 투입 순서를 바꿔주진 않는다"** — Competence with the wrong order makes the wrong thing faster and in greater quantity. The frame and the order are the human's and the lead's responsibility.
6. **"같은 표면을 두 번 튜닝했는데도 아니면 계층을 의심한다 — 있었는데 적용 안 됨"** — A rule already in [[system/working-rules.md]] was not applied in v2 (a proven engine plus a map editor should have been used instead of a custom canvas engine). A rule does not work merely by existing. Check it explicitly at the moment of choosing the layer (deciding the stack at start).
   - 2026-09-07 addition (contrasted with 온전's success): On toyrocket, the physics freeze, the camera contract, HUD C, and "검사 PASS ≠ 보기 좋다" were all in the documents and all were broken. Only `stage1-world.json`, which was enforced in code, survived. The condition under which a rule worked was not the quality of the rule but ① how often the user looked at the screen (온전 every day / toy 6 of 14 days, the other 34 sessions were one turn of a worker brief), ② whether what was locked was a check, ③ whether the brief carried the freeze list. Three mechanisms break rules: the document is not in the worker's context / when the task and the rule conflict, the task wins / prose is caught by nobody. The response is Skill(dispatching)'s frozen items and return column, and Skill(frontend-ux-router) rules 10~14.

## Related open structural problems

- A worker structurally has a narrow view (the "좁은 시야로 비판받기" problem). The narrowness itself is the design and is not a fault. The bug appears when a narrow PASS is promoted to a product PASS without translation. A solution has been proposed and is under discussion (separating a frame-audit role, obliging the worker brief to report doubted premises, obliging the lead to translate the verdict).

## When a long delegation breaks in the runtime (a lead lesson, not user confirmed)

Source: Maplog Recap collection app port, 2026-09-25~26. The owner on the same route (`anthropic/claude-opus-5-5-sub`) ended more than six times on timeout and connection errors, and a revived (AgentSend revive) session died immediately twice on a 'stale ctx' runtime error.

- If a revive dies on a runtime error, do not keep reviving the same session; start a new session with the handoff material. If it repeats on the same route, model and route choice is the user's, so ask for the cause and the candidates and change it (Woojin: "Opus sub 말고 일반으로 해줘", 9/26).
- Put "단계 하나 끝낼 때마다 진행 기록 한 줄" in a long delegation brief. One owner edited five files for 75 minutes with no record and then broke, so the next owner had to take over without knowing what was finished. When it breaks, first take a copy of the files at that moment.
- If the broken owner had already finished the build, the lead does only the install and the check directly, instead of a new session, to cut the handoff cost.
- Before passing the user's short choice ("2번", "3,4,8") to the owner, ask back in one line what was understood. "월은 2번" was misread as a pill in every month cell, and one version was thrown away (the user's intent was one guide line under the month row).
