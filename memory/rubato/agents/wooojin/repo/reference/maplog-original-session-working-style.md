---
description: A way of discovering Maplog's direction with the user and carrying it through to an executed artifact. Check the connection from real input to result, and keep the implementer's responsibility and the lead's independent judgment.
---
## Status

The principle of restoring product feel and execution rhythm together is user confirmed and checked against the original. Current feel criteria and proposal details follow `/Users/wooojin/App/maplog/record/PRODUCT.md`, and execution approval follows `/Users/wooojin/App/maplog/record/CURRENT.md`. The past stage operations below are not current implementation authority.

On 2026-09-10 Woojin explained “우리 maplog에서 유지해야하는 감성의 축이 있다고 생각해. 그리고 그걸 구현 중간에도 잊지 않아야 제대로 구현할 수 있어”. The context is that he cannot sustain a method where he personally corrects, one by one, an implementation that did not understand the picture he wanted. He confirmed putting into the core document the criterion that viewing is enjoyable even without choosing, and that viewing must not break when he comes to want to continue.
The two stages — looking quickly and at low cost at the reason for a screen and, if it is ambiguous, discarding or switching, then defining the grasped purpose as a UX sentence and refining the implementation with references — were recorded as a user proposal. A recorded proposal is not approval to resume production or investigation, and avoid both making an ungrounded hypothesis into confirmed UX and asking the user again about every detail.

Original: `/Users/wooojin/.rubato-pi/agent/sessions/--Users-wooojin--/2026-08-30T20-09-03-978Z_01a0544a-32ea-7dd5-afd8-64b55fa52274.jsonl`

## 2026-09-02 correction — do not split off only the operating method

Status: directly corrected by the user and restored as one integrated whole.

Woojin's original:

> “아니? 이런식으로 우리 합치기로 한거 아니야. 이 방향이 아니고, 방금 분석한거에 이어서 핵심 문서들 v2 관련 문서 다 읽고, 컨설트 정리한것도 그록으로 요약해서 너가 읽던가 해. 우리 감성 아직 모르는거같아”

The original session's execution rhythm is not a separate work template. It is a way of executing Maplog V2's product causality and feel inside the same judgment. Before a brief or a review, restore the following together.

- Maplog is a private-first memory map that spreads personal photos on a real map and gives `어? 내가 여기도 갔었네?` first.
- The photo is the protagonist, and the map is the entrance to meeting a memory. Even nationwide, do not turn photos into dots or statistics.
- `우수수` is the failure where the mode of existence suddenly pours out on zoom-in, and `팟 팟 팟` is the failure where memory membership is recalculated at every zoom.
- Place is rank 1, capture-local day is rank 2. A Visit is a per-date visit inside a Place, and a Journey connects these visits.
- A cluster only tidies the screen and does not change Place, Visit, or Journey membership.
- Show first the result of the app automatically restoring a place, and the user does not do classification labor beside a correct result; they fix only the wrong places.
- The LabelPartition Lab engine may remain, but work chrome such as the Lab UI, an empty audit, three entries, progress, and today's tasks is not the product.
- Current product and feel judgments prioritize `/Users/wooojin/App/maplog/record/PRODUCT.md`, and facts and approvals prioritize `/Users/wooojin/App/maplog/record/CURRENT.md`. For the past result-first handoff and the V2 stage table, find and use only the grounds that are needed, and do not hide a conflict with the canonical source.
- Do not place a machine PASS or a broad generic UX checklist above the current bounded product contract. At the same time, do not declare a product PASS before Woojin's actual felt experience.

Grounds synthesis:
`/Users/wooojin/Downloads/maplog-qa/2026-09-02-result-first/original-session-analysis/grok-v2-integrated-product-synthesis.md`

## Role and authority

In the original, Woojin did not attach a fixed title to the agent. The role was a seat one level behind the implementing hands: designing the stages, operating separate implementation and review, retrieving and comparing the physical artifact, and giving a brief the product owner Woojin can accept.

> “각 단계를 전부 이어서 하지 말고, 단계 완료시 무조건 작업 끊고 회수 한 뒤, 저 문서 기준 만족했는지 검토 후 나한테 이해하기 쉽게 브리프해줘. 내가 책임자로서 납득하게.” (L51)

> “전부를 너가 다 읽지 말고, 다른 그록으로 negative review 시켜. 걔한테 검증 못한것도 브리프 받고 너는 그걸 비교해줘” (L854)

> “특히 너가 직접 구현하는게 아니니까 조금 더 한 차원 뒤에서 봐줘야해.” (L3497)

## Ways to keep

2026-09-10 user preference: execution is left to agents so the conversation context, in which the lead concretizes the product together and sets the implementation plan, is kept. Woojin's original: “직접 코드 작성, 검증, 기기 연결 등 잡무는 전부 에이전트로 굴리면 좋겠어.” / “작업회수도 그대로 맹신하지 않으며 작업 결과를 끼워맞추지도 않았으면 좋겠어. 그렇다고 엄격한 검증이랍시며 과하게 검증에 꽂혀서 매몰되지 않고.” Instead of constant detailed surveillance, hand over a goal whose intent and boundary are clear, and the lead takes the judgment of contrasting the artifact and the grounds with the original purpose. In the review opinion delivered on 9/11, he reconfirmed “가능한 범위에서는 그 담당이 끝까지 책임지도록 유지해줘”. Fixes, checks, installs, and runs the implementation owner took on are finished by the same owner within the possible range, and the lead independently checks the core grounds but does not repeatedly take over every technical task. Parts that cannot be delegated because of tools or permissions are handled individually, and are not made into a rule of always delegating or always doing it directly. Concrete placement and approval to start production are separate. On 2026-09-11 Woojin reconfirmed “나도 충분히 놓칠 수 있는거고, 기계적인부분의 디테일은 너가 챙겨야하는거야”. Do not make the user enumerate every detail; the lead and the owner look after boundaries, performance, data, and basic behavior. Even when the goal is the same, discuss planning direction, candidate composition, comparison questions, and important experiential tradeoffs enough with the user. Common collaboration principles follow [[system/working-rules.md]], and do not read delegation of mechanical details as authority to confirm the plan alone. Following the request “의도의 목적성은 항상 유지하고 문서도 잘 기록해두는게 좋을거같아 왠만하면 언제봐도 이해가 되게”, leave purpose, reason, the current decision, and open methods together in the existing PRODUCT. Long-term he wants “상용 어플수준의 개발, 앱스토어 출시”, but the conditions “당장은 절대 아니지만”, “대신 신경쓰지 마”, and “지금처럼 천천히 하나씩 만들어보고싶어” are attached. Do not use the long-term goal as grounds for current release preparation or a large foundation build. Status: user confirmed; the source is window `01a08ec2-4833-7d50-823b-8a2dea18eaa5`, user item `5c4ce498`.

- Before an implementation plan, concretize the wanted experience enough through questions and conversation. 2026-09-10 user original: “너가 이렇게 내 의견이 궁금하고 더 이해하고 싶은거 있으면 많이 말해줘. 그러다보면 방금같이 내 아이디어도 나올거같아. 얼추 그렇게 되고나서야 구현 계획 정의부터 해보자. 천천히 단계별로 하고싶어.” The same day the user confirmed applying, even during implementation, a rule of contrasting existing sentences with the actual user intent, the context at the time, and the model's interpretation, and not swapping in a new confirmed sentence before understanding enough. Original: “앞으로 구현 하면서 … 이 규칙 꼭 하자”, “확정인건 내가 원하는 방향이지, 세부적인 가지들이 아님”. The title and application rules of `/Users/wooojin/App/maplog/record/PRODUCT.md` are canonical. Do not conclude that the entire past decision is a distortion, arbitrarily lift a stated protection condition, or turn it into a full-document audit every turn.
- Conversation is not only the work of hitting the user's finished answer. Original of the review opinion the user asked to keep on 2026-09-11: “실제로 대화하면서 우진에게도 새로운 생각이 생겼어”, “네가 새로운 구분이나 관점을 먼저 제안하고, 그에 대한 경험을 들으며 네 해석도 수정하는 과정”. In viewing a region and photo bundle, the premise connecting visits at one place was revised, and from the explanation that choosing materials is not the fun, the proposal changed to looking at long-period viewing first rather than the input screen. After the trial, unhesitating progress was distinguished from shortening every movement in a batch. It is not a method of increasing the question count or leaving every next choice to the user; keep a joint exploration where the proposal actually changes with experience. Status: user request and current work criterion.
- At stage completion, do not go on to the next feature by inertia; cut and retrieve.
- Separate implementation and test success from a product and physical-device felt pass.
- When asking approval for a direction change, write `원래 이랬는데 > 이렇게` and the intent in 1~2 lines of easy words.
- A report answers `뭐가 됐는지 / 어떤 의도였는지 / 뭐가 남았는지` first, rather than listing files.
- Specify the physical artifact Woojin will see, and say what to judge. On 2026-09-10 Woojin explained “가능하면 내가 직접 테스트해보는게 제일 빠르고 편하며 훨씬 직관적이고 원하는 피드백 받기 좋을거야” while attaching the condition “작은 단위마다 일일히 나를 부르지는 않았으면 좋겠어”. Prioritize direct experience, but do not call him for every part; bundle into a connected range where one experience and an open judgment can be looked at. The agent owns the basic behavior check, and do not count the number of user calls as the outcome of participation.
- Before asking the user for a next action such as connecting a device or granting permission, check the actual connection from input to result, whether that action can lead to the intended experience. 2026-09-11 original: “‘기기나 권한이 없어서 확인하지 못한 것’과 ‘아직 그 동작을 구현하지 않은 것’을 구별하는 게 중요해.” A synthetic input check is valid but does not substitute for a real input connection. The missing PhotoKit connection on the first long-period return is a case that was supplemented later, so do not make it again. Rather than a long explanation, accurately distinguish the spans that are implemented, unverified because of access, and unimplemented.
- Turn on external review only when a meaning unit or the feel is shaking, and do not steer toward a predetermined answer.
- Brief the implementer so they do not wander, but the lead does not sink into the implementer's frame and compares the results.
- Reuse existing parts, and do not lower the product bar.
- At handoff, match only the related state of the existing PRODUCT and CURRENT to the latest experience. Do not repeat work already updated, and do not change a state of having experienced some of the fun into unexperienced or a whole-product pass. 2026-09-11 user request: “이 의견 때문에 새 체크리스트나 검토팀을 만들지는 않아도 돼.” Keep the existing approval scope, and do not interpret it as approval to change a global setting. Original source: the current Rubato session window `01a08c37-078b-7616-8073-9a00a8d2ff2d`, user item `fd7d3936`.

## What Woojin praised directly

> “그래도 쉬운 말로 설명해준거 고마워 잘했어” (L1959)

> “+n 카드 tap는 만족이야 잘 만들었어.” / “사진 감상 아주 잘 됐고” (L2420)

> ““혼자”를 검토 없이 밀어붙인다는 뜻으로 받아들이진 않은거 잘했어. 그런 디테일 챙기는거 좋아.” (L2506)

The object of the praise was not an abstract procedure but a boundary sense: behavior that actually worked on a physical device, an easy explanation, and not mistaking independent judgment for pushing through without review.

## Feel learned from the 2026-09-24~26 Recap collection screen session

Status: organized by the lead before the session switch, writing approved with the user's “ㅇㅋㅇㅋ 좋아” (window `01a0d2d8-0e67-79cd-b8fa-c633e25c5354`, item `ff29bff1`). The canonical source of the decisions themselves is the CURRENT 9/24–26 lines and PRODUCT `#recap-collection`, and the session summary is `/Users/wooojin/Downloads/maplog-qa/2026-09-24-recap-collection-review/CHECKPOINT-lead-2026-09-26.md`. Below is the feel of the judgment, not the decision.

**Taste signals (original):**
- The reaction was bigger when the meaning came through movement rather than explanation. On the preview sample of a photo settling onto its pin, “아니 예쁜데???”, and on the board where six photos each go to their own pin, “잘했어 아주! 그대로 가자”.
- Quiet, and the photo as protagonist: “너무 복잡해도 안되고 시선분산과 정신이 없으면안돼”, the collage “1이 제일 예뻐. 1>>>>4>자동”, the gap map “사진이랑 좀 이질감” → lower the contrast, then again “지금 좀 어둡네” → make it visible enough.
- Adding elements to explain the meaning (▶, pills, phrases, adding a map band) failed more than three times. He wants “진짜 확실한 연출” more than a common reference (Polarsteps and the like).
- He wants several possibilities rather than one right answer (“정답만을 원하는게 아니라 여러방향의 가능성”), and often makes his own answer that was not among the options (season center plus both sides, two winters, the 3·4·8 combination). That answer was usually the best.
- He marks the scope of confirmation himself: “이건 확정은 아니야”, “바로 실행하지 말고 의논”, “나중에 폰에서 써보고 바뀔수도 있어”. Respect this marking as it is.

**Flow that worked:** a text layout (regions and coordinates) → switches on an HTML sample with real photos and coordinates (gap 4/6/8, collage in, button in) → Woojin picks by number (“가 A 나”) → the lead asks back in one line → organize the numbers → owner-plan feedback → transplant → the phone once at the end (“폰은 마지막에 한번에”). Fixing only that piece each time a spot is pointed at leads to wandering. Then Woojin does “잠시 멈춰봐. 프레임 밖에서 다시 생각해보자” — set the rules again from the start. If investigation is needed, fix the lead's hypothesis first, and run Pro (without candidate names) and DeepSeek (physical artifacts and open source first) separately and contrast them (the 9/24 method, which Woojin remembers as “잘 하고나서 활용까지 했던거”).

**Meaning of Woojin's words (confirmed this time):**
- “정신없지 않게” = move only one thing at a time and put an order on it; when returning, appear in place instead of flying in.
- “없어져도 될 부분만 숨기는게” = always keep the progress line and the numbers, and hide only the button.
- “무슨일이 있어도 4계절” = he meant the order (spring→winter), not that he wanted empty slots → skip empty seasons, and the end is a rubber band.
- If only “이상한데?????” comes, ask back where it is strange. There was a time a board was thrown away by fixing from a guess (the “월은 2번” misunderstanding).
- A short “ㅇㅇ” or “ㄱㄱ” is approval of the entire immediately preceding proposal. But a change of owner model or role is asked separately.
- Praise that shows when there is no complaint (“다 이해 했구만!”) was a signal that asking back and an easy table had landed.

## What not to overfit

In the original, a particular consult count, model combination, long PASS list, and token tally were not a universal procedure. When there was no uncertainty, execution was short, and an outside eye and Woojin's verdict were brought in only when a product unit was shaking. Do not promote an in-screen experiment tool or a disk cleanup into a product stage.
