---
description: 2.5D expression rules for the openaigame rocket game — draw a wall opening as a parallelogram, not a front-facing rectangle.
---
# openaigame — 2.5D expression rules

> **프로젝트 종결 반영 (2026-08-28):** 평행사변형 개구부 규칙과 마지막 `교훈`은 우진이 확정한 재사용 가능한 미학/해석 규칙으로 **생존**한다. `관련 수치 (B2 시점)`과 production 과제는 닫힌 v2 이력이며 후속 과제가 아니다.

## A wall opening is a parallelogram

Status: **user confirmed (2026-08-26)**

Woojin's utterance: "2.5d에서 다가오는 옆면 벽에있는게 그렇게 보이잖아 (…) 대각선으로",
and, when confirming, "평행사변형 맞아!! 내가 말하려던거야. 앞으로 이런 2.5d 스타일은
나중에 디자인 입힐때 꼭 참고해."

- Do not draw a **wall opening** such as a window, door, or hole **as a front-facing rectangle (a frame).**
  It is a hole cut in a side wall that recedes in depth, so it reads as a **parallelogram** whose top and bottom edges are slanted.
- Drawn as a front-facing rectangle, it reads as "벽에 걸린 그림", not as "벽에 뚫린 구멍".
  In fact the B2 window was made as a front-facing rectangle, and this correction followed.
- This rule applies not only to the B2 ghost stage but to **all later C production art**.

## Related numbers (as of B2)

- Window size: keep the width `900`, height `2043` (2.8× the previous B2 720). Height/width ratio `2.27`.
  This ratio was measured from a screenshot box Woojin drew and sent.
- The earlier document's "가로·세로 2배(1800×1440)" was discarded because the ratio reading was wrong.
  The cause was making it close to a square from the wording alone.
- **Slant direction: the nearer left jamb is higher and it falls off to the right.** The craft goes left→right,
  so the window's left edge is closer to the camera. Draw the nearer jamb thicker.
- Raised the window by `0.5개(1021px)` of the window height, and raised the curtain on the window and the airship flying through the window with it,
  keeping one structure.

## Not done yet (production work)

The slant flips while passing through. Approaching, the near side (left) is higher; at the moment of passing it gets close to a front-facing rectangle; after passing, the other side is higher. That makes the sense of "옆을 스쳐 지나갔다". In B2, because of cost, it was left as one fixed slant, and it is implemented in C production, which puts in real parallax.

## Lesson

Measuring **the actual ratio of the picture the user drew and sent** is the source of truth, over a scale phrase in a document ("2배").
A scale is ambiguous about which axis it is based on, but a picture is not.
