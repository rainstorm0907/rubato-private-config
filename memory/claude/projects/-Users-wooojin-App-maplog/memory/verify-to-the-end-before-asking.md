---
name: verify-to-the-end-before-asking
description: 문서 체인과 도구는 끝까지 직접 확인한 뒤 행동한다. 한 단계에서 멈추고 우진님에게 되던지지 않는다.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fe9382e6-b6b9-4698-868d-1569f6574d41
  modified: 2026-07-27T10:36:00.378Z
---

지시 문서를 한 단계만 읽고 멈추지 말고 **체인 끝까지 따라간다.** 도구가 한 번 실패하면 대안을 직접 조사한 뒤에 보고한다. 확인 없이 "안 됩니다"로 우진님에게 넘기지 않는다.

**Why:** 2026-07-27 하루에 같은 실패가 두 번 났다. ① `AGENTS.md`만 읽고 거기서 가리키는 `code/DESIGN.md`를 안 열어서, 그 안의 trigger 표가 지정한 `code/design/import-and-album-flows.md`(사진 선택·cover flow 담당 계약)를 못 읽었다. 그 결과 2026-07-13 사용자 확정 손패 계약을 깨는 지시를 내렸고, 이미 제거됐던 결함(손패 전체 재정렬, 끝 카드 잘림)을 되살렸다. ② Codex 고정 세션 전달이 MCP 도구 하나로 실패하자 `codex --help`를 30초 확인하지 않고 우진님에게 수동 전송을 요청했다. 실제로는 `codex exec resume`이 있었다. 우진님이 "내가 일일이 매번 짚어줄 수 없다"고 했고, 이건 정당한 지적이다.

**How to apply:** 작업 패킷을 만들기 전에 `record/CURRENT.md` → 메인 계획 → `code/DESIGN.md`의 `읽는 순서` trigger 표 → 해당 세부 계약 순으로 실제로 연다. 그 계약에서 `사용자 확정`으로 표시된 항목은 Fixed이므로 지시로 덮지 않고, 바꿔야 하면 우진님에게 변경으로 올린다. 도구가 필요한데 첫 시도가 실패하면 `--help`·설정 파일·설치된 CLI를 먼저 훑고, 그래도 없을 때만 넘긴다. 관련: [[maplog-fixed-session-dispatch]]
