thread_id: 01a01eac-0c17-76a0-80b8-cba135b66726
updated_at: 2026-08-20T12:32:54+00:00
rollout_path: /Users/wooojin/.codex/sessions/2026/08/20/rollout-2026-08-20T19-16-26-01a01eac-0c17-76a0-80b8-cba135b66726.jsonl
cwd: /Users/wooojin
git_branch: main

# 경량 리서치 라우팅과 Grok+Aside 실행기 구축

Rollout context: `/Users/wooojin/dev/maple` 및 `/Users/wooojin` 환경에서 일반 작업 세션의 리서치 역할을 재설계했다. 사용자는 Sol이 전체 작업과 최종 비교를 맡고, Consult는 집중 공개 분석, Grok High는 넓은 탐색과 로그인 브라우저 조작, Aside는 브라우저 백엔드가 되길 원했다. 새 창은 최소화하고 작업 종료 시 탭과 프로세스를 정리해야 한다.

## Task 1: Consult를 Aside 기반 ChatGPT 실행기로 교체

Outcome: success

Preference signals:
- 사용자가 “그냥 Sol이 작업 및 비교, 에이전트로 Grok이 경매장 Aside 브라우저에서 탐색”하는 구조를 명확히 요구했다 -> Sol이 브라우저를 직접 따라다니지 않고 외부 에이전트 결과만 받아 최종 판단하도록 한다.
- 공개 웹에는 Consult도 포함해야 하며, “정확한 클릭같은 것도 알아서 에이전트가 끝내게” 하고 Sol 토큰과 작업 흐름을 아껴야 한다고 했다 -> Consult는 좁은 판단, Grok은 넓은 탐색·브라우저 조작으로 분리한다.
- 사용자는 “최대한 경량화”를 반복 요청했다 -> 별도 중복 스킬·공용 라이브러리·자동 체이닝을 만들지 않고 실행기와 라우터만 둔다.

Reusable knowledge:
- `/Users/wooojin/.codex/skills/consult/scripts/run_aside_consult.py`가 Aside의 로그인된 ChatGPT Pro 탭에서 `GPT-5.6 Sol + 매우 높음`(quick) 또는 `GPT-5.6 Sol + Pro`(deep)를 직접 확인하고, 패킷 업로드·응답 저장·대화 URL 회수·작업 탭 종료를 수행한다.
- 실제 quick과 deep 호출 모두 모델 선택, 응답, 정확한 `/c/...` URL, 탭 기준선 복원을 통과했다. 기존 사용자 탭은 보존됐다.
- Consult의 모델 선택이 검증되지 않으면 전송하지 않고 fail-closed한다. `contenteditable` 입력창에는 `fill()` 대신 클릭 후 `keyboard.insertText()`를 사용해야 한다.
- Aside ChatGPT 계정은 `ChatGPT Pro` 개인 계정이어야 하며 Work/Free/미로그인 상태는 중단한다.

Failures and how to do differently:
- 초기 `agbrowse` 경로는 모델 선택기를 찾지 못하고 잘못된 모델로 전송할 위험이 있어 폐기했다. Consult는 Aside 기반으로 교체해야 한다.
- Aside 실행기 초기에는 ChatGPT UI 렌더 지연과 detached ref, contenteditable 입력 문제를 겪었다. fresh snapshot, detached 시 1회 재탐색, 입력 후 내용 검증으로 해결했다.

References:
- `/Users/wooojin/.codex/skills/consult/SKILL.md`
- `/Users/wooojin/.codex/skills/consult/scripts/run_aside_consult.py`
- Quick evidence: `.consult/routing-pilot/aside-quick-final-response.json`
- Deep evidence: `.consult/routing-pilot/aside-deep-response.json`

## Task 2: 자동 리서치 라우터와 Grok 실행기 구축

Outcome: success

Preference signals:
- 사용자는 “다른 작업 세션에서 리서치 하라고 하면 자동 판단 및 발동”을 원했다 -> `research-browser-router`는 implicit invocation을 유지하고, 로컬 자료로 충분하면 외부 호출을 생략한다.
- 사용자는 별도 `grok-aside-research` 스킬은 불필요하고 “그록 실행기까지만” 원했다 -> 단일 라우터 + Consult 실행기 + Grok 실행기 구조를 유지하고 별도 Grok 스킬은 만들지 않는다.
- 사용자는 Grok이 로그인 경매장에서도 탐색하고 필터·클릭·다운로드까지 끝내길 원했다 -> Grok은 Aside 브라우저의 reversible 작업을 직접 완료하고 Sol에는 compact report만 반환한다.

Reusable knowledge:
- 정확한 Aside xAI 설정은 `provider=xai-grok-oauth`, `model=grok-4.6`, `effort=high`다. 일반 `xai` provider는 “not available”이지만 `xai-grok-oauth`는 실제 실행에 성공했다.
- `/Users/wooojin/.codex/skills/research-browser-router/scripts/run_grok_research.py`는 Aside native Grok agent를 호출한다. 기본 모드는 quick이며 공개 웹과 로그인 브라우저를 모두 다룬다.
- 실행기는 최대 페이지 수·브라우저 액션 수·wall-clock timeout을 강제하고, `grok-brief.md`, `grok-report.md`, `grok-run.json`, stdout/stderr를 저장한다. Grok 보고서는 `직접 관찰`, `공식 확인`, `해석`, `미확인`, `브라우저 작업`, `상태 변경`, `승인 필요` 섹션을 사용한다.
- 읽기·검색·필터·상세 열기·정확한 클릭·다운로드는 Grok이 수행한다. 구매·제출·메시지·삭제·계정/보안 변경 등 consequential mutation만 사용자 승인을 기다린다.
- Grok 성공 시 Sol은 `grok-report.md`와 `grok-run.json`의 compact 상태만 읽고 raw 로그는 실패나 모순 때만 읽는다.
- `grok mcp add aside ...`로 추가했던 중복 MCP 등록은 제거했다. 현재 Grok 실행은 Aside native provider를 사용한다.

Verification:
- Wikipedia 시험에서 Grok이 기존 Maple Auction 및 메이플 가이드 탭을 건드리지 않고 새 탭을 열어 English 링크를 클릭하고 `en.wikipedia.org`와 제목을 확인한 뒤 탭을 닫았다.
- 최종 `grok-run.json`: `status=complete`, `model=grok-4.6`, `provider=xai-grok-oauth`, `effort=high`, `orphanCheck=gone`, 기존 탭 변화 없음.
- 이전 Grok CLI+Aside MCP 경로도 동작했지만 native Aside 경로가 더 가볍고 중복 구성이 없어 최종 채택됐다.

Failures and how to do differently:
- 첫 Grok 실행기는 WebSearch/WebFetch만 허용해 로그인 경매장을 못 다뤘다. 원인은 Grok의 능력 부족이 아니라 브라우저 권한을 주지 않은 라우터 계약이었다. 로그인 웹의 넓은 탐색은 Grok+Aside agent로 보내야 한다.
- `xai/grok-4.6`은 Aside provider ID가 아니었다. 반드시 `xai-grok-oauth/grok-4.6` 조합을 사용한다.
- 20초 timeout 시험은 usable report 없이 code 1로 종료됐지만 process group과 브라우저 baseline은 정리됐다. 부분 결과가 있으면 code 3으로 저장한다.

References:
- `/Users/wooojin/.codex/skills/research-browser-router/SKILL.md`
- `/Users/wooojin/.codex/skills/research-browser-router/scripts/run_grok_research.py`
- Successful pilot: `/Users/wooojin/dev/maple/.research/aside-native-grok-click/grok-run.json`
- Successful report: `/Users/wooojin/dev/maple/.research/aside-native-grok-click/grok-report.md`

## Task 3: 기존 메이플 세션에 새 라우팅 적용

Outcome: partial

Key steps:
- 다른 메이플 세션에 새 실행기를 사용하라는 follow-up을 보냈다.
- 해당 세션은 이미 눈장 후보 찜과 API 갱신을 수행했으므로 반복하지 말고 남은 심볼 비용 리서치부터 새 실행기를 사용하도록 지시했다.
- 기존 세션에서 이전 Grok 실행기가 실패한 뒤 web search와 computer-use fallback으로 진행한 흔적이 있어, 새 규칙 적용 전후가 혼재한다.

Failures and how to do differently:
- 진행 중 세션에 라우터 업데이트가 자동으로 소급되지는 않는다. 이미 시작된 세션에는 명시적 follow-up을 보내야 한다.
- 앞으로는 “최신 리서치/로그인 매물/정확한 클릭” 요청 시 라우터와 실행기를 먼저 읽고, Grok native Aside runner를 호출해야 한다.

References:
- Thread: `01a01ef5-339b-7c70-b5fc-e8c0b8908944`
- Maple task cwd: `/Users/wooojin/dev/maple`
- Existing Maple Auction tab was preserved throughout validation.
