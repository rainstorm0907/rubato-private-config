---
description: 2026-08-31 우진이 두 Consult 문서를 Maplog seed-first 구현 지침으로 승인하고 단계별 실행을 허용한 결정.
---
## 결정

- 상태: **사용자 확정·구현 착수 승인**
- 날짜: 2026-08-31
- 맥락: `/Users/wooojin/App/maplog/.consult/maplog-seed-first-swift-followup-response-2026-08-31.md`와 `/Users/wooojin/App/maplog/.consult/내가 받아온 consult.md`를 구현 정본과 운영 번역으로 삼아 다음 단계를 정하는 자리.
- 우진 원문: “거의 저 문서가 완벽하기 때문에 저대로 행동하면 될거같아. 단계별로 쪼개서. 목표에 도달하기 위해 억지로 하거나 끼워맞추기 금지.”
- 우진 원문: “사용자 답변은 동의하는걸로 간주해.”

## 적용

- seed-first Journey 방향은 추가 추상 기획 질문 없이 단계별로 구현한다.
- 각 단계는 저장소 사실과 runtime 증거를 통과해야 다음 단계로 넘어간다.
- production pin→stable SceneID, 동일 NMFMapView 유지, 영속 photo identity 중 하나가 자연스럽게 성립하지 않으면 억지 adapter나 임시 ID로 통과시키지 않고 구조를 재판정한다.
- 후보 도움, Recap motion, export, social, root-tab 개편은 기본 Journey 왕복과 PhotoKit 첫 실행 뒤에 둔다.
