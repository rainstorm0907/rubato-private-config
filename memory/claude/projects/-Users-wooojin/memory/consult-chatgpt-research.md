---
name: consult-chatgpt-research
description: "consult 스킬(ChatGPT Pro 웹 외부 리서치) 클로드+코덱스 양쪽 설치, 전용 크롬은 숨김·백그라운드로만 동작"
metadata: 
  node_type: memory
  type: project
  originSessionId: b0cab1aa-eaaa-4d77-bd38-5b5be5d15829
  modified: 2026-08-13T17:17:25.927Z
---

2026-07-04 설치: `consult` 스킬 = ChatGPT Pro 웹 UI를 agbrowse(CDP)로 조종해 외부 리서치/2차 의견을 받아오는 도구. 원본 zip `~/Downloads/consult-skill-self-contained-20260704.zip`, 영구 번들 `~/dev/tools/consult-self-contained`.

**설치 위치:** `~/.claude/skills/consult` + `~/.codex/skills/consult`(동일 사본) + `~/.local/bin/agbrowse`(번들 래퍼 심링크) + `~/.codex/consult.env`(우진 ChatGPT 프로젝트 URL). 전용 크롬 프로필 `~/.codex/browser-profiles/consult-agbrowse`, CDP 9223 — **본 크롬 창/탭과 완전 분리**.

**브라우저 계정 (2026-07-05, 우진님 지시 — 절대 변경 금지):** ChatGPT = 우진 프로젝트 계정 / **Gemini = rainstorm0907@gmail.com (서로 다른 구글 계정, 이대로 유지)**. 로그아웃·계정 전환 금지.

**창 방해 금지 (2026-07-05):** macOS는 숨긴 크롬이라도 탭 활성화(`Target.activateTarget` — agbrowse new-tab/select-tab/text 경유)를 하면 앱을 도로 꺼내 작업 창 위로 올림. 자동화는 **`quiet-browse`**(`~/.local/bin/quiet-browse`, 번들 bin/quiet-browse.mjs, 탭 활성화 없는 CDP open/text/close/list + 작업 전 숨김 상태 기억·자동 재숨김) 사용. 래퍼에 `agbrowse hide`/`show` 명령 추가 — 로그인 개입 후 반드시 hide. 감시 루프에 select-tab 넣지 말 것(60초마다 창 올라와 우진님 불만, 2026-07-05).

**quiet-browse 순수 CDP 재작성 (2026-07-05):** playwright `connectOverCDP`가 크롬 상태 타서 `setDownloadBehavior`로 깨짐 → **Node 내장 WebSocket만 쓰는 순수 CDP로 재작성**(playwright/npm 의존성 0). Target.getTargets/createTarget(background:true)/attachToTarget(flatten)+Runtime.evaluate(innerText)/closeTarget. 코덱스 앱 node v24.14.0 포함 모든 node 24+/25가 WebSocket 내장이라 코덱스 셸에서도 그대로 동작. 크롬 메인 PID 탐지는 `ps ax`에서 `MacOS/Google Chrome ` + `remote-debugging-port` + `--type=` 없는 줄(자식 프로세스 제외 — pgrep은 헬퍼 잡아서 osascript 실패). **아카/디시는 curl/web-fetch로 열면 HTTP 200이어도 JS 렌더 껍데기만 옴 → 반드시 quiet-browse(실제 렌더 innerText)로 읽어야 함.** 코덱스가 커뮤니티 못 긁는 근본 원인이 이것.

**우진님 지시 (2026-07-04): ① consult 작업은 항상 이 동일 프로필을 유지해서 쓸 것. ② 항상 로그인 계정의 '우진' 프로젝트 안에서만 돌 것** — 래퍼가 chatgpt send/query에 `--url` 미지정 시 consult.env의 프로젝트 URL(`g-p-…-ujin/project`)을 자동 주입함(다른 vendor 지정 시 제외). 검증: 대화가 프로젝트 URL 하위(`…-ujin/c/…`)에 생성되는 것 확인(2026-07-04, PROJECT-OK 스모크). 로그인 완료 상태. 다른 BROWSER_AGENT_HOME으로 실행하거나 프로필 디렉토리를 지우고 새로 만들면 ChatGPT 로그인 쿠키가 날아가 재로그인이 필요해짐. 래퍼 기본값이 이 프로필이므로 환경변수를 덮어쓰지만 않으면 됨.

**백그라운드 구성 (우진님 요구: 작업 창 방해 금지):**
- vendor `browser.mjs` 패치: `AGBROWSE_NO_FOREGROUND=1`이면 `foregroundCdpWindow`/`focusChromeApp` 스킵. 원본은 `open -a`로 **본 크롬까지 전면으로 끌어올리는** 문제가 있었음.
- 래퍼 `bin/agbrowse`의 `quiet_start`: 콜드 스타트 시 전면 앱 기억 → `start` → 그 크롬 pid만 System Events로 숨김(`visible=false`) → `open -a`로 원래 앱 복귀. web-ai(render 제외)·start에서 자동 발동. 검증 완료(cmux 포커스 유지).
- 기본 크롬 플래그: `--disable-backgrounding-occluded-windows --disable-renderer-backgrounding --window-position=900,620` (숨김 상태 렌더 스로틀 방지).
- 창 다시 보이게(로그인/수동 개입): `AGBROWSE_NO_FOREGROUND=0 agbrowse start`.

**Chrome 151 프로필 가드 패치 (2026-08-12):** Chrome 151이 `--no-startup-window` 기동 시 Local State의 `last_active_profiles`를 `[]`로 되돌려서 래퍼의 기본 프로필 가드("consult Chrome is already running with a different default profile")가 항상 fail-closed하게 됨 → `~/dev/tools/consult-self-contained/bin/agbrowse`의 가드를 `last_active_profiles in ([directory], [])`로 완화(백업: `agbrowse.bak-20260812`). 크롬 업데이트·번들 vendor 교체 시 이 패치도 재적용 필요. 크롬을 죽여도 헬퍼가 다시 띄우므로 "이미 실행 중" 에러는 프로세스 문제가 아님.

**주의:** `npm install -g agbrowse@latest`로 업데이트하면 패치 유실 + PATH 충돌 가능 — 업데이트는 번들 vendor 교체 후 재패치가 원칙. 스킬 재설치는 `~/dev/tools/consult-self-contained/install.sh --all-skills --force`(기존 백업됨). 긴 리서치는 SKILL.md의 send/poll 패턴 + 백그라운드 Bash로 돌리면 세션이 안 막힘.

**브라우저 위생 수리 (2026-08-14, meight 워커):** ① 코덱스 설치본에 `ensure_consult_chrome.py` 신설 — `--no-startup-window`로 사전 기동해 about:blank 창이 화면에 안 뜸. ② 각 consult 실행이 자기가 연 탭만 닫음(before/after CDP diff 검증, 기존 탭 보존). ③ 모델 선택기 고장의 근본 원인 = 스크립트가 물고 있던 self-contained 번들 0.1.16의 셀렉터 낡음 → 전역 agbrowse 0.1.23 사용으로 전환(전역 패키지는 무패치). 수정 파일: 두 설치본의 `run_agbrowse_consult.py` + 코덱스 `ensure_consult_chrome.py`. **미해결:** 클로드 설치본은 CDP 9222를 기대하는데 9222는 agent-real-chrome이 점유 — 클로드 쪽 consult는 런타임 미검증(정적 확인만). 워커 브리프에 TCC 팝업 유발 수단(스크린샷·osascript 등) 금지를 명시할 것 — 8/14 팝업 폭탄 사고.

**산출물 원문 보존 (2026-08-06, 우진님 확정 지시):** "consult 했던것들은 파일로 나오는거 원문 그대로 올려줘. 가공하지 말고. 우리꺼에 더하지도 말고 앞으로도 그렇게" — consult/외부 조사 결과는 원문 파일 그대로 보존·전달하고, 내부 판단·팀 결론과 섞어 재작성하지 말 것. 외부 의견을 팀 확정 결정처럼 표현하는 것도 금지.

관련: [[codex-claude-global-sync]] (스킬 양쪽 동기화 구조)
