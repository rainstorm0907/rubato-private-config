---
description: 우진이 백그라운드·다른 세션이 네트워크 오류 때문에 멈추지 않고 안전하게 이어지길 원하는 지속 선호.
---
## 네트워크 오류 뒤 세션 지속성

- 상태: 사용자 확정 선호, Rubato 레포에서 구현·검증됨(2026-09-01), PR 생성 대기.
- 구현: text/thinking/일반 agent toolCall 뒤 transport 오류는 Senpi의 기존 제한 재시도로 넘기고, Cursor exec-channel처럼 provider가 이미 tool을 실행한 경우에만 `senpi:no-turn-retry:`를 유지한다. 단위 501개·통합 11개·전체 typecheck가 통과했고 일반 Rubato Opus 독립 리뷰에서 P0~P2가 없었다.
- 2026-09-01, Rubato의 `senpi:no-turn-retry:WebSocket error`가 다른 세션을 멈추는 문제를 보고 우진: "이건 자꾸 왜 써서 다른 세션 멈추는거야?"
- 해석: 내부 안전 표식이 그대로 세션을 터미널 오류로 끝내는 동작을 원하지 않는다. 부분 출력 뒤 네트워크가 끊겨도 중복 도구 실행은 막으면서, 안전한 세션은 부모 개입 없이 이어지거나 복구돼야 한다.
