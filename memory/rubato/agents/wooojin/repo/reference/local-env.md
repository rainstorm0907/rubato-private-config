---
description: 이 Mac 고유의 CLI·도구 설정과 알려진 함정.
---
이 Mac 고유의 개발 환경 사실. `~/.codex/memories`에서 옮겨왔다. 도구 업데이트로 재발할 수 있어 재확인이 필요하다.

## 홈 디렉토리 배치

- 포트폴리오 폴더 정본은 `~/포트폴리오` (한글 이름 — `portfolio`/`resume` 영문 검색에 안 걸린다). 대회·프로젝트별 하위 폴더(Cofathon-2026, openaigame-2026)에 결과 보고서를 넣는다. `~/portfolio`를 새로 만들지 않는다.
- 포트폴리오·이력서·지원서·과거 프로젝트 성과가 필요한 작업에서는 `msearch`로 이 위치를 찾은 뒤 `/Users/wooojin/포트폴리오/INDEX.md`부터 읽는다. 관련 프로젝트의 `요약.md`, 필요한 근거 파일 순서로만 좁혀 들어가고 폴더 전체를 한꺼번에 읽지 않는다. 이미지와 PDF도 요청에 직접 필요할 때만 연다.

## Claude / Codex

- Claude Code를 Google·claude.ai 로그인 전용 상태로 만들려면 `~/.claude/anthropic.env`의 `ANTHROPIC_API_KEY` 주입과 `~/.claude.json`의 `customApiKeyResponses`를 **둘 다** 제거해야 한다.
- Codex↔Claude 스킬 이식 시 도구명이 다르다. Claude의 위임은 `Agent`(Codex의 `Task`가 아님), `meight`는 Codex worker 라우팅, `consult`는 외부 고품질 검토.
- `~/.claude/skills` 직접 쓰기가 보안 경계로 차단될 수 있다. 허용된 staging(`Downloads/...`)에 먼저 쓰고 옮긴다.

## GitHub 계정

- 이 노트북의 GitHub 계정은 `rainstorm0907`이며 `keepitmello/Rubato` 권한은 READ다. `keepitmello/Rubato` 관리자 계정은 mello가 있는 다른 노트북에 있으므로, 이 노트북에서 그 계정으로 인증을 바꾸거나 `origin/rubato/base` 직접 push를 시도하지 않는다.

## Aside / 브라우저

- macOS Aside 내장 `rg`가 quarantine 때문에 반복 보안 경고를 내면, 원본을 백업하고 해당 경로를 Homebrew `rg`로 심볼릭 링크 교체하면 해결된다. Aside 업데이트 시 재발 가능. `spctl`은 `/usr/sbin/spctl` 경로를 쓴다.

## Karabiner

- Varmilo 규칙 충돌로 한영·Rectangle·`⌘⇧3`이 동시에 깨지면, 새 규칙을 얹지 말고 가장 가까운 정상 자동 백업으로 롤백한다. 설정은 `~/.config/karabiner/karabiner.json`, 백업은 `automatic_backups/`.
- 2026-09-01, `TFG24F14V`는 Mac DisplayPort·Windows HDMI 1로 연결했다. DDC 밝기 쓰기는 동작하지만 입력 선택 VCP `0x60`은 표준 HDMI 1 코드 `17`, 대체 코드 `4`, 자체 후보 `1·2·3`을 모두 무시하고 현재값 `7`을 유지했다. BetterDisplay·m1ddc 양쪽에서 재현돼 소프트웨어 DDC 입력 전환은 이 모니터에서 불가로 판정했고, 실패한 Karabiner 단축키는 제거했다. `hardwarePowerOff`로 DP를 끊으면 HDMI로 자동 전환되지 않고 모니터가 꺼지며, BetterDisplay Pro가 없어 소프트웨어 재연결도 불가했다.
- DP로 돌아올 때 어두워진 원인은 BetterDisplay가 `TFG24F14V`에 저장한 combined brightness 15%·software brightness 30%를 재적용했기 때문이다. 2026-09-01 두 값을 100%로 저장해 재연결 디밍을 제거했다. 이 모니터 자체 OSD에는 입력 소스 단축 버튼이 없으므로 한 번에 전환하려면 외장 DP 스위치/KVM이 필요하다.

## msearch — 임베딩 크레딧 소진 상태

- **지금 상태(2026-09-15~)**: OpenAI platform 잔액이 0이라 임베딩이 429로 거절된다. 벡터 색인과 벡터 검색만 죽었고 **한국어 렉시컬 검색(BM25+형태소)은 정상이라 `msearch`는 계속 쓴다.** 코드가 벡터 단계를 `try/except`로 삼키고 렉시컬 결과를 낸다.
- **소음을 껐다**: 검색할 때마다 자동 색인이 429를 토해서 `~/.rubato/memory/msearch-state/.env`에 `MSEARCH_NO_AUTOINDEX=1`을 넣었다. 왜 껐는지와 지우라는 지시를 그 위 주석에 같이 적어뒀다.
- **되돌리는 법**: platform.openai.com 결제 페이지에서 충전 → `.env`의 `MSEARCH_NO_AUTOINDEX=1` 한 줄 삭제 → 다음 검색이 밀린 파일을 알아서 색인한다(자동 따라잡기 기능). `msearch --doctor`가 전부 pass인지로 확인한다. 별도 재색인 명령은 필요 없다.
- **남는 구멍**: 2026-09-13 이후 고친 `system/working-rules.md`, `reference/agent-workflow-lessons.md`, `reference/codex-plain-home.md` 세 개는 **옛날 판 본문으로 검색된다.** 최근에 정한 규칙을 찾을 때는 `rg -n -i "찾을말" ~/.rubato/memory/agents`로 한 번 더 본다. 나머지 65개는 최신이다.
- **함정**: `failed ...: Error code: 429` 줄은 **색인 실패지 검색 실패가 아니다.** 그 아래에 결과가 정상으로 나온다. 그걸 보고 "메모리 회수 불가"로 판정하고 멈추면 안 된다(2026-09-15에 실제로 한 번 오판했다).
- **대체 경로는 없다**: ChatGPT 구독 OAuth로는 임베딩을 못 쓴다(msearch README가 명시). `GEMINI_API_KEY`도 선불 크레딧이 말라 있다. 로컬 임베딩은 `memory-index.py`의 `VECTOR_DIM = 1536`이 하드코딩이라 규격 밖이고, 하려면 차원을 설정으로 빼는 공식 PR이 먼저다.
- **비용 감각**: `text-embedding-3-small`은 100만 토큰에 $0.02, 메모리 전체(68파일 230KB)를 통째로 재색인해도 0.2센트다. 막힌 건 단가가 아니라 잔액 0이다.

## T3 앱에서 세션이 "문맥 모드" 승인창에 걸려 죽을 때

- **증상**: 앱에서 새 스레드를 astra로 시작하면 `Provider turn start failed / The operation was aborted due to timeout`이 뜨고, 이어서 `문맥 모드 승인/거절` 창이 남는다. 승인이든 거절이든 누를 때마다 `Cannot route thread '<id>' because no persisted provider binding exists`가 쌓인다. `provider_session_runtime`에 그 스레드 행이 아예 없다.
- **교착의 모양**: 세션 시작이 모델을 모르는 상태에서 모드를 요약으로 확정한다 → 뒤이어 오는 `set_model(astra)`이 "노트 모드로 바꿀까요?" 확인을 `await`한다 → 그 확인이 시작 RPC를 붙잡아 타임아웃 → 바인딩이 저장되지 않는다 → 그 확인의 답이 갈 곳이 사라진다. **빨리 눌러도 소용없다**(3초 안에 눌러도 실패). 승인창이 뜬다는 사실 자체가 이미 늦었다는 신호다.
- **수정**: `1fdc26e45`. 기록된 모드도 없고 사용자가 명시한 모드도 없으면 첫 모델의 기본값이 그냥 이기고 확인을 띄우지 않는다. 회귀 테스트는 `harness/pi-runtime/features/context-notes/new-session-astra-mode.test.mjs`.
- **하지 말 것**: `RUBATO_CONTEXT_MODE=history-notes` 환경변수로 덮는 우회. 확인창은 사라지지만 모든 세션이 노트 모드로 고정된다. 2026-09-16 우진이 그 부작용 때문에 거부했다.
- **한 번 이 상태가 된 스레드는 못 살린다.** 바인딩 행이 없어 되돌릴 손잡이가 없으므로 새 스레드를 만든다.

## 엔진을 업데이트해도 돌던 pi-server는 옛 코드를 들고 있다

- **증상**: 세션이 안 열리고 T3가 `Provider turn start failed` / `Internal server error`를 낸다. 실제로 서버가 던진 건 `이 세션은 작업 노트 방식으로 이어져 있어요...`였다.
- **함정**: `rubato remote`나 엔진 업데이트는 디스크만 바꾼다. 이미 떠 있는 `pi-server`(부모 pid 1, `--runtime-root ~/.rubato-pi/stock-engine`)는 기동 시점 모듈을 메모리에 들고 있어서 **재시작 전까지 옛 코드로 판정한다.** 고친 커밋이 들어갔는데도 증상이 그대로면 먼저 `ps -o lstart= -p <pid>`로 기동 시각과 설치 시각을 비교한다.
- **판별법**: 저장소의 회귀 테스트에서 수정을 되돌려 보고 몇 개가 실패하는지 센다. 실패가 사용자 증상과 다른 케이스 하나뿐이면, 디스크 코드는 이미 그 증상을 막고 있고 남은 원인은 실행 중인 프로세스다.
- **주의**: 그 서버가 사용자의 살아 있는 세션들을 호스팅한다. 죽이면 진행 중인 대화가 같이 끝난다. 데스크톱 앱 자체를 재시작하면 Tailscale Serve 경로까지 날아가므로(아래 항목) 서버만 다시 띄우는 편이 싸다.
- **미결**: 브랜치 `fix/context-mode-resume-refusal`(worktree `/Users/wooojin/dev/Rubato-wt/context-mode-resume`, 커밋 `6e034a2c7`)이 남은 한 케이스를 막는다 — 사람이 전역을 `summary`로 직접 지정한 상태에서 노트 세션을 재개하는 경우, 그리고 호스팅 서버가 세션별 모드를 공유 `process.env`에 쓰는 문제. 머지 여부는 우진 확인 대기.

## 토큰이 어디서 나가나 — 긴 대화의 곱셈

- **소모는 문맥 크기 × 호출 수다.** 사용자 한 번 입력에 도구 왕복이 평균 10회 붙고(2026-09-15 세션 실측: 사용자 46턴 → API 481회), 그 왕복 하나하나가 그때까지 쌓인 문맥을 통째로 다시 읽는다. 478회 호출한 세션 하나가 캐시 읽기만 1억 4천만이었고, 그중 실제로 새로 만든 건 output 25만뿐이었다.
- **모델별 실측 (호출당 평균 읽기 / 도달한 최대 문맥)**: astra 135K / 253K · sol 120K / 271K · opus 205K / **643K** · fable 236K / 551K. 캐시 비율은 어느 쪽이나 95%로 같다. **차이는 캐싱 성능이 아니라 문맥이 자라도록 방치되느냐다.** astra는 창이 27만이라 강제로 눌리고, opus는 100만이라 64만까지 자란 뒤 매 호출이 그걸 읽는다.
- **`RUBATO_CONTEXT_WINDOW_TOKENS`는 작업 노트 모드에서만 걸린다.** 요약 모드에는 임계값 설정이 아예 없다(`RUBATO_SERVER_COMPACTION_DISARMED` 외에 관련 환경변수 없음). 그래서 opus를 눌러 쓰려면 `HISTORY_NOTES_DEFAULT_MODELS`에 넣어 노트 모드로 돌리는 것이 유일한 경로이고, 절충으로 원문 전체 참조가 약해진다. 상태: 2026-09-18 우진이 이 변경 없이 "주제 바뀔 때 새 스레드"로 가기로 선택.
- **한도는 프로바이더별로 따로다.** 서브에이전트(sol/astra)는 코덱스 한도를, 리드 대화(opus/fable)는 클로드 한도를, 그록은 xai 한도를 쓴다. 누적 실측: 코덱스 계열 약 35억, 클로드 계열 약 12억, 그록 1.6억. **무거운 탐색·검증을 그록에 맡기면 리드 세션의 문맥이 안 불어나고 클로드 주간도 안 줄어든다.**

## CodexBar가 루바토 사용량을 세는 방식

- **CodexBar는 각 도구의 홈만 본다.** Codex 비용은 `~/.codex/sessions`, Claude 비용은 `~/.claude/projects`. 루바토는 자기 세션을 `~/.rubato-pi/agent/sessions`에 쓰므로 **다리가 없으면 통째로 안 세어진다.** 증상은 "그래프가 그 도구 CLI를 마지막으로 쓴 날에 멈춤".
- **다리는 `~/.codexbar/bin/codexbar-live-extract`**(launchd `com.wooojin.codexbar-live-extract`, 3분 주기)다. 루바토 세션을 tail 해서 하루·모델당 파일 하나를 각 홈에 쓴다. openai-codex 갈래는 원래 있었고, anthropic 갈래는 2026-09-18에 붙였다(`~/.claude/projects/-rubato-extract/`). 매번 같은 파일을 덮어쓰므로 중복이 쌓이지 않는다.
- **표시 토큰이 실제보다 작아 보이는 건 정상이다.** CodexBar의 `totalTokens`는 캐시 읽기를 제외하고, `cacheReadTokens`로 따로 보고한다. 둘을 더하면 원본 합계와 정확히 일치한다(2026-09-17 실측: 5,194,861 + 98,736,768 = 103,931,629). 캐시 읽기가 전체의 95%라 20배 차이로 보인다.
- **추출기는 조용히 죽는다.** 디스크가 차면 `save_state`가 `ENOSPC`로 실패하고 메뉴바는 옛 숫자를 그대로 보여준다. 숫자가 얼어 있으면 `~/Library/Logs/codexbar-live-extract.log`부터 본다.
- **Claude 한도(%)는 별개 경로다 — 어댑터 `~/.codexbar/bin/cswap-meter` 하나가 카드 두 장을 만든다(2026-09-21 정리).** 1번 `main` = `dalisalvador1231@gmail.com`, 2번 `sub` = `codesmithbuild@gmail.com`(Aside `u1` 브라우저 세션으로 claude.ai API를 읽는다 — 이 계정 자격증명은 어디에도 저장하지 않는다). **토큰의 주인은 응답 헤더 `anthropic-organization-id`로 확인한다**(oauth/profile·claude.ai 로는 못 밝힌다. setup token 은 `user:profile` 스코프가 없다).
- **dali 자격증명의 정본은 키체인 `Claude Code-credentials-dc67051c`** — 안에 setup token(`sk-ant-oat01-…`, expiresAt 2100, refreshToken 없음)이 `{"claudeAiOauth":{…}}` JSON 으로 들어 있다. 래퍼 `~/.local/bin/claude`·`~/.local/lib/codexbar-rubato/claude` 와 미터가 모두 **키체인을 먼저 읽고** `~/.codexbar/claude-meter/setup-token`(평문 사본)은 폴백으로만 쓴다. `plutil -extract claudeAiOauth.accessToken raw -o - -` 로 뽑는다. **접미사 없는 `Claude Code-credentials` 는 읽지 않는다** — Claude Code 가 토큰 갱신 때 다시 쓰면서 ACL 을 리셋해 키체인 팝업을 만드는 항목이다(아래 항목).
- **한도를 다 쓴 계정은 `/api/oauth/usage`가 429라 claude CLI 프로브가 통째로 죽는다.** 그래서 `POST /v1/messages`(max_tokens 1) 응답 헤더의 `anthropic-ratelimit-unified-5h/7d-*`로 5시간·7일 창을 읽는 폴백을 넣었다. **함정: 주간이 막힌 계정에서 Claude 는 `5h-reset` 을 `7d-reset` 과 같은 값으로 보낸다**(대표 claim 이 `seven_day`). 그대로 쓰면 세션·주간이 같은 시각에 리셋되는 것처럼 보이므로, 두 값이 같으면 세션 리셋은 비운다. 갱신이 실패하고 캐시가 오래되면(8분, 서브 5분) `usageStatus: unavailable`로 내보내서 며칠 전 숫자가 방금 읽은 값인 척 뜨지 않게 한다. 서브 읽기는 403(`account_session_invalid`)이 한 번씩 튀므로 3회 재시도한다.
- **claude-swap 어댑터의 switch 응답 계약(v1)**: `{"schemaVersion":1,"switched":bool,"from":{"number":N},"to":{"number":M},"reason":"…"}`. **`from`/`to` 는 슬롯 숫자가 아니라 `{"number":N}` 객체여야 한다** — 숫자로 보내면 앱이 메뉴에 빨간 `Account switch failed: claude-swap / switch output is malformed: missing from account` 를 띄운다(2026-09-21에 이 버그를 찾아 고쳤다). `reason` 은 성공 응답에도 필수다. 실패는 `{"schemaVersion":1,"error":{"type":…,"message":…}}` 로 보낸다. 앱은 이 어댑터를 5분마다, 그리고 메뉴를 열 때마다 호출한다.
- **키체인 함정**: 접미사 없는 `Claude Code-credentials`는 지금 토큰이 빈 문자열이고(laventador12 자리), `~/.claude-default-profile.sh`가 없는 디렉터리를 가리키면 `CLAUDE_CONFIG_DIR`이 조용히 무시돼 모든 셸이 그 빈 공유 슬롯으로 떨어진다. 프로필 dir↔키체인 접미사는 `sha256(dir)[:8]`이다. **`~/.codexbar/config.json`은 앱이 뜰 때 한 번만 읽으므로 고친 뒤에는 앱을 껐다 켠다.**
- **Codex 사용량을 세는 방식(2026-09-22 조사)**: ChatGPT 플랜의 Codex 5시간·주간 한도는 **메시지 수가 아니라 토큰을 크레딧으로 환산한 예산**이다. 공식 식은 `credits = input×요율 + cached input×요율 + output×요율`이고 요율표는 Astra **250 / 25 / 1250**(input / cached / output, 1M당), Sol 100/10/500, Terra 50/5/300 — 즉 **캐시 입력은 입력의 10%, 출력은 입력의 5배**다. 추론 토큰은 출력으로 과금되고, ChatGPT 플랜에서는 cache write가 과금되지 않는다. **Fast 모드는 같은 모델에서 한도를 더 빨리 닳게 한다(Astra Fast 2.5×)**. 혼동 금지: API TPM은 캐시도 1:1로 세지만 그건 구독 한도가 아니다. 근거: `developers.openai.com/codex/pricing`, `help.openai.com/en/articles/11481834`, `/20001106`(Codex rate card), `openai/codex` 이슈 #36488·#42357·#44685·#43731. **주의: 포함 한도의 회계가 이 요율표와 같은 단위인지는 확증 못 했다** — 요율표로 환산한 주간 크레딧이 주간 %와 맞지 않았다.
- **CodexBar의 코덱스 숫자는 "내가 쓴 양"만 센다.** 위젯의 일별 토큰은 하네스 실측(pi 세션 jsonl 전수 집계)과 0~6% 안에서 붙는다(9/22는 0.2% 차). 즉 로컬 세션 스캔이라 계정 전체(다른 기기·코덱스 데스크탑앱) 소모는 안 보인다 — 그건 OpenAI 대시보드(credits, 서비스별: Desktop App / Uncategorized / CLI / Exec)의 몫이다. 대시보드 UI는 %만 보여주고 절대 credits는 API로만 온다(CodexBar가 캐시해 둔 7월 데이터에 `dailyBreakdown`으로 존재).
- **하네스 astra 사용량 실측 감각**: 주간(9/19 08:19Z~) 126.7M 토큰(캐시 포함) · 906콜. 크레딧 가중으로는 fresh 31% / **cached 57%** / output 12% — 캐시가 10%로 할인돼도 **캐시 읽기가 여전히 제일 큰 항목**이라, 남은 절약 레버는 캐시가 아니라 "호출 수 × 문맥 크기"다.
- **laventador12는 뺐다(2026-09-21)**: cswap alias/rotation에서 제외(`cswap disable 3`), `~/.claude-default-profile.sh`는 dali 프로필로, CodexBar claude는 `cookieSource: off`(그 전엔 크롬 쿠키로 laventador12 신원이 새어 들어왔다). dali의 CLI refresh token은 죽어 있어서 cswap 슬롯으로 `claude`를 쓰려면 재로그인이 필요하다 — setup-token 쪽은 살아 있다.
- **CodexBar 자체 Claude 읽기는 이 맥에서 어느 모드로도 안 살아난다(2026-09-22 확인).** `source: cli` 는 `claude /usage` 를 실행해 stdout 의 `% left` 글자를 파싱하는데(래퍼 + 파이프에서는 print-mode 푸터만 나온다) 여기선 늘 `Claude usage probe timed out` 이다. `source: oauth` 는 키체인 항목을 읽어야 하는데 `claudeOAuthKeychainPromptMode=never`(팝업을 막으려고 정한 값)면 CodexBar 가 키체인을 아예 안 읽고, `onUserAction` 으로 풀어도 배경 컨텍스트에선 `Claude OAuth credentials not found` 다. 그래서 앱 자체 Claude 행/카드는 "새로 고치는 중 / 세션 0% 남음" 같은 **자리표시(0%, 빈 막대)** 에 머물 수 있다 — 이건 실제 데이터가 아니다. 카드는 claude-swap 어댑터가 넣는 값으로 굴러간다.
- **키체인 공유 슬롯(`Claude Code-credentials`)에는 dali 자격증명을 넣어 뒀다(2026-09-22).** 앱은 위 이유로 그걸 안 읽지만, 래퍼 없이 `claude` 를 돌리면 dali 로 붙는다. 앱이 키체인을 읽게 하려면 `claudeOAuthKeychainPromptMode` 를 `onUserAction` 이상으로 풀어야 하고, 그러면 Claude Code 가 토큰을 갱신할 때 ACL 이 리셋돼 키체인 팝업이 돌아온다(아래 함정).

## 아이폰에서 맥에 붙는 법

- **공식 경로는 T3 Code다.** 앱스토어의 T3 Code 앱(또는 Safari)으로 맥의 T3 서버에 붙는다. 데스크톱에서 쓰는 그 서버 그대로라 스레드가 폰에서도 이어진다. 근거: `scripts/remote-release/USER-TEST.md` — "아이폰 클라이언트는 T3 Code다. 맥에서 `rubato-gui`로 연 환경에 T3 Connect로 붙인다."
- **자체 PWA(`/rubato`)는 폐기됐다.** 2026-09-16 업데이트가 PWA와 허브의 HTTP/WS 계층을 지웠고, 설치기는 더 이상 `/rubato` Serve 경로를 만들지 않는다. 폰 홈 화면에 남은 옛 아이콘은 `/` 로 넘어가 T3의 `index.html`을 200으로 받으므로 **"연결은 됐는데 목록이 비어 있는"** 모습이 된다. 고장이 아니라 사라진 것이니 아이콘을 지운다.
- **페어링 발급**: `cd ~/.rubato/t3-source && T3CODE_HOME=~/.rubato/t3-home node apps/server/dist/bin.mjs pair --tailscale --ttl 2h --label <이름>`. 주소·토큰·QR이 함께 나온다. QR 이미지는 `qrencode -o <png> -s 20 -m 4 "<pairing url>"`로 만들어 맥 화면에 띄우거나 텔레그램으로 보낸다.
- **전제**: 폰은 맥의 T3 서버에 붙으므로 **데스크톱 앱이 켜져 있어야** 한다. tailnet 경로 `/` → `127.0.0.1:3773`은 데스크톱 앱이 켜질 때 스스로 깐다(`tailscaleServeEnabled`).
- **T3가 serve를 다루는 방식**: 서버 종료 시 `tailscale serve --https=443 off`를 부른다(`~/.rubato/t3-source/packages/tailscale/src/tailscale.ts`, acquire/release 쌍). 443 위 **모든** 경로를 지우므로, 같은 443에 다른 경로를 얹어 두면 앱을 끌 때마다 함께 날아간다. 지금은 얹을 경로가 없어 무해하지만, 나중에 무언가를 얹는다면 이 성질을 먼저 감안한다.

## 리서치 라우팅

- Sol이 최종 비교·판단, Consult(Aside 기반 ChatGPT)는 좁은 공개 판단, Grok+Aside 네이티브 실행기는 넓은 공개·로그인 브라우저 탐색과 정확한 클릭까지 수행한다.
- Grok provider는 `xai-grok-oauth`/`grok-4.6`. `xai/grok-4.6`은 실패한다.
- 별도 중복 스킬이나 자동 체이닝은 만들지 않기로 확정했다.
