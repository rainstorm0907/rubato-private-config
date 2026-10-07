# Task Group: Rubato engine update recovery and desktop runtime failure diagnosis
scope: `/Users/wooojin/dev/Rubato` 업데이트·재빌드 뒤 Rubato가 시작하지 않거나, 메시지는 들어가지만 세션 응답이 멈출 때 패키지 closure·개인 오버레이 보존·GUI/엔진/socket 상태를 분리해 진단하고 복구·종료 검증하는 기준이다.
applies_to: cwd=/Users/wooojin/dev/Rubato (runtime diagnosis also recorded from /Users/wooojin); reuse_rule=현재 macOS Rubato 설치와 `~/.rubato-pi` 런타임에는 직접 재사용한다. 프로세스 PID, `maxfiles`, 설치 엔진 상태, GUI/bridge 상태는 시점 의존적이므로 실제 로그·process/socket을 다시 확인하고, 개인 설정·세션·확장은 변경 금지 경계로 둔다.

## Task 1: Repair missing packaged `request-images.mjs` while preserving the personal overlay, success

### rollout_summary_files

- rollout_summaries/2026-09-24T13-54-22-bq7A-rubato_engine_missing_request_images_fix.md (cwd=/Users/wooojin/App/maplog, rollout_path=/Users/wooojin/.codex/sessions/2026/09/24/rollout-2026-09-24T22-54-22-01a0d3b2-2599-7122-8d6c-c4c0b2124586.jsonl, updated_at=2026-09-24T14:00:42+00:00, thread_id=01a0d3b2-2599-7122-8d6c-c4c0b2124586, repair executed in /Users/wooojin/dev/Rubato; package closure, preservation, and GUI verified)

### keywords

- Rubato, request-images.mjs, ERR_MODULE_NOT_FOUND, context-notes, contextNoteSources, patches.mjs, build-active-engine, stock-engine, personal_manifest=identical, rubato restart, t3-bridge, catalogue ok 22, codesign

## Task 2: Diagnose post-update frozen session and completely shut down duplicate GUI/engine processes, success

### rollout_summary_files

- rollout_summaries/2026-09-21T17-50-57-Kmrn-rubato_update_session_freeze_duplicate_gui_socket_emfile.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/09/22/rollout-2026-09-22T02-50-57-01a0c517-a93a-7712-9358-9473c8960fb9.jsonl, updated_at=2026-09-21T17:56:21+00:00, thread_id=01a0c517-a93a-7712-9358-9473c8960fb9, duplicate GUI, socket disconnect, and orphan engine shutdown verified)

### keywords

- Rubato, pi-server, Electron, duplicate-GUI, pi.sock, connection.json, EMFILE: too many open files, watch, pending byte limit, start-electron, Lock file is already being held, pgrep -lf, macOS

## User preferences

- when updating Rubato, the user asked “최신 업뎃대로 맞추면서 개인 오버레이는 냅두고” -> treat personal settings, extensions, overlays, and sessions as off-limits; prove preservation with pre/post manifests and the actual GUI, not a successful rebuild alone. [Task 1]
- when the cause was explained, the user asked “둘다 종료해줘” -> after explicit approval, terminate the GUI, launcher, and any orphan engine, then prove no related process/window remains. [Task 2]
- a restart is not sufficient evidence for this user: confirm the real Rubato window still shows the existing project, sessions, and model list. [Task 1]

## Reusable knowledge

- `ERR_MODULE_NOT_FOUND` from `context-notes/controller.mjs` for `request-images.mjs` can mean source and GUI bundle are current while installed `~/.rubato-pi/stock-engine` is incomplete. Inspect `harness/pi-runtime/features/context-notes/patches.mjs` package lists and test a core installed import; this incident needed only `"request-images.mjs"` added to `contextNoteSources`. [Task 1]
- After the focused context-notes tests, run `node harness/scripts/build-active-engine.mjs --force`; verify the installed file and `controller.mjs` import, then use `rubato restart`, bridge `connected`/`catalogue ok 22`, `codesign --verify --deep --strict /Applications/Rubato.app`, and the accessibility UI as separate checks. `rubato restart` can leave the GUI closed, so explicitly open it if needed. [Task 1]
- Preserve `~/.zshrc`, `~/.rubato/agent`, `~/.rubato-pi/agent`, `~/.rubato/t3-home/userdata/settings.json`, and relevant extensions before rebuilding. CLI and GUI/Pi profiles are separate; `harness/scripts/install-extensions.sh` preserves existing extensions unless `--force` is used. The verified 19-file result was `personal_manifest=identical`. [Task 1]
- For a post-update freeze, first inspect duplicate Electron instances, `/Users/wooojin/.rubato-pi/agent/server/pi.sock` versus `.tty`, `connection.json`, `pi-server.log`, `t3-bridge.log`, and `rubato-gui-install.log`. Here two GUIs shared the profile while no GUI was attached to `pi.sock`; logs also showed `Unix connection exceeded its pending byte limit`, `EMFILE: too many open files, watch`, build `Terminated: 15`, and a `maxfiles` soft limit of 256. Session JSONL remains under `/Users/wooojin/.rubato-pi/agent/sessions`. [Task 2]

## Failures and how to do differently

- Symptom: source fingerprint/current GUI bundle looks valid but the CLI fails before help with a missing module. Cause: the installed feature package omitted a source file. Fix: check feature/package closure and a real installed import rather than trusting repository freshness; keep the minimal package-list fix and note that the resulting dirty worktree can block a later `rubato update` until committed or otherwise preserved. [Task 1]
- Symptom: `rubato restart` returns success but no GUI is visible. Cause: engine restart and desktop window state are independent. Fix: verify process, bridge connection/catalogue, and actual accessibility UI; reopen `/Applications/Rubato.app` when necessary. [Task 1]
- Symptom: `osascript` quit returns success but Rubato processes survive. Cause: it did not remove both GUI instances or the orphaned `pi-server`. Fix: use a simple process check after shutdown, including `pgrep -lf 'start-electron|Rubato.app/Contents/MacOS/Electron|apps/server/dist/bin.mjs|pi-server/src/cli.mjs|pi-rpc'`; terminate remaining owned PIDs and require `no matching processes`. [Task 2]
- Symptom: update-time session freeze accompanies `EMFILE`/pending-byte-limit and a disconnected `pi.sock`. Cause: duplicate GUI and failed build left a malformed runtime state; avoid opening multiple windows during recovery, clear existing processes first, then start one GUI and verify a new session response. [Task 2]

# Task Group: Rubato desktop GUI installation and T3 stale-queue recovery PR
scope: `/Users/wooojin/dev/Rubato`에서 기존 CLI 개인 설정을 보존하며 T3 GUI를 설치·실제 UI로 검증하고, stranded queued message를 복구하는 PR의 검증/머지 판단을 할 때 쓴다. 설치 성공·권한상 mergeable·머지 권장은 서로 다른 판정이다.
applies_to: cwd=/Users/wooojin/dev/Rubato (secondary=/Users/wooojin/dev/Rubato-pr-t3-queue); reuse_rule=현재 T3 integration 경로와 PR #12 사례에만 직접 재사용한다. source pin, GUI model default, CI 상태, session state는 후속 작업에서 다시 확인하며, 실행 중 세션을 끊을 변경은 사용자 승인 없이 하지 않는다.

## Task 1: Install and verify current T3-based Rubato desktop GUI without changing CLI settings, success

### rollout_summary_files

- rollout_summaries/2026-09-15T05-42-42-Bgp0-rubato_gui_install_and_t3_stale_queue_pr.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/09/15/rollout-2026-09-15T14-42-42-01a0a396-c7a2-7420-8aef-d722947e4ea6.jsonl, updated_at=2026-09-15T08:40:08+00:00, thread_id=01a0a396-c7a2-7420-8aef-d722947e4ea6, pre/post preservation and actual GUI evidence verified)

### keywords

- Rubato, T3, install-gui.sh, t3-home, rubato-pi, /Applications/Rubato.app, codesign --verify --deep --strict, settings.json, xai/grok-4.6, openai-codex/gpt-5.6-sol, CUA

## Task 2: Preserve original Maplog session, recover stale queue, and prepare PR #12, partial

### rollout_summary_files

- rollout_summaries/2026-09-15T05-42-42-Bgp0-rubato_gui_install_and_t3_stale_queue_pr.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/09/15/rollout-2026-09-15T14-42-42-01a0a396-c7a2-7420-8aef-d722947e4ea6.jsonl, updated_at=2026-09-15T08:40:08+00:00, thread_id=01a0a396-c7a2-7420-8aef-d722947e4ea6, recovery verified locally; PR merge deferred for unresolved CI)

### keywords

- stale-queue, pendingMessageCount, isStreaming, Resume, Discard, replay failure, PR #12, cbb13a29a578b25c73c4e44c41e22941f0e1dd7c, restart-profile.test.mjs, no-pid, MERGEABLE, UNSTABLE, gh pr checks

## User preferences

- when the user asked “우리 세팅 그대로인지 확인” -> installs must prove preservation with pre/post config/auth/model-store hashes and actual UI evidence, not infer it from a launched process. [Task 1]
- when personal commits/settings such as `v0.4+r2` and an existing session matter -> treat them as off-limits, preserve them explicitly, and use a new recovery session instead of destructive migration. [Task 2]
- when a PR is mergeable but CI is unstable, the user asked whether to merge directly or wait -> report technical mergeability separately from the recommendation; do not merge with unresolved red/pending checks without explicit approval. [Task 2]

## Reusable knowledge

- Run `bash harness/t3-integration/install-gui.sh --apply` from `/Users/wooojin/dev/Rubato`. GUI data is `~/.rubato/t3-home`; GUI Pi profile is `~/.rubato-pi/agent`; existing CLI profile remains `~/.rubato/agent`. `/Applications/Rubato.app` points to the built runtime bundle, and `codesign --verify --deep --strict /Applications/Rubato.app` passed. [Task 1]
- Verify install preservation by comparing pre/post hashes and then observing existing projects, sessions, and models in the actual app. GUI default `xai/grok-4.6` and CLI default `openai-codex/gpt-5.6-sol` are intentionally separate. [Task 1]
- In this incident, preserve original session `01a0993f-d6f1-799f-8e7a-f0defac63083`; recover in new `01a0a42b-c9f9-7117-85c1-c9feca2e6b4b`. The fix retains a non-streaming pending queue, offers Resume/Discard, and retains unsent messages after replay failure. Actual recovery reduced the queue from 3 to 0 while tool execution continued. [Task 2]
- Review PR state with `gh pr view 12 --json ...`, `gh pr checks 12`, and failing-job logs; compare the failed job’s ownership with the changed-file scope. Local evidence was bridge 27 pass, full T3 integration 34 pass/5 skipped, source apply/idempotence/remove/dirty-guard, typecheck, build, and Codex audit all passing. [Task 2]

## Failures and how to do differently

- Symptom: CUA display-name lookup times out. Cause: the app is running under a discoverable bundle ID rather than the queried display name. Fix: use `cua.getState()` to find `app.rubato.t3`, then rebind by bundle ID; Peekaboo was unavailable and is only a `--no-remote` fallback. [Task 1]
- Symptom: CI note text corrupts while editing a PR body. Cause: shell heredoc backticks were command-substituted. Fix: use a quoted heredoc, `<<'EOF'`. [Task 2]
- Symptom: PR is `MERGEABLE` but `mergeStateStatus=UNSTABLE`, `checkpoint` fails on `harness/pi-server/test/restart-profile.test.mjs` with `reason: "no-pid"`, and `stock-pi` remains pending. Fix: do not wave off the failure merely because it appears outside the changed files; document it and wait for stock-pi plus an explicit failure-allowance decision before merging. The rollout ended before merge, and reinstall/merge can interrupt the running recovery session. [Task 2]

# Task Group: local Codex/Rubato CLI configuration and plain-Codex isolation
scope: `/Users/wooojin` macOS zsh 환경에서 Rubato가 결합된 기본 Codex와 순정 Codex를 분리해 실행·진단할 때의 cwd/config 탐색 경계와 검증 절차다. 실제 프로젝트의 `.codex`는 별도 점검 대상이며, 이 메모는 설정을 변경하거나 secret을 출력할 근거가 아니다.
applies_to: cwd=/Users/wooojin; reuse_rule=이 설치 상태와 `CODEX_HOME=$HOME/App/codex-plain-home`에는 재사용 가능하다. Codex 버전·프로젝트 `.codex`·native hook은 바뀔 수 있으므로 새 세션과 대상 cwd에서 다시 진단한다.

## Task 1: 일반 Codex와 Rubato Codex 분리 실행 경로 조사, partial

### rollout_summary_files

- rollout_summaries/2026-09-12T12-16-13-EmC7-codex_rubato_separation_cwd_config_injection.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/09/12/rollout-2026-09-12T21-16-13-01a0958b-f918-7ac2-abff-3059bed017d3.jsonl, updated_at=2026-09-12T12:26:34+00:00, thread_id=01a0958b-f918-7ac2-abff-3059bed017d3, neutral-cwd plain-Codex verification; project-cwd behavior remains a per-project check)

### keywords

- Codex, Rubato, CODEX_HOME, codex plugin list, codex doctor --json, cwd, project .codex, AGENTS.md, config.toml, openai_base_url, model_instructions_file, No Rubato paths found, MCP servers=0

## User preferences

- when the user asked “일반 codex만 사용해보려면 어떻게 할까?”, “확인좀해줘”, then reported Rubato instructions still appeared -> do not finish configuration-separation guidance with a command alone; inspect the actual executable/effective config and verify a new session's plugin list, instructions, and doctor result. [Task 1]

## Reusable knowledge

- At the 2026-09-12 check, `/opt/homebrew/bin/codex` was `codex-cli 0.154.0`; `rubato` was a zsh function calling `~/.local/bin/rubato-personal`, not a separate binary. The default `~/.codex/config.toml` contained Rubato `model_instructions_file`, local `openai_base_url`, Rubato plugin/marketplace configuration, so the plain home must not be conflated with the default home. [Task 1]
- The verified neutral-environment invocation was `cd /tmp` then `CODEX_HOME="$HOME/App/codex-plain-home" /opt/homebrew/bin/codex`. In that cwd, `codex plugin list` and `codex doctor --json` showed no Rubato paths or plugin, provider `openai`, and `MCP servers=0`. [Task 1]
- `CODEX_HOME` changes the user-config/global-`AGENTS.md` base, but Codex can still discover configuration from the current project cwd. For real work, start plain Codex in the target project directory and inspect that project's `.codex`; do not use `/Users/wooojin` itself as the neutral test cwd. [Task 1]

## Failures and how to do differently

- Symptom: a fresh `CODEX_HOME` still shows Rubato instructions or plugins. Cause: starting in `/Users/wooojin` allowed its project-scope `.codex` configuration to be discovered. Fix: move first to `/tmp` (or a controlled target project cwd), then run `codex plugin list` and `codex doctor --json`; confirm the effective provider, MCP count, config paths, and absence of Rubato paths before calling it separated. [Task 1]
- Do not state that an empty or alternate `CODEX_HOME` is complete isolation without testing cwd/project config discovery and the new session's `base_instructions`. [Task 1]
- Secret-bearing shell/config output can expose credentials. Never store or repeat values; redact as `[REDACTED_SECRET]` and recommend revocation/rotation when a long-lived token is observed. [Task 1]

# Task Group: Maplog document reset, Place·Visit product direction, and approval boundary
scope: `/Users/wooojin/App/maplog`에서 최신 제품 정의를 다시 세우고 Place·Visit 감상·선택 경험을 검토할 때, 문서 정비·방향 탐색·기술 연결·제품 UX 구현의 승인 범위를 분리하는 기준이다. 임시 테스트 UI를 제품 기준안으로 굳히지 않는다.
applies_to: cwd=/Users/wooojin/App/maplog; reuse_rule=Maplog의 새 세션·제품 방향·UX 탐색에 재사용한다. 현재 입구 문서와 실제 코드 의존성은 매번 다시 확인하며, 이 메모는 구체 화면 구현의 승인 자체가 아니다.

## Task 1: 최신 제품 정의와 문서 구조 재정비, success

### rollout_summary_files

- rollout_summaries/2026-09-10T06-22-54-UpGH-maplog_document_reset_overreach_place_visit_ux.md (cwd=/Users/wooojin/App/maplog, rollout_path=/Users/wooojin/.codex/sessions/2026/09/10/rollout-2026-09-10T15-22-54-01a089fb-c639-75e1-90a3-ed805c65ee7b.jsonl, updated_at=2026-09-10T08:22:52+00:00, thread_id=01a089fb-c639-75e1-90a3-ed805c65ee7b, current entrypoints and product framing reset)

### keywords

- Maplog, record/PRODUCT.md, record/CURRENT.md, record/README.md, document-reset, Place-first, Visit, Journey, DisplayCluster, Recap A안, private-first memory map

## Task 2: Place·Visit browse 연결과 UX 범위 과잉 교정, partial

### rollout_summary_files

- rollout_summaries/2026-09-10T06-22-54-UpGH-maplog_document_reset_overreach_place_visit_ux.md (cwd=/Users/wooojin/App/maplog, rollout_path=/Users/wooojin/.codex/sessions/2026/09/10/rollout-2026-09-10T15-22-54-01a089fb-c639-75e1-90a3-ed805c65ee7b.jsonl, updated_at=2026-09-10T08:22:52+00:00, thread_id=01a089fb-c639-75e1-90a3-ed805c65ee7b, runtime connection verified but UX implementation exceeded approval)

### keywords

- Place·Visit, MapFeatureRootView.swift, PhotoLibraryService.swift, SceneCatalogSync.swift, PlaceVisit.swift, simulator, BUILD SUCCEEDED, date browse, scroll, swipe album, 이어보기 버튼, scope-creep

## User preferences

- when the user said “구문서는 아카이브로서 전부 읽을 필요없고 분기점 이후 문서 기준” -> 최신 입구와 분기점 이후 기록을 먼저 읽고, 과거 plans/ops는 필요한 근거로만 확인한다. [Task 1]
- when the user said “기존 코드 재활용 및 강화할 가능성이 높기때문에 아예 버리는건 아니라고” -> 방향 전환을 코드 폐기로 등치하지 말고 실제 의존성을 확인해 선별 재사용한다. [Task 1]
- when the user said “읽어만 봐. 아직 작업 아니야”, later corrected “내가 바로 구현해보라고 하지 않았는데” -> 읽기·문서 정비·방향 탐색은 구현 승인이 아니다; 대상·범위·완료 조건을 짧게 확인한 뒤에만 구현한다. [Task 2]
- when the user said “상하스크롤인지 아님 스와이프 앨범 식인지 ... 다양한 방향성이 많잖아” -> 감상·선택 UX는 임시안 하나를 기준안처럼 구현하지 말고, 핵심 변수와 비교 가능한 대안을 먼저 제시한다. [Task 2]
- when the user said “몇번 만져보면 되는 검증은 ... 낑낑댈 필요없고 ... 과하거나 기존대로라면 잘 유지되는 부분은 검증하지 말아줘” -> 단순 체험을 장시간 QA로 키우지 말고 새 연결·데이터 보존 위험만 좁게 확인한다. [Task 2]

## Reusable knowledge

- 현재 제품은 기존 사진에서 Place를 발견하고, 그 장소의 capture-local day별 `Visit = Place + capture-local day`를 감상·선택해 Journey로 다시 보는 private-first 기억 지도다. Place가 지도 1순위이고 Journey는 사용자가 고른 Visit 순서이며 DisplayCluster는 정체성·저장 상태를 바꾸지 않는다. [Task 1]
- 현재 입구는 `record/CURRENT.md`, `record/PRODUCT.md`, `record/README.md`다. `record/v2/*`, plans, branchpoint, ops는 원문·근거로 보존하지만 자동 실행 지시가 아니다. 9/3 Recap A안은 iPhone 14에서 사용자가 마음에 들어 한 출발 자산일 뿐 제품 통합·출시 품질 완료 증거가 아니다. [Task 1]
- 테스트 보관함에서는 7개 Place와 장소 열기 → 날짜별 사진 → 확대·복귀 → Visit 선택/해제/0개/재선택/취소 흐름이 동작했고 `/tmp/maplog-place-build.log`에 `BUILD SUCCEEDED`가 남았다. 이는 기술 연결 증거이지 실사진 감상 품질·Recap 가치를 검증한 것은 아니다. [Task 2]

## Failures and how to do differently

- 증상: 문서 재정비 뒤 Place·Visit 화면 구현까지 진행한다. 원인: 문서 재정비 승인과 제품 구현 승인을 혼동했다. 수정: 문서 재정비 → 방향 탐색 → 최소 기술 연결 → 제품 UX 구현을 각각 별도 승인으로 둔다. [Task 1][Task 2]
- 증상: 날짜 선택 UI 하나를 만든 후 그 안을 평가해 달라고 한다. 원인: 탐색해야 할 UX 공간을 임시 구현으로 닫았다. 수정: 장소를 연 뒤 “이날을 이어 보고 싶다”로 넘어가는 경험에서 스크롤·앨범/스와이프·선택 시점/위치를 먼저 비교하거나 질문한다. [Task 2]
- 증상: 테스트 데이터에서 동작하고 build가 성공했으니 제품 경험도 검증됐다고 여긴다. 원인: 조작성과 감상 품질을 분리하지 못했다. 수정: runtime은 새 연결과 데이터 보존만 확인하고, 실제 사진 경험과 다음 행동의 명료성은 별도 사용자 판단으로 남긴다. [Task 2]

# Task Group: MapleStory 챌린저스 시즌4 보상 반입과 레공레 이지 벨로나 판단
scope: `/Users/wooojin/dev/maple`에서 챌린저스 보상·월드 리프와 레공레 보스 도전을 조사·조언할 때 쓴다. 시즌 공지와 현재 캐릭터/실전 기록을 함께 보며, 보상 전체표의 미완결 상태와 보스 배율의 한계를 명시한다.
applies_to: cwd=/Users/wooojin/dev/maple; reuse_rule=챌린저스 시즌4와 `레공레` 관련 후속 질문에 재사용한다. 이벤트 보상·리프 규정·Maplescouter 수치는 시점 의존적이므로 답변 전 최신 공식 공지와 snapshot을 다시 확인한다.

## Task 1: 200레벨 비약과 챌린저스 보상·코인샵 반입 분류, partial

### rollout_summary_files

- rollout_summaries/2026-09-10T06-19-59-GK85-maplestory_challenger_rewards_bellona_difficulty.md (cwd=/Users/wooojin/dev/maple, rollout_path=/Users/wooojin/.codex/sessions/2026/09/10/rollout-2026-09-10T15-19-59-01a089f9-1c16-7771-b0ff-44d3883daafd.jsonl, updated_at=2026-09-10T07:19:04+00:00, thread_id=01a089f9-1c16-7771-b0ff-44d3883daafd, official transfer restrictions confirmed; full event-by-event table incomplete)

### keywords

- MapleStory, 챌린저스 시즌4, 200레벨 달성의 비약, 250레벨 달성의 비약, 월드 리프, 코인샵, 메멘토 골드 큐브, 카르마 브론즈 에디셔널 큐브, 160제 카르마 17성권, 에오스, 핼리오스, lwi.nexon.com

## Task 2: 레공레 이지 벨로나 난이도와 패턴 병목 판단, success

### rollout_summary_files

- rollout_summaries/2026-09-10T06-19-59-GK85-maplestory_challenger_rewards_bellona_difficulty.md (cwd=/Users/wooojin/dev/maple, rollout_path=/Users/wooojin/.codex/sessions/2026/09/10/rollout-2026-09-10T15-19-59-01a089f9-1c16-7771-b0ff-44d3883daafd.jsonl, updated_at=2026-09-10T07:19:04+00:00, thread_id=01a089f9-1c16-7771-b0ff-44d3883daafd, Maplescouter feasibility separated from first-clear difficulty)

### keywords

- 레공레, 이지 벨로나, Maplescouter, 130.8%, 인세인, 핀볼, 중앙 아래 돌진, 광폭화 양날도끼, 데스카운트, 하드 메이린, 19분 46초

## User preferences

- when the user asked for “모든 보상들”, “이벤트별 코인샵별” -> 보상을 직접 수령, 캐릭터 인벤토리로 리프, 리프 불가 열로 나눈 압축표부터 제시한다. [Task 1]
- when the user said “꽤 어렵더라고” -> 보스 배율만으로 클리어 시간·체감 난이도를 낙관하지 말고 패턴 숙련도, 직업별 딜로스, 실제 커뮤니티 사례를 함께 반영한다. [Task 2]

## Reusable knowledge

- 200레벨/250레벨 달성의 비약은 챌린저스 월드에서 쓸 수 없고 본섭에서 사용한다. 유니온용 캐릭터가 이미 대부분 200 이상이면 신규 육성 일반론보다 200대 저레벨 캐릭터에 분산하는 계정 상태별 최적화를 우선한다. [Task 1]
- 사전 리프와 종료 리프는 합산 최대 5캐릭터이며 최초 도착 월드는 변경 불가다. 챌린저스1~3의 대상은 스카니아·베라·루나·제니스·크로아·유니온·엘리시움·이노시스·레드·오로라·아케인·노바, 챌린저스4는 에오스·핼리오스다. 메멘토 큐브류, 카르마 브론즈 에디셔널 큐브, 160제 카르마 17성권, 챌린저스 3·4레벨 특수 스킬링/획득 링, 메이린 에테르넬 조각은 리프 전에 사용해야 한다. [Task 1]
- 2026-09-10 Maplescouter의 레공레는 Lv.286, 전투력 1억 2,525만, 보스380, 헥사환산 49,283, 이지 벨로나 130.8% 솔플 가능이었다. 이는 딜 부족이 아니라 패턴 숙련이 병목일 가능성을 뜻한다. 하드 메이린 110.5%를 19분 46초에 실제 클리어한 기록도 있다. [Task 2]
- 벨로나는 인세인에서 피격하면 보스 회복과 데스카운트 손실이 생겨 생존 실패가 딜로스로 이어진다. 2페이즈 50% 이하 핀볼, 중앙 아래 돌진, 광폭화 양날도끼에서는 평딜보다 회피를 우선하고, 숙련 뒤 평딜을 더한다. 연습 목표는 해당 구간 진입 때 데스카운트 4개 이상이다. [Task 2]

## Failures and how to do differently

- 증상: 아이템 종류·사용 제한을 확인하기 전에 비약 활용을 추정한다. 원인: 공식 아이템 설명과 시즌 공지를 뒤늦게 봤다. 수정: 사용처·리프 가능성은 공식 설명/시즌 공지부터 고정한다. [Task 1]
- 증상: 긴 PNG 이벤트 본문을 통째로 OCR해 탐색이 길어진다. 원인: 이미지 구조를 활용하지 않았다. 수정: HTML에서 `lwi.nexon.com` 이미지 URL을 뽑고 1,600~2,000px 단위 crop/OCR 후 이벤트별 보상·교환 속성·기한을 구조화한다. 아직 완결된 전체표는 없음을 명시한다. [Task 1]
- 증상: 130.8%만 보고 16~17분 클리어를 예상한다. 원인: ratio가 패턴·직업별 딜로스·숙련을 반영하지 않는다. 수정: “스펙상 가능”과 “첫 클리어 체감 난이도”를 분리하고, 첫 트라이 실패·장시간 연습은 정상 범위로 설명한다. [Task 2]




# Task Group: macOS Aside bundled-rg security-warning troubleshooting
scope: `/Users/wooojin`의 Aside가 반복적으로 macOS 보안 경고를 띄우거나 검색을 멈출 때, 실제 실행 바이너리의 quarantine/rejection을 확인하고 검증된 대체 경로를 복구하는 로컬 데스크톱 장애 대응이다.
applies_to: cwd=/Users/wooojin; reuse_rule=이 Mac의 Aside runtime과 Homebrew ripgrep에는 재사용 가능하다. Aside 업데이트가 내장 바이너리를 복원할 수 있으므로 재발 시 경로·링크·업데이트 여부를 다시 확인하고, 다른 앱에는 원인을 먼저 검증한다.

## Task 1: Replace Aside's quarantined bundled rg, success

### rollout_summary_files

- rollout_summaries/2026-08-20T13-29-37-oMyf-fix_aside_rg_macos_security_warning.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/08/20/rollout-2026-08-20T22-29-37-01a01f5c-e998-7b62-96fb-5484a42b5beb.jsonl, updated_at=2026-08-20T13:32:41+00:00, thread_id=01a01f5c-e998-7b62-96fb-5484a42b5beb, verified root-cause replacement; recheck after Aside updates)

### keywords

- macOS, Aside, rg, ripgrep, quarantine, com.apple.quarantine, spctl, syspolicyd, CoreServicesUIAgent, xattr, /Users/wooojin/.aside/runtime/native/bin/rg, /opt/homebrew/bin/rg

## User preferences

- when the repeated warning persisted, the user said: "이것좀 그만 뜨게해봐!!!!!!!!!!" -> remove the recurring root cause instead of merely dismissing the current dialog; report the cause, applied change, recurrence condition, and actual re-run verification concisely. [Task 1]

## Reusable knowledge

- Aside invoked `/Users/wooojin/.aside/runtime/native/bin/rg`; the bundled executable had `com.apple.quarantine`/provenance metadata and `/usr/sbin/spctl --assess --type execute --verbose=4 <path>` reported it as rejected. [Task 1]
- The working repair preserved the original as `/Users/wooojin/.aside/runtime/native/bin/rg.blocked-original-20260820` and made the original path a symlink to `/opt/homebrew/bin/rg`. The replacement reported `ripgrep 15.1.0`; an actual search completed, no new security warning was logged, and `CoreServicesUIAgent` had zero windows. [Task 1]
- To diagnose a recurrence, inspect `xattr -l <path>`, assess the actual executable with `/usr/sbin/spctl`, then inspect `syspolicyd`, `CoreServicesUIAgent`, and `XProtectService` through `log show`; confirm behavior by rerunning a search, not only by checking the link. [Task 1]

## Failures and how to do differently

- Symptom: `spctl` validation fails before assessing the file. Cause: this macOS environment's tool is `/usr/sbin/spctl`, not `/usr/bin/spctl`. Fix: invoke `/usr/sbin/spctl` explicitly. [Task 1]
- Symptom: removing xattrs appears to help but the warning returns. Cause: the quarantined Aside-bundled binary remains the executable or can be restored by an update. Fix: preserve it for rollback, link the known-good Homebrew binary at the invoked path, verify with a real search, and recheck the same path after Aside updates. [Task 1]


# Task Group: OpenAI Game execution gates and later map-redesign input
scope: `/Users/wooojin/App/openaigame`에서 구현·위임 전 단계/근거/허용 범위를 판정하고, 음향 비교 중 들어온 후속 맵 재설계 입력을 구현 승인과 분리하는 현재 운영 관문이다. 실제 플레이 근거 없는 억지 보상/시스템과 승인 전 맵 구현을 막는다.
applies_to: cwd=/Users/wooojin/App/openaigame; reuse_rule=OpenAI Game의 다음 구현·위임·단계 전환에 적용한다. 기준 문서와 현재 버전은 작업 시작 전에 다시 확인하며, 이 규칙을 Maplog 등 다른 프로젝트의 기본 gate로 일반화하지 않는다.

## Task 1: Add persistent pre-implementation anti-forcing gates for OpenAI Game, adopted

### rollout_summary_files

- extensions/ad_hoc/notes/20260815T101212-openaigame-anti-forcing-gates.md (cwd=/Users/wooojin/App/openaigame, rollout_path=none, updated_at=2026-08-15T10:12:12+09:00, thread_id=none, authoritative current execution-gate and Fable-connection note) [ad-hoc note]

### keywords

- OpenAI Game, docs/14-execution-gates.md, REFERENCE, DRAFT, v4, anti-forcing, current stage, one hypothesis, Fable medium, plan mode, Telegram, TELEGRAM_STATE_DIR, telegram-2, @maplog_bot, mirror.last

## Task 2: Preserve follow-up map-redesign input without authorizing implementation, pending

### rollout_summary_files

- extensions/ad_hoc/notes/20260815T193700-openaigame-map-density-height-reveal.md (cwd=/Users/wooojin/App/openaigame, rollout_path=none, updated_at=2026-08-15T19:37:00+09:00, thread_id=none, authoritative follow-up map-redesign input; not implementation authorization) [ad-hoc note]

### keywords

- OpenAI Game, 맵 재설계, 넓어진 거리, 빠른 속도, 배경·전경 사물, 글 없이 안내, 실제 비행선, 상승과 하강, 3단계 바람 구역, 높이와 구조, 음향 비교

## User preferences

- when OpenAI Game implementation or delegation is proposed, the user explicitly requires the current stage and permitted scope to be checked first; `REFERENCE` and `DRAFT` are not implementation authorization. [Task 1] [ad-hoc note]
- when a version is scoped, require exactly `현재 단계 / 판정할 가설 하나 / 근거 문서와 절`; if one is absent or conflicts, reject the implementation brief rather than filling it in. One version judges one hypothesis, not several new systems at once. [Task 1] [ad-hoc note]
- when considering a hidden discovery or reward, explicitly judge `억지가 아닌가`; do not assign meaning merely because an event is already detectable. [Task 1] [ad-hoc note]
- Fable review is input only: the main session must compare it with documents and actual-play evidence, then obtain Woojin's scope approval before implementation. [Task 1] [ad-hoc note]
- map-redesign input is not implementation approval while sound comparison is in progress -> do not start map implementation from this note; retain it as a later design input. [Task 2] [ad-hoc note]

## Reusable knowledge

- The canonical project gate is `/Users/wooojin/App/openaigame/docs/14-execution-gates.md`. Current baseline is v4: do not stack the next version on v5; map and core play come first. [Task 1] [ad-hoc note]
- A hidden discovery/reward is eligible only when all are present: naturally observed real-play behavior, temptation from a pre-existing map/object, an afterward-understandable cause, a verified source of play technique, and a reward that expands behavior. [Task 1] [ad-hoc note]
- Request an independent Fable check at a phase transition, first introduction of a new system, or boundary that turns `REFERENCE`/`DRAFT` into implementation. Do not overuse it for numeric tuning, one-variable experiments within the same stage, or bug fixes. Keep the judgment session Fable medium in plan mode and non-writing; implementation goes to a separately approved, brief-gated session. [Task 1] [ad-hoc note]
- The Fable check uses the existing `@maplog_bot` (`어플개발`) slot at `~/.claude/channels/telegram-2`. Do not enable the global Telegram plugin; configure only that session with `TELEGRAM_STATE_DIR=~/.claude/channels/telegram-2` and the Telegram channel plugin so another session does not capture the bot. Verify the bridge by `mirror.last` updating or by successful Telegram delivery, not merely by a live Claude process. [Task 1] [ad-hoc note]
- For later map redesign, use small background/foreground objects to guide the next airship and wind through direction, spacing, and motion rather than text; reduce big rectangular assemblies in favor of curved, overlapping, asymmetric airships. From stage 3 introduce ascent/descent and make later equipment reveal previously unseen heights/structures; redesign the stage-3 wind approach line and force direction. [Task 2] [ad-hoc note]

## Failures and how to do differently

- Symptom: a `REFERENCE`/`DRAFT` document or easy-to-detect event becomes a new system by implementation convenience. Cause: stage authorization and the anti-forcing judgment were skipped. Fix: stop on a missing/conflicting three-part brief and require the real-play eligibility criteria before coding. [Task 1] [ad-hoc note]
- Symptom: Fable is treated as implementation approval, or its judgment session changes files. Cause: independent review and production authority were blurred. Fix: keep Fable medium/plan/non-writing, then have the main session compare evidence and obtain scope approval before a separate implementation session. [Task 1] [ad-hoc note]
- Symptom: Telegram appears connected because Claude is running, but key stage updates never arrive. Cause: process liveness was mistaken for channel delivery, or the global plugin captured the shared bot. Fix: use the scoped `telegram-2` state directory and confirm `mirror.last` or a real send. [Task 1] [ad-hoc note]

# Task Group: 백석대 2026-2 수강계획의 보류된 기독교세계관 분반 선택
scope: 소프트웨어학전공 3학년 2학기 시간표의 확정 과목과, 여자친구 시간표를 대조한 뒤 결정할 기독교세계관 공용 분반 선택을 보존한다. 현재 성적 위험 판단은 당시 강의평 근거이며 최종 수강신청 확정은 아니다.
applies_to: cwd=/Users/wooojin; reuse_rule=2026-2 시간표 대화·재확인에만 사용한다. 강의 시간·분반·성적 위험은 변경될 수 있으므로 실제 수강신청 전 최신 정보와 두 사람의 확정 시간표를 다시 대조한다.

## Task 1: 백석대 2026-2 시간표 방향과 기독교세계관 결정을 보류, pending

### rollout_summary_files

- extensions/ad_hoc/notes/2026-08-09T00-58-44-baekseok-course-plan.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-08-09T00:58:44+09:00, thread_id=none, authoritative current course-plan note) [ad-hoc note]

### keywords

- 백석대, 2026-2, 소프트웨어학전공, 3학년 2학기, 월·수·목 등교, 화·금 공강, 프런티어십, 컴퓨터공학부 채플, 소프트웨어공학, 빅데이터, 다함께 파이썬, 창의융합 Leading Class, 기독교세계관, 서현덕, 김은득, 기독교탐사

## Reusable knowledge

- Current target pattern is 월·수·목 등교 with 화·금 공강. Confirmed courses are 프런티어십(한정수 월1), 컴퓨터공학부 채플(월3), 소프트웨어공학(이승화 월4,5), 빅데이터(이시은 사이버), 다함께 파이썬(손은영 목5,6), 창의융합 Leading Class(박지연 수7,8). [Task 1] [ad-hoc note]
- Do not finalize 기독교세계관 until the girlfriend's Monday 기독교탐사 time is known; then compare both timetables and choose a shared Monday or Wednesday section. The current grade-first candidate is 서현덕 월2; the existing-attendance-day candidate is 김은득 수4, with higher A-grade risk in lecture evaluations. [Task 1] [ad-hoc note]

## Failures and how to do differently

- Symptom: a single-person timetable optimization prematurely fixes 기독교세계관. Cause: the girlfriend's Monday 기독교탐사 constraint is still unknown. Fix: preserve both 월2 and 수4 candidates, then make the joint-timetable comparison before registering. [Task 1] [ad-hoc note]

# Task Group: Hackathon proof-spine, worktree integration, and final-submission verification
scope: 열린 문제의 해커톤에서 제품 선택부터 구현·협업·제출 검증까지, 대표 주장마다 최종 제출 아카이브에서 재실행 가능한 증거를 연결하는 운영 방식이다. 특정 대회의 제품 판단이나 구현 계획 자체는 이 범위에 포함하지 않는다.
applies_to: cwd=/Users/wooojin; reuse_rule=다음 Cofathon·KB AI Challenge 등 contest workflow에 재사용 가능하다. 대회 원문, 제품 선택, 제출 규격, 정확한 검증 명령은 매 대회마다 새 프로젝트 문서에서 다시 확정한다.

## Task 1: Consolidate Cofathon reproducibility discipline and KB AI Challenge product narrative into a proof-spine workflow, adopted

### rollout_summary_files

- extensions/ad_hoc/notes/2026-08-04T13-23-55+0900-hackathon-proof-spine-workflow.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-08-04T13:23:55+09:00, thread_id=none, authoritative future-contest operating decision) [ad-hoc note]

### keywords

- Cofathon, KB AI Challenge, hackathon, proof spine, 한 줄 → 한 사용자 경로 → 한 코드 경로 → 한 검증 명령 → 한 제출 주장, START_HERE.md, DECISIONS.md, CONTRACT.md, RELEASE.md, AGENTS.md, clean release worktree, claim-evidence, final ZIP

## User preferences

- when preparing the next contest, the user has decided to combine “Cofathon의 동결·재현 규율” with “KB AI Challenge의 제품 서사·다역할 UX” -> use one operating system rather than treating reproducibility and product narrative as separate tracks. [Task 1] [ad-hoc note]
- when an open-ended contest starts, do not lock a detailed implementation plan at the start -> freeze the contest original text, allow independent exploration and the human product choice, then lock one representative path before parallel expansion. [Task 1] [ad-hoc note]

## Reusable knowledge

- The proof spine is `한 줄 → 한 사용자 경로 → 한 코드 경로 → 한 검증 명령 → 한 제출 주장`: every representative sentence needs evidence that can be rerun from the final submission archive. Build the input-one-item through result-return path before parallel UI, runtime, docs, and additional scenarios. [Task 1] [ad-hoc note]
- Use three layers with distinct authority: a personal Codex skill for contest initialization, phase transitions, worktrees/task packets, integration, claim-evidence checks, and final-ZIP re-verification; project `START_HERE.md`, `DECISIONS.md`, `CONTRACT.md`, `RELEASE.md` for current facts/contracts; project `AGENTS.md` only for durable safety rules such as dirty-tree preservation, owner scope, verification integrity, release authority, and no secrets. Keep product value, current work, and long status history out of `AGENTS.md`. Related skill: skills/hackathon-proof-spine/SKILL.md. [Task 1] [ad-hoc note]
- Keep private judgment notes separate from shared meeting notes: `지금 믿는 것 / 찜찜한 것 / 상대에게 전달할 것 / 지금 끝낼 하나 / 나중에 볼 것`; promote only human-confirmed material into the shared decision record. [Task 1] [ad-hoc note]
- Default collaboration topology: shared development host plus independent worktrees per person/agent, one integration owner, and a separate clean release worktree. GitHub is milestone backup/final publication, not the real-time handoff channel. Integrate every 60–90 minutes; check contract changes immediately; if two people must edit the same file, pause parallel work for a short pair session. [Task 1] [ad-hoc note]
- Freeze new features early in release. Extract the exact submission ZIP into a fresh directory and run install, build, test, hero smoke, PDF render, and claim-evidence comparison there; only that archive-level result can be final PASS. [Task 1] [ad-hoc note]

## Failures and how to do differently

- Symptom: documents grow but SSOT keeps moving, fixture UI is disconnected from runtime, or the last integration is rushed. Cause: document authority/lifetime, people/agent ownership, and phase-transition conditions were not narrow and explicit. Fix: use the three-layer structure and lock the proof spine before broad parallelism. [Task 1] [ad-hoc note]
- Symptom: parallel `main` push/pull is used as live coordination, or the same file is edited concurrently. Cause: GitHub and worktree boundaries were treated as collaboration protocol. Fix: keep worktrees independent under one integration owner; use milestone GitHub sync and pair briefly for shared-file edits. [Task 1] [ad-hoc note]
- Symptom: the working repository passes but the submitted artifact cannot substantiate the claims. Cause: final submission archive was not revalidated. Fix: re-extract the exact ZIP into a clean directory and run the complete release checklist before calling it PASS. [Task 1] [ad-hoc note]

# Task Group: Maplog structure-first implementation and design-stage boundary
scope: `/Users/wooojin/App/maplog`에서 기능·권한·데이터 흐름을 연결하는 구현 단계와 별도 감성/시각 디자인 단계를 혼동하지 않고, native interaction과 필수 UX를 먼저 안정시킬 때 쓴다.
applies_to: cwd=/Users/wooojin/App/maplog; reuse_rule=Maplog의 제품·개발 작업에는 재사용 가능하다. 다만 구체 UI/구현 우선순위는 메인 SSOT와 현재 task boundary를 다시 확인한다.

## Task 1: Set the Maplog pre-design implementation boundary, success

### rollout_summary_files

- extensions/ad_hoc/notes/20260722-012325-maplog-design-stage-boundary.md (cwd=/Users/wooojin/App/maplog, rollout_path=none, updated_at=2026-07-22T01:23:25+09:00, thread_id=none, user-confirmed design-stage boundary and primary product/development SSOT) [ad-hoc note]

### keywords

- Maplog, 디자인 단계 전 구현 원칙, 최소 정보 구조, native interaction, loading, empty, error, 복구, 접근성, 개인정보 경계, 2026-07-12_product_development_plan.md

## User preferences

- when Woojin confirmed the 2026-07-22 boundary for a stage that connects `기능·권한·데이터 흐름` -> 최소 정보 구조와 native interaction을 먼저 안정시키고, 감성·시각 완성도는 별도 디자인 단계에서 일관되게 입힙니다. 임시 시각안을 최종 디자인처럼 굳히거나 조각마다 과도하게 다듬지 않습니다. [Task 1] [ad-hoc note]
- when working before the visual-design stage -> 뒤로가기·주 행동·loading/empty/error·복구·접근성·개인정보 경계처럼 기능 이해와 안전에 필수인 UX는 생략하지 않습니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- Maplog의 메인 제품·개발 SSOT는 `/Users/wooojin/App/maplog/record/plans/2026-07-12_product_development_plan.md`다. 구현 단계의 scope/순서는 이 문서부터 대조한다. [Task 1] [ad-hoc note]
- pre-design implementation은 bare functionality가 아니라 최소 정보 구조, native interaction, 안전·복구·접근성 경계를 갖춘 usable slice를 뜻한다. visual polish는 functional structure가 안정된 뒤 일관된 단계로 묶는다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: 임시 시각안을 최종 디자인처럼 굳히거나 기능 조각마다 과도하게 다듬어 구조 결정을 지연시킨다. 원인: 구현 단계와 감성·시각 완성도 단계를 섞었다. 수정: 현재 작업이 기능·권한·데이터 흐름을 잇는 단계면 SSOT 기준 최소 구조/native interaction과 필수 UX만 완료하고 디자인 polish는 별도 단계로 넘긴다. [Task 1] [ad-hoc note]

# Task Group: MapleStory HEXA/VI skill delta and hexaOrder decision workflow
scope: MapleStory에서 새 VI/HEXA core를 지금 열지, `hexaOrder`를 기다릴지, 특정 burst/boss threshold 때문에 당길지를 판단할 때 기존 V/IV 대비 실제 증가분과 현재 자원을 함께 확인하는 workflow다.
applies_to: cwd=/Users/wooojin/dev/maple; reuse_rule=같은 로컬 Maple character snapshot과 HEXA 상담에는 재사용 가능하다. skill tooltip, `hexaOrder`, character resources, boss target은 live-state-specific이므로 매 질문마다 다시 확인한다.

## Task 1: Record HEXA/VI skill opening and late-hexaOrder decision workflow, success

### rollout_summary_files

- extensions/ad_hoc/notes/2026-07-21-hexa-skill-delta-workflow.md (cwd=/Users/wooojin/dev/maple, rollout_path=none, updated_at=2026-07-21T00:00:00+09:00, thread_id=none, authoritative note for VI/HEXA opening and hexaOrder decision routing) [ad-hoc note]

### keywords

- MapleStory, VI, HEXA, hexaOrder, hexa-skill-workflow.md, growth-assistant.mjs, `skill <character> <skill>`, V core, IV tooltip, VI tooltip, Maplescouter, burst threshold, boss target

## User preferences

- when Woojin asks whether a new VI/HEXA skill should be opened or why it is late in `hexaOrder` -> conclusion first: `open now`, `wait for order`, or pull forward only for a specific burst/boss threshold; personalize it with current character resources and boss target. [Task 1] [ad-hoc note]

## Reusable knowledge

- Start with `/Users/wooojin/dev/maple/kb/hexa-skill-workflow.md`, refresh the character snapshot when stale, then run `node tools/growth-assistant.mjs skill <character> <skill>` to inspect the existing V core, active HEXA core, and recorded resources. [Task 1] [ad-hoc note]
- Compare the existing V/IV tooltip with the VI tooltip and remove repeated text. Never count the full VI tooltip as incremental damage; separate reprinted effects, true numerical additions, and structural interactions. [Task 1] [ad-hoc note]
- Verify class interactions with official notes plus focused class-board experiments, then check the live Maplescouter `hexaOrder`. A later rank means cheaper competing gains exist; it does not automatically make the core bad. [Task 1] [ad-hoc note]
- Stop once existing-to-new delta, important interactions, live order, and resource constraint are known; do not continue broad research after a personalized conclusion is supported. [Task 1] [ad-hoc note]

## Failures and how to do differently

- Symptom: the full VI tooltip is reported as the new skill's damage gain. Cause: reprinted V/IV effects were not removed from the comparison. Fix: calculate only the existing-to-VI delta and label numerical additions versus structural interactions separately. [Task 1] [ad-hoc note]
- Symptom: a late `hexaOrder` is treated as proof that the core should never be opened. Cause: relative opportunity cost was flattened into a binary quality judgment. Fix: compare competing gains and current resources; pull the core forward only when its burst/boss threshold justifies it. [Task 1] [ad-hoc note]

# Task Group: Maplog completed-work reporting and provenance discipline
scope: `/Users/wooojin/App/maplog`에서 구현/QA/문서화가 끝난 뒤 Woojin에게 결과를 다시 설명하거나 project record를 남길 때, plain-language summary와 provenance/status를 섞지 않고 정리하는 기본 reporting contract로 쓴다.
applies_to: cwd=/Users/wooojin/App/maplog; reuse_rule=같은 Maplog repo의 completed-work report, wrap, handoff, project-record 업데이트에는 재사용 가능하다. 다만 실제 결정 출처와 verification evidence는 해당 run 기준으로 다시 확인해야 한다.

## Task 1: Record Maplog explanation-first reporting and provenance/status defaults, success

### rollout_summary_files

- extensions/ad_hoc/notes/20260711-224807-maplog-explanation-and-provenance.md (cwd=/Users/wooojin/App/maplog, rollout_path=none, updated_at=2026-07-11T22:48:07+09:00, thread_id=none, authoritative note for completed-work reporting, provenance labeling, and decision-status discipline) [ad-hoc note]

### keywords

- Maplog, completed-work report, plain Korean summary, provenance, decision status, user-confirmed, assistant recommendation, research inference, implemented, verified, superseded, next unresolved decision

## User preferences

- when Woojin brings back a completed-work report, first explain in plain Korean `what actually changed, how it connects to the original plan, what the user can now do, and what remains` -> 다음 구현 프롬프트로 바로 점프하지 말고 explanation-first closeout를 기본값으로 둡니다. [Task 1] [ad-hoc note]
- when recording Maplog decisions, do not write assistant recommendations, research conclusions, or implementation-agent judgments as Woojin's intent or as a user-confirmed decision -> decision source를 명시적으로 분리합니다. [Task 1] [ad-hoc note]
- when a decision came from Woojin, preserve a short verbatim quote and the date/context when available -> 사용자 판단은 paraphrase만 남기지 말고 짧은 원문 anchor를 함께 남깁니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- project record 기본 순서는 `plain-language summary first -> provenance/status -> implementation facts -> verification evidence -> next unresolved decision`이 가장 reread-friendly하면서도 future-agent handoff에 충분하다. [Task 1] [ad-hoc note]
- provenance label은 최소 `user-confirmed`, `assistant recommendation`, `research inference`, `implementation decision`, `observed QA evidence`를 구분해서 쓴다. [Task 1] [ad-hoc note]
- decision status는 `proposed`, `user-confirmed`, `implemented`, `verified`, `superseded`, `user-confirmation-pending` 같은 explicit status vocabulary로 남기는 편이 검색과 stale cleanup에 유리하다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: completed-work report가 바로 다음 구현 지시로 넘어가서 사용자가 `이번에 뭐가 바뀌었는지` 다시 물어야 한다. 원인: closeout보다 handoff를 먼저 썼다. 수정: plain Korean으로 changed/plan-link/now-possible/remaining을 먼저 설명한다. [Task 1] [ad-hoc note]
- 증상: assistant proposal이나 research conclusion이 사용자 의사결정처럼 기록된다. 원인: source label 없이 결론만 압축했다. 수정: 각 decision에 provenance label을 붙이고, Woojin 결정이면 짧은 quote/date anchor를 남긴다. [Task 1] [ad-hoc note]
- 증상: 같은 문서 안에서 현재 상태가 proposal인지 implemented인지 헷갈린다. 원인: explicit decision status를 생략했다. 수정: `proposed` / `implemented` / `verified` / `superseded` / `user-confirmation-pending` 같은 상태를 각 항목에 붙인다. [Task 1] [ad-hoc note]

# Task Group: Maplog implementation prompt model routing
scope: `/Users/wooojin/App/maplog`의 구현 프롬프트에서 작업 성격에 맞는 모델·추론 강도와 writable-repo 경계를 먼저 고정할 때 쓴다.
applies_to: cwd=/Users/wooojin/App/maplog; reuse_rule=현재 Maplog의 prototype discovery와 approved production integration routing에만 재사용한다. 모델 availability와 exact effort는 프롬프트 시작 전 다시 확인한다.

## Task 1: Route Maplog prompts between Claude Fable prototype work and GPT-5.6 Terra production integration, user-confirmed

### rollout_summary_files

- extensions/ad_hoc/notes/2026-07-12-maplog-model-routing-preference.md (cwd=/Users/wooojin/App/maplog, rollout_path=none, updated_at=2026-07-12T18:59:51+09:00, thread_id=none, authoritative note for starting Maplog implementation prompts with a concrete model and reasoning recommendation, splitting Fable prototype work from Terra integration work) [ad-hoc note]

### keywords

- Claude Fable, GPT-5.6 Terra, very high reasoning, model routing, implementation prompt, read-only prototype, writable repository isolation, motion, feel, data contracts, regression tests

## User preferences

- when Woojin explicitly requested that future implementation prompts begin with a concrete recommendation for which available model and reasoning effort should run that task -> 프롬프트 맨 위에서 `추천 모델 + reasoning effort + 왜 이 라우팅인지`를 먼저 고정합니다. [Task 1] [ad-hoc note]
- when the work is a high-ambiguity, product-defining visual interaction prototype where user intent, convenience, motion, and feel must be discovered and demonstrated -> Claude Fable first를 기본값으로 두고, real repo write는 분리합니다. [Task 1] [ad-hoc note]
- when the work is approved-interaction integration in the real Maplog repo, including persistence, data contracts, edge cases, performance, regression tests, QA evidence, and documentation -> GPT-5.6 Terra with very high reasoning을 기본값으로 둡니다. routine specified UI edits와 non-visual implementation도 Terra 쪽으로 바로 보냅니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- current routing default는 two-step이다: high-ambiguity visual interaction prototype은 Claude Fable first, approved interaction을 real Maplog repo에 integrating하는 작업은 GPT-5.6 Terra with very high reasoning으로 넘긴다. Fable은 read-only or isolated로 두고, Terra와 같은 writable repo를 동시에 잡지 않는다. [Task 1] [ad-hoc note]
- routine, already-specified UI edits와 non-visual implementation work는 Fable prototype 없이 Terra로 바로 가도 된다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: implementation prompt를 시작할 때 어떤 모델이 맡아야 하는지 다시 길게 합의해야 한다. 원인: task type별 routing default를 프롬프트 맨 앞에 고정하지 않았다. 수정: `prototype-discovery면 Fable / production integration이면 Terra very high` recommendation을 prompt header에 먼저 둔다. [Task 1] [ad-hoc note]
- 증상: Fable prototype과 Terra production integration이 같은 writable repo에서 동시에 돌아 충돌하거나 provenance가 흐려진다. 원인: prototype surface와 implementation surface를 분리하지 않았다. 수정: Fable은 read-only or isolated로 돌리고, 승인된 mechanics만 Terra가 real repo에 통합한다. [Task 1] [ad-hoc note]


# Task Group: MapleStory YouTube research playback safety
scope: MapleStory YouTube 영상에서 특정 시점의 시각 증거가 필요한 리서치를 할 때 transcript/subtitle 우선, muted playback, isolated browser profile을 적용한다. 영상의 내용·시세·게임 판단 자체는 별도 리서치 workflow에서 검증한다.
applies_to: cwd=/Users/wooojin/dev/maple; reuse_rule=MapleStory YouTube research에 재사용 가능하다. 영상 재생은 특정 timestamp의 시각 증거가 필요할 때만 하며, 개인 Chrome profile은 이 workflow 범위 밖이다.

## Task 1: Record transcript-first and muted YouTube inspection rule, success

### rollout_summary_files

- extensions/ad_hoc/notes/20260723-142415-maple-youtube-muted-playback.md (cwd=/Users/wooojin/dev/maple, rollout_path=none, updated_at=2026-07-23T14:24:15+09:00, thread_id=none, authoritative playback-safety rule) [ad-hoc note]

### keywords

- MapleStory, YouTube research, transcript, subtitles, timestamp, visual evidence, --mute-audio, player mute, headless Chrome, isolated browser profile, real Chrome profile

## User preferences

- when MapleStory YouTube research is needed -> existing transcripts or subtitles come first; open a video only for visual evidence at a specific timestamp. [Task 1] [ad-hoc note]
- when browser or headless Chrome must inspect a video -> mute before playback and use an isolated profile, never Woojin's real Chrome profile. [Task 1] [ad-hoc note]

## Reusable knowledge

- Use `--mute-audio` or the player mute control before any video inspection. The isolated-profile requirement applies equally to browser and headless Chrome. [Task 1] [ad-hoc note]

## Failures and how to do differently

- Symptom: research opens videos by default or plays audio through the user's normal browser profile. Cause: transcript-first and isolated muted playback were not treated as the default. Fix: inspect transcript/subtitles first; only open a required timestamp in a muted, isolated profile. [Task 1] [ad-hoc note]

# Task Group: MapleStory challenger-server market and community research workflow
scope: MapleStory 챌섭 장비, 주문서, 보스컷, 시세, 커뮤니티 여론을 빠르게 조사해야 할 때 캐릭터 snapshot, 로컬 KB, 최소한의 커뮤니티 렌더를 병렬로 묶어 재사용할 때 쓴다.
applies_to: cwd=/Users/wooojin; reuse_rule=같은 MapleStory 챌섭 시세/커뮤 리서치 workflow에는 재사용 가능하지만, 실제 매물가와 여론은 시점 의존적이므로 character snapshot과 최신 KB를 먼저 다시 확인해야 한다.

## Task 1: Record fast challenger-server market/community research workflow, success

### rollout_summary_files

- extensions/ad_hoc/notes/2026-07-10-002003-maple-challenger-scroll-workflow.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-07-10T00:20:03+09:00, thread_id=none, authoritative note for fast MapleStory challenger-server pricing and community research routing) [ad-hoc note]

### keywords

- MapleStory, 챌섭, 챌린저, 시세, 커뮤, 주문서, 카레잠, 카헤잠, 미트라, 블랙보조, item-equipment.json, kb/branchpoints, latest_digest.sh, quiet-browse, 깡통가, 완성품가

## User preferences

- when Woojin asks about 챌섭 장비/주문서/보스컷/시세/커뮤 여론 -> 오래 헤매지 말고 current character snapshot, 로컬 KB, 최소 커뮤니티 근거를 병렬로 묶어 빠르게 결론까지 가져갑니다. [Task 1] [ad-hoc note]
- when community evidence is needed for 아카/디시 style sources -> raw fetch/curl로 길게 긁지 말고 `quiet-browse open` -> `sleep 2~3` -> `quiet-browse text` 순서로 검색 목록 1개와 핵심 글 1~3개만 읽습니다. [Task 1] [ad-hoc note]
- when giving MapleStory market advice -> 답변은 결론 먼저 `사라/기다려라/조건부`, 숫자 매수선, 근거 2~3줄 구조로 압축합니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- 먼저 `character/<캐릭>/item-equipment.json`과 관련 `kb/branchpoints/`로 현재 상태를 고정하고, 동시에 `./scripts/latest_digest.sh`와 대상 키워드 `rg`를 `kb/latest-digest.md`, `kb/branchpoints`, `kb/yt`에 돌리는 순서가 빠르다. [Task 1] [ad-hoc note]
- 제목 여론만 보면 오판하기 쉽다. 최소한 `뉴비`, `저메소`, `시즌용 교불 매몰`, `완제품 구매 가능`, `직업별 매물가`, `보스컷`, `후반 수요` 전제를 분리해서 읽는다. [Task 1] [ad-hoc note]
- 교불/카르마/시즌 전용 장비는 회수 가능 장비처럼 설명하면 안 된다. 거래 가능/회수 가능 여부를 먼저 명시한 뒤 가격/효율 판단으로 넘어간다. [Task 1] [ad-hoc note]
- `깡통가`와 `완성품가`는 분리해서 본다. 깡통가에는 강화, 잠재, 에디, 재설정 비용을 붙여 실제 매수선과 비교한다. [Task 1] [ad-hoc note]
- Related skill: `skills/maple-challenger-research/SKILL.md` [Task 1]

## Failures and how to do differently

- 증상: 챌섭 시세/커뮤 질문인데 자료 탐색이 길어지고 답이 늦어진다. 원인: 캐릭터 상태와 로컬 KB를 먼저 고정하지 않고 커뮤니티부터 헤맸다. 수정: `item-equipment.json` + `kb/branchpoints` + `latest_digest.sh`/`rg`를 먼저 병렬로 돌린다. [Task 1] [ad-hoc note]
- 증상: 제목 여론만 보고 추천이 흔들리거나 사용자 상황과 안 맞는다. 원인: 뉴비/저메소/교불 매몰/완제품 가능성 같은 전제를 분리하지 않았다. 수정: 질문마다 전제를 먼저 분리하고 맞는 줄기만 남긴다. [Task 1] [ad-hoc note]
- 증상: 깡통가가 싸 보인다는 이유로 잘못된 추천이 나온다. 원인: 강화/잠재/에디/재설정 비용을 빠뜨리고 완성품가와 같은 층위로 비교했다. 수정: `깡통가 + 추가 비용`과 완성품가를 분리해 실제 매수선을 계산한다. [Task 1] [ad-hoc note]

# Task Group: MapleStory Maplescouter API tooling and 레공레 boss-ratio refresh
scope: MapleStory `레공레` 같은 캐릭터의 환산/boss stat을 다시 재야 하는데 browser surface가 불안정하거나 noisy할 때, UI scraping 대신 direct Maplescouter API route와 measured anchor를 빠르게 재사용할 때 쓴다.
applies_to: cwd=/Users/wooojin; reuse_rule=같은 MapleStory Maplescouter 조회/보스 추정 workflow에는 재사용 가능하지만, API values와 boss ratio 결론은 캐릭터 상태와 측정 시점 의존적이므로 조회 전에 갱신 여부를 먼저 확인해야 한다.

## Task 1: Record direct Maplescouter API route and 2026-07-08 레공레 anchor, success

### rollout_summary_files

- extensions/ad_hoc/notes/2026-07-08T20-43-09+0900-maplescouter-api-tooling.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-07-08T20:43:09+09:00, thread_id=none, authoritative note for bypassing browser friction with direct Maplescouter API access and refreshing `레공레` estimates) [ad-hoc note]

### keywords

- MapleStory, Maplescouter, 레공레, 레테, 심연의 결계의 핵, Browser is not available: extension, api.maplescouter.com, /api/id, api-key, boss300_stat, boss380_stat, exchangePower, hexaUsed, Black Mage estimate

## User preferences

- when MapleStory consulting hits browser friction and the approved browser surface still fails with `Browser is not available: extension` -> visual scraping을 계속 밀기보다 direct data route를 먼저 찾아 같은 search path를 반복하지 않게 합니다. [Task 1] [ad-hoc note]
- when the user has already asked to remember character benchmarks for later boss comparison -> fresh measurement anchors도 baseline처럼 남겨 이후 ratio refresh에 바로 재사용합니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- browser/extension path가 unavailable하거나 noisy하면 `https://maplescouter.com/ko/result?name=<character>&preset=00000`의 Next.js chunk를 열어 API base와 request shape를 먼저 확인한다. 이 note 기준 durable route는 `https://api.maplescouter.com/api/id?name=<character>&preset=00000`였다. [Task 1] [ad-hoc note]
- direct request에서 필요한 header는 `api-key`, `Content-Type: application/json`였고, useful JSON paths는 `.calculatedData.boss300_stat`, `.boss380_stat`, `.boss300_hexaStat`, `.boss380_hexaStat`, `.exchangePower`, `.exchangePowerHexa`, `.hexaUsed`였다. [Task 1] [ad-hoc note]
- 2026-07-08 measured anchor는 character `레공레`, Lv280 `레테`, Challenger World 2 기준으로 `boss300_stat 39347`, `boss380_stat 38899`, `boss300_hexaStat 31624`, `boss380_hexaStat 31264`, `exchangePower 63243589.15541312`, `exchangePowerHexa 38886323.44397476`, `hexaUsed [64,1428]`였다. [Task 1] [ad-hoc note]
- `레공레`는 Nexon API/in-game combat power보다 Maplescouter 환산/헥환/boss stat을 SSOT로 우선하는 편이 맞다. prior note의 Lete/정축여축-style combat-power distortion 때문에 same-boss refresh는 comparable measurement condition일 때만 `updated boss ratio ~= previous ratio * (1 + final damage/stat gain)` 식으로 잇는다. [Task 1] [ad-hoc note]
- 2026-07-08 practical conclusion은 old Black Mage estimate `89.97%` -> after HEXA stat `~97.2%` -> after legendary abyss core and follow-up measured growth `~99-103%`, center around `~101%`였다. workspace 기록은 `/Users/wooojin/dev/maple/kb/branchpoints/2026-07-08-legongre-abyss-core-legend.md`와 `/Users/wooojin/dev/maple/kb/prediction-log.md`에 남겼다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: browser가 승인됐는데도 `Browser is not available: extension` 때문에 측정 흐름이 막힌다. 원인: UI/browser surface availability를 SSOT data path보다 우선시했다. 수정: browser surface가 불안정하면 Maplescouter page chunk -> API endpoint 확인 -> direct JSON fetch 순서로 바로 피벗한다. [Task 1] [ad-hoc note]
- 증상: in-app/browser rendering noise 때문에 visual inspection에 시간을 너무 많이 쓴다. 원인: measured values를 DOM/화면에서 읽으려 했다. 수정: boss stat/환산 확인은 direct API response를 기준으로 보고, UI는 supplementary check로만 둔다. [Task 1] [ad-hoc note]

# Task Group: MapleStory equipment efficiency calculation mode
scope: MapleStory 장비 업그레이드 효율이나 meso-per-efficiency 계산을 요청받았을 때 exact mode와 rough mode를 나눠 빠르게 재사용할 때 쓴다. 캐릭터 current snapshot, API delta, screenshot tooltip을 근거로 계산하는 MapleStory 상담용 메모다.
applies_to: cwd=/Users/wooojin; reuse_rule=같은 MapleStory 장비 상담/효율 계산 workflow에는 재사용 가능하지만, 캐릭터 스냅샷과 최근 ratio는 시점 의존적이므로 계산 전에 갱신 여부를 먼저 확인해야 한다.

## Task 1: Record MapleStory precise-vs-rough efficiency calculation mode, success

### rollout_summary_files

- extensions/ad_hoc/notes/20260705-185949-maple-efficiency-calc-mode.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-07-05T18:59:49+09:00, thread_id=none, authoritative note for exact meso-per-efficiency calculation workflow) [ad-hoc note]

### keywords

- MapleStory, efficiency calculation, meso-per-efficiency, precise mode, rough mode, API delta, screenshot tooltip, Maplescouter, spec-efficiency coefficients, cost per 100m, cost per 1b

## User preferences

- when Woojin asks for `exact meso-per-efficiency calculations` in MapleStory gear consulting -> 계산을 대충 ratio 하나로 끝내지 말고 current snapshot, API before/after delta, screenshot tooltip 증가치를 근거로 분해 계산합니다. [Task 1] [ad-hoc note]
- when Woojin explicitly asks for a `fast` or `rough` answer -> full decomposition 대신 최근 ratio를 재사용해 빠르게 buy/skip/order recommendation부터 주고, rough estimate임을 먼저 밝힙니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- precise mode에서는 current character snapshot을 refresh/use하고, changed stats는 API before/after delta와 user screenshot을 concrete evidence로 둔다. [Task 1] [ad-hoc note]
- upgrade는 가능하면 `attack/magic attack`, `boss damage`, `main stat`, `all stat %`, `potential`, `starforce`, `set effect`, `symbol effect` 같은 stat component로 나눠 본다. [Task 1] [ad-hoc note]
- 각 component는 character의 current `Maplescouter/spec-efficiency coefficients`가 있으면 main-stat-equivalent로 변환하고, 결과는 total combat power increase, approximate damage/final-damage increase, total cost, efficiency per `100m`/`1b` mesos까지 함께 보고한다. [Task 1] [ad-hoc note]
- Maplescouter 내부 식을 직접 알 수 없을 때는 decomposition만 approximate로 낮추고, API delta와 screenshot tooltip increase는 hard evidence로 취급한다. [Task 1] [ad-hoc note]
- rough mode에서는 full decomposition을 생략하고, 해당 캐릭터의 most recent calculation ratio, prior combat power/damage ratio, screenshot tooltip increase, known recent upgrade efficiency를 재사용해 빠르게 추정한다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: exact efficiency 질문인데 단순 비율 답변만 줘서 사용자가 원하는 meso-per-efficiency 근거가 약해진다. 원인: current snapshot/API delta/screenshot evidence를 수집하지 않고 rough mode로 답했다. 수정: exact 요청이면 먼저 precise mode로 전환하고 stat component 분해와 cost per `100m`/`1b`까지 같이 낸다. [Task 1] [ad-hoc note]
- 증상: rough answer인데 과도하게 분해 계산하느라 답이 느려진다. 원인: fast/rough cue를 놓치고 precise mode 절차를 그대로 탔다. 수정: rough 요청이면 최근 ratio 재사용, rough label, recommendation-first를 기본값으로 둔다. [Task 1] [ad-hoc note]

# Task Group: MapleStory 레공레 레테 benchmark and boss-practice correction
scope: MapleStory 보스 추천이나 현재 스펙 맥락을 판단할 때 `레공레` `레테` 캐릭터의 2026-06-26 baseline과 practice clear 시간을 빠르게 재사용할 때 쓴다. 이 캐릭터 전용 기준이며, 챌린저/버프 상태와 post-clear timer 해석을 함께 봐야 한다.
applies_to: cwd=/Users/wooojin; reuse_rule=같은 캐릭터 `레공레` `레테`의 보스 비교/추천에는 재사용 가능하지만, 레벨·챌린저 버프·장비가 바뀌면 baseline을 다시 갱신해야 한다.

## Task 1: Record 2026-06-26 MapleStory 레공레 레테 spec/context baseline, success

### rollout_summary_files

- extensions/ad_hoc/notes/2026-06-26-maple-legongre-lete-benchmark.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-06-26T00:00:00+09:00, thread_id=none, user explicitly asked to remember this as the 2026-06-26 baseline) [ad-hoc note]

### keywords

- MapleStory, 레공레, 레테, Lv276, Challenger World, EMERALD 30000, Item Burning Plus, 카오스 더스크, 하드 윌, actual-control benchmark

## Task 2: Correct Chaos Gloom clear-time interpretation for the 2026-06-26 레공레 benchmark, success

### rollout_summary_files

- extensions/ad_hoc/notes/2026-06-26-maple-legongre-cgloom-time-correction.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-06-26T00:00:00+09:00, thread_id=none, correction note that supersedes the earlier Chaos Gloom time read) [ad-hoc note]
- extensions/ad_hoc/notes/2026-06-26-maple-legongre-lete-benchmark.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-06-26T00:00:00+09:00, thread_id=none, original benchmark note containing the superseded `15:02` interpretation) [ad-hoc note]

### keywords

- Chaos Gloom, 카오스 더스크, 4:58, post-clear timer, exit timer, top-right buff, 40-minute potion, 30-minute buff, 5-6 minutes, correction

## User preferences

- when the user explicitly said to remember this as the `2026-06-26 레테 spec/context baseline` -> MapleStory character benchmark/screenshot context는 이후 보스 추천 비교에 바로 재사용할 수 있게 baseline 형태로 남깁니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- 캐릭터 baseline은 `레공레`, class `레테`, live level `276`였고, screenshot EXP state는 `Lv276 4,772,676,843,063 (38.136%)`였다. [Task 1] [ad-hoc note]
- Challenger World state는 `EMERALD 30000`, challenger coins `19250`, upper challenger coins `0`였다. Challenger pass는 `Lv.10`, weekly points `500/500`, EXP support line purchased/claimed through current visible tier였고 applied effects는 normal monster damage `+200%`, additional EXP `+20%`였다. [Task 1] [ad-hoc note]
- Emerald challenger buff snapshot은 `EXP 1.5x`, `attack/magic +80`, `normal monster damage +150%`, `boss damage +70%`, `ignore defense +70%`, `buff duration +60%`, `crit rate +30%`, `crit damage +40%`, `stance 100%`, `all stat +100`, `max HP/MP +5000`, `summon duration +10%`, `cooldown reduction -5%`, `guild contribution 2x`, `rune spell duration +50%`였다. [Task 1] [ad-hoc note]
- Item Burning Plus state는 stage 7 진행 중, `276/270`, hard Damien solo `1/1`, challenger emblem `2650/3000`, weekly hunting mission `10000/10000`였다. [Task 1] [ad-hoc note]
- actual-control benchmark로는 Hard Will practice가 가장 직접적이다. screenshot은 boss HP `0.1%`, remaining time `1:48`, death count remaining around `9`였고 actual clear는 approximately `18:13-18:20`로 본다. 가이드 없이 깬 기준이라 clearable but slower/learning-heavy anchor로 쓸 수 있다. [Task 1] [ad-hoc note]
- Chaos Gloom practice clear는 initial note의 `15:02`가 아니라 correction note 기준으로 `about 5-6 minutes`가 맞다. center `4:58`은 boss remaining timer가 아니라 kill 뒤 뜨는 post-clear 5-minute exit/cleanup timer이고, top-right buff/potion area의 `40-minute buff at 34 remaining`과 `30-minute buff at 24 remaining`이 실제 elapsed cue다. [Task 1][Task 2] [ad-hoc note]
- future boss recommendation에서는 Chaos Gloom은 already within practical expectation, Hard Will은 clearable but slower/learning-heavy로 본다. next practical comparisons는 `Hard Darknell`, `Chaos Guardian Angel Slime`, `Hard Lucid`, `Hard Verus Hilla`였다. [Task 1][Task 2] [ad-hoc note]

## Failures and how to do differently

- 증상: Chaos Gloom screenshot의 center `4:58`을 boss remaining timer로 읽어 clear time을 `15:02`로 과대추정했다. 원인: 새 post-clear 5-minute exit/cleanup timer를 전투 timer로 오인했다. 수정: clear 직후 스샷은 top-right buff/potion timer를 먼저 보고, center countdown이 post-clear UI인지 확인한다. [Task 2] [ad-hoc note]
- 증상: correction이 나온 뒤에도 earlier benchmark note의 수치를 그대로 재사용할 수 있다. 원인: baseline note와 correction note를 분리 저장했지만 superseded status를 메모에 명시하지 않으면 검색 시 오래된 숫자가 먼저 잡힌다. 수정: Chaos Gloom benchmark는 `about 5-6 minutes`로 overwrite하고, `15:02`는 superseded interpretation으로만 남긴다. [Task 1][Task 2] [ad-hoc note]

# Task Group: MapleStory boss benchmark and boss-ratio decision rules
scope: MapleStory 보스 비교나 다음 솔로 목표 판단에서 `오렌지솥밥` 캐릭터의 실제 클리어 앵커와 환산/Maplescouter 비율 기준을 빠르게 재사용할 때 쓴다. 이 캐릭터 전용 기준이며, 스샷 시간 충돌과 피로도까지 함께 반영해야 한다.
applies_to: cwd=/Users/wooojin; reuse_rule=같은 캐릭터 `오렌지솥밥`의 보스 비교/추천에는 재사용 가능하지만, 스펙 수치와 실제 가능 보스는 업그레이드 이후 다시 갱신해야 한다.

## Task 1: Record 2026-06-25 MapleStory boss benchmark for 오렌지솥밥, success

### rollout_summary_files

- extensions/ad_hoc/notes/2026-06-25-maple-orange-boss-benchmark.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-06-25T00:00:00+09:00, thread_id=none, user explicitly asked to remember future boss-comparison data) [ad-hoc note]

### keywords

- MapleStory, 오렌지솥밥, Maplescouter, 환산주스탯, Champion Black Mage, Normal Seren, Easy Kalos, Easy Adversary, boss ratio, conservative screenshot

## Reusable knowledge

- 캐릭터 baseline은 `오렌지솥밥, Luna, Ren, Lv.282`, latest Maplescouter snapshot after 2026-06-25 upgrades는 `combat power 70,409,457`, `boss300 46,180`, `boss380 45,796`, `arcane force 1350`, `authentic force 340`, `ascent_const 0.008657956840101733`였다. [Task 1] [ad-hoc note]
- 이 캐릭터 비교는 HP table보다 `환산주스탯/Maplescouter-style boss ratio first`가 우선이고, actual clear anchors는 Champion Black Mage clear와 Normal Seren clear다. [Task 1] [ad-hoc note]
- Champion Black Mage는 about `110.5%`, rough 20-minute model time `18.1m`였고, conservative screenshot anchor는 `0.6% HP at 1:48 remaining`이다. `0.1% HP at 4:53 remaining` 스샷도 있지만 file order/timer progression과 충돌해서 optimistic/phase-display evidence로만 둔다. [Task 1] [ad-hoc note]
- Normal Seren은 about `212.7%`, rough 20-minute model time `9.4m`였고 comfortably stable로 본다. Seren screenshots는 `0.9% HP at 8:55 remaining`과 clear/cutscene `4:58-4:56 remaining`이 함께 있어도 conservative 쪽은 lower remaining time 기준으로 본다. [Task 1] [ad-hoc note]
- Easy Kalos는 about `171.0%`라 damage는 충분하고 main variable은 mechanics/downtime이다. Easy Adversary는 about `119.8%`라 ratio만 보면 가능하지만 피로도와 unfamiliar patterns 때문에 same-day push 추천 대상은 아니다. [Task 1] [ad-hoc note]
- 현재 비현실 target은 `Normal Kalos 49.5%`, `Champion Kalos 34.3%`, `Normal Adversary 34.9%`, `Hard Seren 86.9%`, `Champion Seren 71.5%`였다. [Task 1] [ad-hoc note]
- future rule of thumb: around `110%`는 near-cut으로 last 1-2 minutes 예상, around `120%`는 some mistakes allowed, around `170%`는 damage sufficient so mechanics/fatigue decision, around `200%+`는 stable farm/comfortable clear 쪽이다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: 스크린샷 timer display가 서로 충돌해 clear benchmark가 과하게 낙관적으로 잡힐 수 있다. 원인: file order/timer progression이 맞지 않는 장면을 같은 무게로 썼다. 수정: `Prefer conservative screenshot time if timer displays conflict`를 기본값으로 둔다. [Task 1] [ad-hoc note]
- 증상: Kalos/Adversary를 단순 HP 또는 비율만으로 추천하고 싶어진다. 원인: mechanics/downtime와 fatigue 변수를 과소평가했다. 수정: Kalos/Adversary는 pattern burden을 별도 가중하고, 사용자가 tired하다고 하면 new mechanic-heavy boss push는 추천하지 않는다. [Task 1] [ad-hoc note]

# Task Group: Maplog manual representative-only cover selection
scope: `/Users/wooojin/App/maplog`에서 Gathering cover를 한 장의 수동 대표사진과 자동 rear/layer selection으로 유지하고, 이전 full-cover-order 상태를 안전하게 이행할 때 쓴다.
applies_to: cwd=/Users/wooojin/App/maplog; reuse_rule=동일한 cover-selection contract와 migration에 재사용한다. UI gesture/geometry의 구체 구현은 현재 code와 별도 검증이 필요하다.

## Task 1: Keep Maplog cover selection manual for one representative only, user-confirmed

### rollout_summary_files

- extensions/ad_hoc/notes/2026-07-12-maplog-manual-representative-only.md (cwd=/Users/wooojin/App/maplog, rollout_path=none, updated_at=2026-07-21T12:45:20Z (source-file git timestamp), thread_id=none, user-confirmed decision that supersedes a user-selected full cover order) [ad-hoc note]

### keywords

- Maplog, manual representative-only, Gathering, 1/2/3-photo map-pin tiers, rear layers, 다른 사진으로 할래요, hand fan, lifted card, deterministic, re-entry, relaunch, legacy cover order, migration

## User preferences

- when choosing a Gathering cover -> 사용자는 대표 사진 한 장만 직접 고르고, 1/2/3-photo map-pin tier의 rear/layer 사진은 Maplog가 자동으로 고르길 확정했습니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- `다른 사진으로 할래요`에 들어가면 기존 automatic preview card는 selected/lifted/slot state 없이 hand fan으로 돌아간다. 탭하거나 scrub-commit한 한 카드만 manual representative로 lifted되고, 다른 카드를 고르면 이전 representative는 fan으로 돌아간다. [Task 1] [ad-hoc note]
- automatic rear choice는 uncurated하게 보이되 같은 input에서 deterministic하고 re-entry/relaunch에도 안정적이어야 한다. photo add/delete 뒤에는 recompute하되 유효한 manual representative는 유지한다. legacy full cover order는 superseded됐으므로 migration은 첫 legacy user cover만 manual representative로 해석하고 rear layer를 자동 재생성한다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: rear/layer photo까지 user-editable slot으로 노출하거나 full cover order를 보존한다. 원인: superseded된 cover-selection contract를 계속 적용했다. 수정: manual state는 representative 한 장만 보관하고 rear layer는 deterministic automatic selection으로 재생성하며, legacy migration은 첫 cover만 대표로 읽는다. [Task 1] [ad-hoc note]

# Task Group: Maplog live-map QA native-quality escalation
scope: Maplog live map QA처럼 지도/실시간 UI에서 체감 품질이 부족할 때, 현재 구현 계층 튜닝을 계속할지 native/정석 계층으로 피벗할지 판단하는 작업에 쓴다. 성능 수치 자체보다 marker sync 같은 핵심 품질 기준 충족 여부를 본다.
applies_to: cwd=/Users/wooojin/Documents/Codex/2026-06-07/maplog-side-qa; reuse_rule=Maplog 계열 QA와 지도/캔버스/미디어/실시간 UI 품질 판단에는 재사용 가능하지만, 실제 SDK 선택과 구현 범위는 현재 프로젝트 구조를 다시 확인해야 한다.

## Task 1: Prefer native overlay over tuned SwiftUI compromise for live map marker sync, success

### rollout_summary_files

- extensions/ad_hoc/notes/20260607-215956-maplog-native-quality-principle.md (cwd=/Users/wooojin/Documents/Codex/2026-06-07/maplog-side-qa, rollout_path=none, updated_at=2026-06-07T21:59:56+09:00, thread_id=none, authoritative extension note on native-quality pivot) [ad-hoc note]

### keywords

- Maplog, live map QA, SwiftUI overlay, 60fps, marker 위치 동기화, NMFMarker, native overlay, 네이버 지도 앱, scenario expected actual verdict evidence follow-up

## User preferences

- when app quality still felt wrong after tuning, the note preserved: `조금 나아진 타협안`보다 `사용자가 요구한 핵심 품질을 만족하는 정석 구현` -> 체감 품질이 큰 UI는 미세튜닝 성과보다 품질 ceiling을 먼저 봅니다. [Task 1] [ad-hoc note]
- when native marker sync finally matched the desired feel and the user reacted `이거야` -> 품질 기준이 명확히 드러난 순간에는 `충분히 괜찮음`에서 멈추지 않고 first-party/native 구현 가능성을 먼저 검토합니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- SwiftUI overlay 라벨을 `60fps`까지 올려도 marker 위치 동기화가 어긋나면 성능 문제가 아니라 계층 적합성 문제일 수 있다. 이 경우 Naver SDK `NMFMarker` 같은 native overlay가 정석 해법이 될 수 있다. [Task 1] [ad-hoc note]
- 비슷한 QA에서는 `현재 구현 계층에서 구조적으로 가능한가`, `native SDK / first-party API / proven engine이 더 맞는가`, `튜닝 전에 계층 전환이 정석인가`를 먼저 묻는 편이 시행착오를 줄인다. [Task 1] [ad-hoc note]
- QA 메모를 `scenario / expected / actual / verdict / evidence / follow-up` 순서로 남기면 품질 판단과 피벗 근거가 선명해진다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: `60fps` 튜닝 뒤에도 사용자는 품질 부족으로 느꼈다. 원인: 프레임레이트 개선과 marker 위치 동기화 정확도는 다른 문제였고, 현재 계층이 요구 품질을 구조적으로 못 맞췄다. 수정: 추가 튜닝 전에 native overlay 전환 가능성부터 평가한다. [Task 1] [ad-hoc note]
