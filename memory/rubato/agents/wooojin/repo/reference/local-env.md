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
