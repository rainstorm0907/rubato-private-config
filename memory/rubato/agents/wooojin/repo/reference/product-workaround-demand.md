---
description: A product-design lesson drawn from MapleStory patch cases — the criterion for reading a repeated risky workaround as demand for a missing primitive and absorbing it as a safe first-class capability.
---
# Designing to absorb workaround demand

## Status and source

- Drawn on 2026-09-01 from a MapleStory patch case analysis.
- 2026-09-02, Woojin: “우리 메이플의 교훈을 얻었잖아.”
- Status: user-confirmed lesson / promoted to durable memory / skill and global placement under review.

## Core

> 반복되는 우회는 누락된 primitive의 신호다. 우회법의 위험한 수단을 그대로 기능화하지 말고, 사용자가 위험과 비용을 감수하며 얻으려던 결과를 안전한 일급 capability로 만든 뒤 권한·한도·가격·감사를 붙인다.

Decompose an observed workaround as follows.

```text
관찰된 우회 = 정당할 수 있는 목적 + 위험한 수단 + 제품에 빠진 제약 처리
```

Before repeating a block, ask:

1. What result did the user actually pay money, time, and risk for?
2. Does a legitimate purpose remain after the risky means are removed?
3. Can that purpose be expressed as a first-class capability of the product?
4. Is the official path clearly superior in safety, convenience, recovery, and audit?
5. Does the official feature replace the existing workaround, or combine with it to make a stronger abuse?

## What to design

- Least privilege and role scope
- Daily and weekly caps and rate limits
- Activity, settlement, and audit logs
- Cancel, recovery, and dispute handling
- A metric for whether the official path actually replaced the unofficial path
- A metric for combined abuse of the official feature and the existing workaround

## Conditions for not productizing

- The desired result itself harms another user
- Officializing grows fraud, spam, or market distortion
- It damages the core experience for a few users
- The cause is a temporary bug or a price error, not demand
- Structural complexity and support cost are larger than the value absorbed
- The official feature only raises the productivity of unofficial operators

## Neighboring principles and the difference

- `laws` changes the implementation structure so a wrong state is unreachable.
- This lesson discovers a missing product capability from repeated user behavior.
- `reframing`, when repeated blocking fails, switches the question from “어떻게 막나” to “무슨 결과를 원했나”.
- `framing` verifies the discovered result as the current alternatives, comparison value, harm metrics, and an experiment contract.
