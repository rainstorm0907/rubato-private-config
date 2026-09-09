---
name: automation-browser-auth-profile
description: agent-browser 영속 로그인 프로필(woojin-auth) — 자동 로그인 시도 허용 범위와 금지선
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a87a3b3d-2107-4dc7-b8cd-e29491a12b20
  modified: 2026-08-13T08:53:16.453Z
---

우진님 개인 계정 로그인이 유지되는 자동화 브라우저 프로필: **agent-browser `--session woojin-auth`** (상태 자동 영속은 `AGENT_BROWSER_SESSION_NAME=woojin-auth` 환경변수로 활성화, 쿠키·스토리지 자동 저장/복원). 2026-08-13 구축, Google(rainstorm0907@gmail.com) 우선, 이후 네이버 등 추가 예정.

**Why:** claude.ai 계정 로그인이 막혀 Gmail 커넥터·크롬 확장이 전부 불통 → [[consult-chatgpt-research]]의 전용 크롬 패턴처럼 "한 번 로그인해두고 재사용하는 자동화 전용 프로필"이 유일한 안정 경로라고 우진님이 결정.

**How to apply:**
- **실체는 진짜 Chrome + 전용 프로필**(`~/.browser-profiles/woojin-auth`, CDP 포트 9223). 실행/종료는 `~/dev/claude-ops/bin/woojin-browser` (인자 없이=시작, `stop`=종료, 데몬 아님). 조작은 `agent-browser connect 9223 --session woojin-auth` 후 평소 명령대로.
- **chrome-devtools MCP**(user 스코프 등록, `--browserUrl http://127.0.0.1:9223`)도 같은 크롬에 붙음 — 콘솔·네트워크·성능·풀 URL 감사가 로그인된 상태 그대로 가능.
- 2026-08-13 로그인 세팅: Google(완료). 네이버·카카오(티스토리)·원티드·인스타·X·GitHub·Supabase는 로그인 탭 띄워둠(우진님 입력 대기). KB 등 금융 사이트는 이 프로필에 로그인하지 않음(금융 금지선).
- **로그인이 풀려 있으면**: 계정 선택 화면에서 프로필(rainstorm0907 등) 클릭, "계속", 자동 로그인 시도까지는 **Claude가 직접 해도 됨** (우진님이 2026-08-13 명시 승인).
- **금지선 (변경 없음)**: 비밀번호·2FA 코드 입력은 절대 대신하지 않음 — 그 화면이 나오면 창을 앞에 두고 우진님께 입력 요청.
- [[browser-automation-policy]]와 함께 적용: 우진님 본 크롬은 computer-use 읽기 전용, 조작은 이 프로필로.
