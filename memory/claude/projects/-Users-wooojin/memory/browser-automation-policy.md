---
name: browser-automation-policy
description: "브라우저/GUI 자동화 도구 사용 방침 — 기본 Chrome 확장, 폴백 Computer Use, 작업 방해 금지"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8e432a29-07cb-4e31-9b36-76148c1789b5
---

우진님 지시 (2026-06-12): 브라우저 자동화는 **Claude in Chrome 확장을 기본**으로 쓰고, 크롬으로 안 되는 GUI 작업(시뮬레이터 탭 등)만 **Computer Use를 폴백**으로 쓴다.

**Why:** 크롬 확장이 DOM 기반이라 토큰/시간 효율이 압도적이고(스크린샷 루프 불필요), 로그인된 세션(NAVER Cloud 콘솔 등)을 그대로 쓸 수 있어서. Computer Use는 화면 점유 비용이 커서 꼭 필요할 때만.

**How to apply:**
- 웹 작업 → `/chrome` 연결 상태 확인 후 Chrome 확장 사용.
- Computer Use는 브라우저 밖 GUI 조작이 필요할 때만. **사용 전 반드시 사전 고지** — 우진님 작업을 방해하지 말 것("창 위로 띄우지 말것"). macOS Computer Use는 실행 중 화면/마우스를 점유하므로 완전 백그라운드는 불가 — 시작 전에 알리고, 짧게 끝내고, Esc로 즉시 중단 가능함을 안내.
- 연결 환경: Claude Code 2.1.173 확인(요구 버전 충족), computer-use는 built-in MCP(`/mcp`에서 enable), macOS 권한(Accessibility+Screen Recording) 필요.

관련: [[hama-deploy-topology]] (Maplog/Hama 작업에서 NAVER 콘솔·Vercel 등 로그인 웹 작업이 잦음)
