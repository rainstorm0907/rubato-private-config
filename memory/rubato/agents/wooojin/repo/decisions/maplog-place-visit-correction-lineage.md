---
description: User confirmation of Maplog Stage 2.5 Place and Visit merge, split, and Journey succession rules, and of the need for a separate UX verdict.
---
# Maplog Place and Visit correction succession rules

- Date: 2026-09-03
- Context: In Stage 2.5, after merging or splitting a Place, decided which side the existing Journey and Visit keep pointing at.
- Related record: [[decisions/maplog-stage-2_5-map-detail-journey-separation.md]]

Woojin's original:

> “어 ㅇㅇ ㅇㅋ 그 규칙들 합리적이다. 대신 그 합치고 나누는 ux 가 매우 중요할것으로 생각된다. 버튼이던지, 뭐 따로 기능이 있던지, 메인지도에서 편하게 드래그해서 묶던지. 일단 알겠어. 확정하자”

Status:

- **User confirmed:** When merging, the target Place the user chose and the same-date target Visit survive, and absorbed references continue to that side.
- **User confirmed:** When splitting, the side whose photos were kept retains the existing Place. If every Visit photo is moved, the Visit moves too; if only some are moved, the remaining side retains the existing Visit.
- **User confirmed:** A new Visit is not automatically added to the existing Journey. A Journey Visit duplicated by a merge keeps the earlier order, and is reported with feedback and undo right after the correction.
- **User confirmed:** Provide persistent undo for the one previous correction step until the next attach or correction.
- Entry UX for merge and split is outside 1.0 and is not the next task. A button, a separate feature, or a drag on the main map are candidates, not a confirmed method. Scope is `record/PRODUCT.md`.

UX constraints:

- Merge and split UX must receive a core product verdict separately from the data rules.
- Do not revive a previously rejected large merge action on the main photo-viewing screen.
- Judge discoverability, prevention of a wrong merge, understanding of the result, and immediate feedback and undo on a real photo-map prototype.
