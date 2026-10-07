---
description: The user's verification result of the 2026-09-02 Maplog V2 real-iPhone restart round trip, and feedback on the date gallery, duplicate numbers, and clusters.
---
# Maplog V2 restart round-trip on-device feedback

Date: 2026-09-02
Context: On a real iPhone 14, made 188 real PhotoKit photos into 7 persisted capture-day occurrences, saved 3 Journeys, then verified force-quit and icon relaunch.

## User confirmation — verified

Woojin:

> “첫 Journey 날짜 근처 카메라가 맞고, Journey 3개와 1·2·3 번호도 잘 돼.”

The same occurrence store was restored after relaunch as 7 occurrences, 188 assignments, and a Journey order of 3, and the user directly confirmed the on-screen order, numbers, and first camera.

## Product feedback — user observation

Woojin:

> “일단 여정 날짜 단위로 나눈거 좋은데, 지금 보니까 거리가 너무 먼거까지 되니까 살짝 당황스러웠어. 왜냐면 아직 사진은 날짜별이 아니라 그냥 전부 나열되어있어서 그런거같아.”
>
> “자연스러워지려면 나중에 하기로 하긴했지만 그거 있잖아. 사진도 날짜 단위로 묶어서 갤러리 식으로 볼 수 있고, 클러스터도 전에 피드백 받은대로 수정해보면 괜찮을 수도 있을거같아.”
>
> “근데 지금처럼 2가 두개로 중복처럼 보이는건 혼란이라 좀 확실히 정할 문제인거같아.”
>
> “클러스터는 아직 여전히 변동적으로 발동중인거 확인했어.”

- Per-date Journey direction: the user liked dates as the unit, and disliked a gallery that still listed every photo flat, and a Journey number that looked duplicated.
- The place gallery now splits that place's photos by day. See `record/PRODUCT.md`. Do not treat "not implemented yet" as current.
- Do not repeat one Journey number on every member photo. Saved Journey is outside 1.0, so do not reopen a number-badge design from this note.
- A cluster whose membership and count change with zoom was rejected again here. The current rule is display-only. See [[decisions/maplog-v2-date-scene-groups.md]].

## Lead responsibility record

The restart implementation brief required projecting the persisted occurrence number onto every member marker, which created the duplicate numbers. Separate from save and restore correctness, it is a failure in which one date occurrence is not read as one Journey node on screen, and an item the lead missed in the checkpoint design.
