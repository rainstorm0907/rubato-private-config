---
name: psd-edit-independent-layers
description: "PSD/디자인 파일 편집은 독립 레이어 단위 비파괴로, 원본 구성·흐름 유지"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 96420cdc-2cf5-43c0-9c8f-bb36061c23a1
---

우진님 포트폴리오/디자인 PSD 작업 시, 각 요소를 독립 레이어 단위(이름변경·삭제·이동 등)로 다루고 원본 합성 결과와 구성 흐름은 그대로 보존한다. 평탄화·통짜 재작성 금지.

**Why:** 우진님이 "앞으로 그렇게 독립 레이어로 작업해, 원래 흐름대로"라고 명시. 레이어 패널이 사람 작업처럼 보여야 하고 그림이 깨지면 안 됨.
**How to apply:** psd-tools로 레이어별 비파괴 편집, 편집 후 원본 대비 composite 픽셀차이로 검증(의도한 영역만 변해야 함), 원본은 별도 폴더에 보존. Related [[hama-portfolio-pdf-pipeline]].
