---
description: 우진 Codex CLI 실기록 홈. CodexBar는 여기를 봐야 함.
---
---
description: 우진 Codex CLI 실기록 홈. CodexBar는 여기를 봐야 함.
---
# Codex CLI 실기록 홈

상태: 사용자 확정·검증됨. 2026-09-13, 우진이 경로를 직접 알려줌.

정본: `/Users/wooojin/App/codex-plain-home`
- 세션: `sessions/YYYY/MM/DD/rollout-*.jsonl`
- 토큰: `event_msg` / `token_count` 의 `last_token_usage`
- config `model = "gpt-6-astra"`

`~/.codex`는 별도 기록. OpenCodex `~/.opencodex/usage.jsonl`의 luna/terra를 어제 사용으로 넣지 말 것. 우진 원문: "어제 luna terra 쓴적없으니까 제대로 방금 아스트라같이 로컬에 존재하는 경로만 전부 다 찾고서 전부 재갱신해"

76MB 롤아웃은 CodexBar 파일 크기 한도에 잘림. 그날 token_count만 작은 extract로 `~/.codex/sessions`에 넣는 우회가 필요했음.
