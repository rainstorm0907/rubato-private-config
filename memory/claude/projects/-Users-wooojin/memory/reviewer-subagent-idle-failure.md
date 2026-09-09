---
name: reviewer-subagent-idle-failure
description: reviewer 서브에이전트가 스폰만 되고 프롬프트를 실행하지 않은 채 대기로 뜨는 실패 패턴과 대체 경로
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 15d5751b-e7b4-4cf8-97c4-f356e45507e6
  modified: 2026-08-20T13:13:43.588Z
---

2026-08-20 세션에서 `reviewer` 서브에이전트가 4회 연속 같은 방식으로 실패했다. Agent 툴로 스폰하면 "Spawned successfully"는 뜨는데 프롬프트를 실행하지 않고 곧바로 `idle_notification`(idleReason: available)만 보내온다. SendMessage로 과제를 다시 넘겨도 결과 보고 없이 또 대기로 돌아간다. ListAgents에는 아예 안 잡힌다.

**Why:** 리뷰어 응답을 기다리며 턴을 계속 넘기면 사용자 시간만 버린다. 우진님은 위임 작업 상태를 선제적으로 알리길 원하고([[delegated-work-status-reporting]]), 검증 강도는 stakes에 비례해야 한다([[proportional-rigor]]).

**How to apply:** 같은 증상이 2회 반복되면 그 경로를 접는다. 대체 순서는 (1) 내가 직접 실행 가능한 것은 런타임 증거로 확인([[verify-before-done]]), (2) 외부 사실은 WebFetch로 1차 문서 직접 확인, (3) 그래도 필요하면 meight(코덱스) 또는 Skill(consult)로 다른 레일 사용. 실제로 이 세션에서는 Microsoft 문서 직독이 리뷰어보다 나은 결과를 냈다 — SendInput이 UIPI에 막힐 때 성공을 반환한다는 핵심 함정을 거기서 찾았다.
