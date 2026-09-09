---
name: agent-browser-headed-when-user-facing
description: 사용자가 조작할 페이지는 본인 크롬에 open으로 띄우기 — 자동화 브라우저는 내가 조작할 때만
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a87a3b3d-2107-4dc7-b8cd-e29491a12b20
  modified: 2026-08-13T15:23:07.586Z
---

브라우저를 띄우는 목적으로 도구를 고른다 (2026-08-14 우진님 교정 "내가 조작하는 건데 자동화를 붙일 필요가 없잖아"):

- **우진님이 직접 조작할 페이지** (가입, 로그인, 결제, 본인 확인): `open -a "Google Chrome" <URL>` — 본인 평소 크롬에 새 탭. 자동화 지문이 없어 구글 OAuth·AWS 가입 차단(ERR-837)에 안 걸린다.
- **내가 조작하는 작업** (스크래이핑, 폼 자동화): agent-browser headless(기본값).
- **내 조작을 우진님이 지켜봐야 할 때만**: `--headed` (세션 재시작 필요 — headed/headless는 세션 단위).

**Why:** 2026-08-13~14 두 번 연속 실수 — ① headless 탭을 "띄워놨어"라고 안내(안 보임) ② headed 자동화 크롬에서 가입시키다 구글 "로그인할 수 없음"·AWS ERR-837 연쇄 차단. 자동화 브라우저는 CDP 지문 때문에 로그인·가입류가 원천 차단됨.

**How to apply — CDP 크롬 (로그인+자동화 둘 다 필요할 때의 정답, 8/14 실증):**
```
open -na "Google Chrome" --args --user-data-dir="$HOME/.config/agent-real-chrome" --remote-debugging-port=9222 --no-first-run <URL>
agent-browser --cdp 9222 --session realchrome <cmd>
```
평범하게 띄운 진짜 크롬(webdriver=false, 정상 UA)에 CDP로 붙는 방식 — 구글 OAuth·패스키 로그인 통과 확인됨. 함정: `--session` 이름 없이 `--cdp`만 주면 데몬이 기존 headless 세션을 재사용해 무시됨 — 반드시 전용 세션명. 창이 화면에 보이므로 로그인은 사용자가 그 창에서 직접, 이후 조작은 내가. 프로필 영속이라 세션 유지. 대안: claude-in-chrome 확장(본인 평소 크롬). [[automation-browser-auth-profile]] [[browser-automation-policy]] [[aws-badge-credly]]
