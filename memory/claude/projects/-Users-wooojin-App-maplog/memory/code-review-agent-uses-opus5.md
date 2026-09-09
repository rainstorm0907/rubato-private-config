---
name: code-review-agent-uses-opus5
description: 코드 리뷰용 서브에이전트는 Fable 상속이 아니라 Opus 5(medium)로 명시 지정해서 돌린다
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e5100df7-a113-4626-b0ef-fd126a7ca53a
  modified: 2026-07-28T10:31:18.140Z
---

코드 리뷰를 서브에이전트(reviewer 등)에 위임할 때 모델을 상속(Fable)으로 두지 말고 `model: "opus"`(Opus 5, medium effort)로 명시 지정한다. 2026-07-28 우진 지시.

**Why:** Fable 자동 상속으로 리뷰가 돌아가는 걸 원치 않음 — 리뷰 작업은 Opus 5 medium이면 충분하다는 판단.

**How to apply:** Agent 도구로 reviewer를 띄울 때 `model: "opus"`를 항상 넣는다. 코드 리뷰 외 작업에는 해당 없음.
