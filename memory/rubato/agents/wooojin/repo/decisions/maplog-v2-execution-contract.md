---
description: What still binds Maplog map expression, and which old stage locks are not permission to stop or start work.
---

## Conclusion

- Product meaning, 1.0 scope, and open judgments live in `/Users/wooojin/App/maplog/record/PRODUCT.md`. Facts and who does what live in `record/CURRENT.md`. The work method lives in `AGENTS.md`. This file does not lock a stage and does not authorize starting work.
- Design structure, performance, UI, copy, empty states, permission, error, and delay for real App Store users, not for the current phone's photo count. That count is a repeatable regression fixture, not a budget or a ceiling.
- At nationwide scale, every located photo stays at its own coordinate. Do not filter or sample the distribution away. A cluster only tidies pins that actually touch on screen. It is not a regional summary and it does not change Place or Visit membership.
- The thing the user sees, even far out, is a real photo, not a field of tiny dots. How a pin says "many photos" is the current pin contract in PRODUCT, not a number badge.

## Rationale

- Chose App Store scale as the design assumption. Woojin: “이것 외에도 제품 구조는 App Store 규모를 기준으로 설계라고 가정해서 앞으로 구석구석 해야돼. UI/Ux , 멘트 같은것까지. 혹은 mock으로 대체되어있는 후보라던지.”
- Chose preserving exact locations over a readable thumbnail of every photo at once. The approved direction was `모든 허용 사진의 실제 좌표상 공간적 존재와 접근성 보존`, not `모든 썸네일 동시 가독성`. Woojin: “전국 단위로 봤을때 합쳐진게 아니라 정확한 위치에 여러개 필터없이 다 보여지면 좋겠어.”
- Rejected: a native cluster that poured markers out on zoom-in (“우수수”) and merged and split at a low frame rate. Also rejected: hiding markers so a far view looks sparse and a zoom suddenly reveals them. Cause was fixed-size markers covering the same screen pixel, not real grouping.
- Rejected: a nationwide view of only 3–5pt dots. Woojin: “멀리서 볼때 사진이 안보이면 뭘 보고 무슨 사진인줄알고 어케눌러?? 그리고 우리 감성 무너지는거 아냐”
- Rejected as a current stop: “do not start release preparation”, the Consult-before-any-code gate, and the Stage 3 lock. On 2026-10-01 Woojin authorized finishing 1.0 (“일단 그렇게 1.0 마무리 해야할거같아”). Scope and what waits until after 1.0 are in PRODUCT, not here.
- Rejected as the default pin language: `+n` as the hidden-photo count. Later pin verdicts dropped number badges. Do not revive them from this file.
- Reuse a verified implementation narrowly when a whole old file is coupled to a retired domain. Do not invent a shared framework first, and do not replace verified native behavior with a stand-in. Woojin: “v2 좋지만, 재사용할건 하고 효율적으로 개발하되 그 문서의 기준은 엄격하게 달성할수 있도록하자”

## Symptom

사진이 멀리서 볼때 적게보이다가 갑자기 확대하니 우수수. 심지어는 엄청 멀리있었는데도 합쳐보이던 문제 발견했어
