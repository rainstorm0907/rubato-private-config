---
name: subagents-go-idle-without-delivering
description: 이 환경에서 Agent 툴 서브에이전트가 결과물 없이 유휴 상태로 끝나는 일이 반복된다 — 감사·리뷰 성격 작업에서 특히
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ad855fc0-a3d2-4969-95fa-f3a22e6a79b2
  modified: 2026-08-21T13:02:05.685Z
---

Agent 툴로 띄운 서브에이전트가 작업을 마쳤다는 신호(idle_notification)만 보내고
정작 보고서를 돌려주지 않는 일이 반복 관측됐다. 2026-08-21 하루에만 네 번
(consult-browser, sol-review, coldstart 2회). SendMessage로 다시 요청하면
한 번은 회수됐고, 나머지는 끝내 아무것도 내놓지 않았다.

**Why:** 이 실패는 조용하다 — 에러가 아니라 "완료"처럼 보인다. 결과를 기다리며
턴을 소비하다가, 결국 직접 해야 할 일을 늦게 시작하게 된다. 감사·검증처럼
"결과가 안 오면 판단을 못 하는" 작업일수록 손해가 크다.

**How to apply:** 서브에이전트에 위임할 때 (1) 보고서를 파일이 아니라 응답 본문으로
달라고 명시하고, (2) 유휴 알림이 왔는데 결과물이 없으면 SendMessage로 한 번만
회수 시도하고, (3) 두 번째로 빈손이면 그 레일을 접고 직접 확인한다. 특히 확인 항목이
명령 몇 개로 끝나는 감사라면 애초에 위임하지 말고 인라인으로 하는 편이 빠르다.
[[tech-lead-charter]]의 "두 번 실패하면 접근 자체가 문제"가 여기 그대로 적용된다.
