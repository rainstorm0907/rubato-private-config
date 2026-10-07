---
description: Maplog map grouping is place first and capture-local day second. A cluster only tidies the screen and does not change membership.
---
# Maplog V2 place-first map, date-second Journey

- Date: 2026-09-02
- Context: Closed the physical-device gate for Stage 2 manipulation, capture-day occurrence, and the production timezone resolver, and discussed the next gate of expressing date scenes on the map before Stage 3 Recap.

Woojin, original wording:

> “날짜 장면을 지도에 제대로 보여주기 위해, 복잡한거 말고도 제일 중요한 사용자 입장에서는 : 같은 장소 1순위로 묶이길 원하고 2순위가 같은 날이야. 근데 지금같은 구조에서 하나하나 다 추가하기 솔직히 조금 귀찮은 상태거든? 이건 조금 대책이 필요할거같아. 외부 의견 들어봐야되나.. 'cluster를 ‘데이터 묶기’가 아니라 ‘화면 정리’로 바꿔야 해' 이건 진짜 필수야 꼭 해내야돼. 일단 stage3 조금만 뒤에 하자 이것들부터 제대로 완벽하게 끝내자 너가 말한것들까ㅈ지”

Current confirmed direction:

- Map grouping priority is same place first, same capture-local day second.
- A cluster is a display-only rule. It does not recompute Place, Visit, or Journey membership.
- Saved Journey add-one-by-one is not a 1.0 surface. Do not treat the fatigue note in the quote above as an order to build a bulk-add UI now. Scope is `record/PRODUCT.md`.

Rejected as still open: whether the map entity is a place, the selection unit a place×date visit, and a Recap section a day. That reading was settled as the model below. Also rejected as a current stop: keeping Recap locked until this model was finished.

Model settled after the outside review:

- Set it as `Photo → Place → VisitOccurrence(Place + capture-local day)`.
- The map entity is Place, the Journey's ordered selection unit is Visit, and LocalDay is an index and a bulk-add range that groups several Visits for viewing.
- Do not discard the existing day occurrence; demote it to date evidence and an index.
- DisplayCluster is a temporary expression according to viewport and zoom, and never takes part in Place/Visit/Journey identity or membership.

Woojin's decision for going to the same place again in the morning and the evening of the same day:

> “한 방문으로 보자”

Context: 2026-09-02, the point of deciding whether to adopt `Visit = Place + capture-local day` and a separate `VisitSession`. Therefore photos of the same Place and the same capture-local day are treated as one Visit regardless of the time gap, and the time flow is shown by the photo order inside the visit. Do not make automatic splitting based on time gaps.

Further progress decision:

> “ㅇㅋ 그럼 consult까지 나오면 내가 판정 해줄게 지금은 섵불리 판정하기 힘들다”

Distance defaults were later fixed by a real-photo verdict at 40m link / 100m width. See [[decisions/maplog-place-threshold-tuning.md]]. Do not keep the caution below as a ban on those numbers.

Context: 2026-09-02, whether to confirm the same-Place judgment policy and `r_v1` from synthetic/local analysis alone. A POI hierarchy was not adopted. Do not promote a new distance or a POI rule from a synthetic run.

same-session consult result:

- Completed the 2026-09-02 unbiased follow-up review in the existing `Maplog V2 전환 자문` conversation the user specified.
- Recommended not treating a coordinate result directly as a Place, and separating one layer further into `PhotoLocationObservation → PlaceInferenceProposal → 사용자 소유 Place → Visit → Journey`.
- The initial shadow inference puts a whole-diameter upper bound and a single-attachment condition for an ambiguous outer point on nearby-coordinate merging, and it recommended including user Place merge and split from the first version.
- Recommended labeling a Place partition of the surrounding area, not photo pairs, in a device-side Place Lab that does not send raw coordinates outside, and separating the tuning set from the locked verification set.
- Local synthetic analysis rejected connected-components chaining, fixed-grid boundary split, and the threshold sensitivity of full-library reclustering, and recommended a frozen-authority runtime that does not recompute a persisted Place.

User verdict:

> “어 그게 맞는거같아.”

Context: 2026-09-02, the point of confirming the following synthesis after comparing the same-session consult and the local synthetic analysis.

Confirmed Place policy direction:

- A Place is not a coordinate cluster or an external POI, but a persistent memory unit the user treats as the same place.
- A coordinate policy only makes a versioned `PlaceInferenceProposal`; it does not make Place identity.
- The first shadow analysis compares a compact inference that puts a whole-diameter upper bound and a single-attachment condition for an ambiguous outer point on nearby-coordinate merging.
- In the device-side Place Lab, the user looks at the photos and the map of the surrounding area, merges and splits the actual Place partition, then picks a bootstrap policy.
- Once a Place is confirmed, runtime does not recluster the persisted Place as a whole. A new photo attaches conservatively, or makes a reconciliation proposal.
- Treat a false merge as a more expensive error than a false split. User merge and split are not a 1.0 surface. If that screen is opened later, the succession rules are in [[decisions/maplog-place-visit-correction-lineage.md]]. Do not build them because this note once called them a basic feature of Place v1.
- Do not migrate an old date-bundle Journey into Place identity. Saved Journey is outside 1.0. See `record/PRODUCT.md`.
- DisplayCluster is a temporary object that organizes Place presentation in the viewport, and has no authority over persistence, membership, or Journey commands.
- The first implementation is one Place Lab, and meter values are not confirmed as product constants before a real-library verdict.

Implementation-start approval:

> “답변 오면 적당히 이제 수정할거 수정하고 굳힐거 해서 구현들어가보자 내 응답은 ㅇㅋ. 에이전트 안 헤매게 잘 교정해줘”

Context: 2026-09-02, prior approval while Anthropic Opus 5 independently audits the Place Lab success criteria and the implementer contract. When the answer arrives, the lead corrects the gaps and conflicts found, fixes it as an implementation contract that separates binding law, hypotheses, and user-verdict points, then enters Place Lab implementation without waiting for further approval. Do not let the agent arbitrarily decide meter values, Place meaning, the privacy boundary, or the merge/split scope.

The Place Lab UI is not the product. Meter values other than the confirmed 40m/100m defaults are not product constants. Do not keep a Stage 3 lock from this note.
