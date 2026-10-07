---
description: Maplog may wait on a first load behind a loading UI. Everyday map and photo viewing is the memory gate, not the first open.
---

## Conclusion

- First load and initial setup may wait behind an honest loading UI. Do not treat that wait as the reason to reject a build.
- Memory pressure, repeated reloads, and stutter while panning the map and flipping through photos are the optimization gate. That feel is easy to kill.
- Do not optimize that path in a hurry, and do not structure later code so snapshot release, cache, and incremental loading become impossible.
- A host measurement of a large library is not a release threshold. The restart round trip itself was confirmed on a real iPhone; the viewing notes are in [[decisions/maplog-v2-restart-roundtrip-device-feedback.md]].

## Rationale

- Chose a loading UI for the first open so everyday use could stay the bar. Woojin: “첫 로딩이나 세팅은 그냥 로딩중인 애니메이션 UI로 대체하면 큰 문제는 안돼.”
- Chose everyday manipulation as the gate. Woojin: “대신 메모리 관련은 평소에 사용하는 동작에 한해선 최대한 최적화 해야돼. 왜냐면 맵 조작하며 사진 돌아가면서 보는 그 과정의 느낌을 팍 죽일 수 있는 위험이 있어.”
- Rejected as a current stop: locking the renderer, catalog, split/merge, and Recap until a separate approval of this checkpoint. The checkpoint was the order for that day, not a standing lock. Current scope is `record/PRODUCT.md`.

## Symptom

첫 로딩이나 세팅은 그냥 로딩중인 애니메이션 UI로 대체하면 큰 문제는 안돼.

대신 메모리 관련은 평소에 사용하는 동작에 한해선 최대한 최적화 해야돼. 왜냐면 맵 조작하며 사진 돌아가면서 보는 그 과정의 느낌을 팍 죽일 수 있는 위험이 있어.

재시작 왕복 작업 체크포인트로 잡고 한번 내 검증-피드백 받고서 resolver도 마무리 하면 될거같아 천천히 해도 되잖아
