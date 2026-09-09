---
description: Maplog Stage 2.5에서 메인 지도·사진 상세의 Place-first/day-second 구조는 확정하고, Stage 3 Journey 연출 단위는 분리해 열어 둔 결정.
---
# Maplog 지도·사진 상세와 Journey 연출 분리

- 날짜: 2026-09-03
- 맥락: Stage 2.5의 Place·Visit 저장 단위와 Stage 3에서 Journey를 보여주는 단위를 한 결정으로 볼지 정리했다.
- 관련 기록: [[decisions/maplog-v2-place-first-map-day-second-journey.md]]

우진 원문:

> “같은 장소가 먼저고, 같은 날이 그다음 이 맞긴한거같아. 그리고 journey를 어디에서 보냐에 따라 다른거같아. 메인 지도화면이라면 최신버전이 확실해. 그렇게 나눈다음, 사진 상세 누르면 같은 장소 내부에 같은 날끼리 묶인 사진들이 나눠져서 보이는거지.”

상태:

- **사용자 확정:** 메인 지도는 Place가 1순위다.
- **사용자 확정:** Place의 사진 상세에서는 같은 장소 안 사진을 capture-local day별 Visit로 나눠 보여준다.
- **사용자 확인 대기:** Stage 3 Journey/Recap에서 여러 Place의 같은 날 Visit를 하루 장면으로 묶을지, 장소별 장면으로 나눌지.

설계 해석:

- Stage 2.5는 `Place + capture-local day`인 Visit를 가장 작은 안정적인 의미 묶음으로 만든다.
- Stage 3은 ordered Visit 입력을 받아 하루 chapter나 장소별 장면으로 연출할 수 있다.
- 저장 단위와 화면 연출 단위를 같은 법률로 조기에 고정하지 않는다.
