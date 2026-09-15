v1

## User Profile

우진님은 Maplog, MapleStory 도구, OpenAI Game, 제품/해커톤, 진로·공모전을 반복적으로 다룬다. 실제 파일·live state·정확한 오류·원문과 검증 증거를 근거로 결론 내리기를 선호한다. 반복되는 로컬 경고·도구 장애도 단순 회피보다 실제 실행 경로와 유효 설정을 고쳐 새 실행으로 확인한다. 리서치에서는 Sol이 최종 비교를 맡고, 에이전트가 범위가 큰 공개/로그인 브라우저 작업과 정확한 클릭을 끝낸 뒤 compact report만 올리기를 원한다. Maplog에서는 private-first 사진 경험, native interaction, 명확한 provenance, 그리고 한 장만 수동으로 고르는 cover contract를 중시한다. 문서 정비·방향 탐색과 제품 UX 구현의 승인은 분리한다. OpenAI Game은 현재 단계·한 가설·문서 근거·실제 플레이를 갖춘 경우에만 구현한다. 공중 월드 비교 lab은 구현·브라우저 검증됐지만 사용자 체험과 최종 월드 선택은 아직 미완료다. 열린 대회는 재현 가능한 proof spine과 제품 서사를 함께 만든다. [ad-hoc note]

## User preferences

- Shared dirty checkout에서는 “commit/reset/clean/revert하거나 다른 작업을 정리하지 마세요”: `git status --short`부터 보고 unrelated changes를 보존한다.
- 리서치에서는 “Sol이 작업 및 비교, 에이전트로 Grok이 … Aside 브라우저에서 탐색”, “정확한 클릭같은 것도 알아서 에이전트가 끝내게”: Sol은 compact report로 최종 판단하고, 넓은 로그인/브라우저의 reversible 작업은 에이전트에 맡긴다. 구매·제출·메시지·삭제·계정/보안 변경은 승인 전 하지 않는다.
- 리서치 실행 구조는 “최대한 경량화”, “그록 실행기까지만”: 중복 스킬·공용 라이브러리·자동 체이닝을 늘리지 않고 router + runners를 유지한다. 로컬 근거가 충분하면 외부 리서치를 생략한다.
- 키보드 설정이 최근 변경 뒤 깨지면 “며칠 전으로 돌릴 수 없나?”를 우선한다: 새 매핑을 덧붙이기 전 정상 자동 백업으로 되돌리고, 실제 기기에서 한영·`⌘⇧3`·Rectangle을 확인한다.
- OpenAI Game 구현·위임 전 `현재 단계 / 판정할 가설 하나 / 근거 문서와 절`을 제시한다. `REFERENCE`·`DRAFT`는 구현 허가가 아니며, 현재 음향 비교 중인 맵 재설계 메모도 승인 아니다. [ad-hoc note]
- OpenAI Game의 새 세션은 대표 문서만 읽게 하되 초기 큰 계획은 지우지 않는다. `START_HERE.md`는 최소 입구, `CLAUDE.md`는 `AGENTS.md` 포인터로 둔다.
- 독립 분석은 “공통 입력 패킷만 지정 순서”, 다른 세션 결과는 “찾거나 읽거나 언급하지 마세요”, 지정된 단일 산출물만 편집한다. 미검증 물리는 `[예상]`으로 남긴다.
- 승인된 OpenAI Game 구현이 “`experiments/aerial-world-lab/**` 뿐”처럼 쓰기 범위를 고정하면 baseline·docs·commit·cleanup으로 넓히지 않는다. 실제 브라우저 상호작용을 하고 changed files / checks / browser-confirmed / unverified를 분리해 보고한다.
- 범위 제한된 창작 설계에서는 “안전한 평균안 대신 하나의 응집된 월드 비전에 베팅하세요”: 구조 유형 메뉴 대신 단일 비전·트레이드오프·폐기 기준을 제시하고, 지정 산출물 하나와 짧은 경로 보고만 남긴다.
- Maple 도구 개선은 실제 CLI를 먼저 써 보고 관찰된 마찰만 최소 수정한다. 오늘 갱신한 character snapshot은 약 14일 재사용 가능하되 매물·이벤트·주간 진행은 별도 최신 확인한다.
- Maple EXP/구매 상담은 사용자의 `1소재=30분` 같은 단위와 실제 스크린샷을 우선하고, 결론·구매 상한부터 짧게 제시한다.
- Maplog에서 “읽어만 봐. 아직 작업 아니야” 같은 읽기·문서 정비·방향 탐색은 구현 승인이 아니다. 구현 전 대상·범위·완료 조건을 확인하고, 감상·선택 UX는 스크롤/스와이프 등 대안을 먼저 비교한다.
- Maple 챌린저스 보상은 “모든 보상들”, “이벤트별 코인샵별” 요청이면 직접 수령/인벤 리프/리프 불가 표부터 낸다. 보스 배율은 “스펙상 가능”과 첫 클리어 체감 난이도를 분리해 설명한다.
- 채용 조사에서는 “지원 버튼은 절대 누르지 마”, 자격은 “원문 근거로만 판정”: 읽기·검증만 하고 공식 공고와 로컬 학업 근거를 분리한다.
- 넓은 채용 조사는 후보를 모은 뒤 `현재 열림 / 마감 / 시즌 추정`으로 구분한다. 공모전은 개인 참가 우선, 필요하면 2인 대안을 함께 본다.
- 컨텍스트 이전 문서에는 1·2인칭 대신 ‘사용자’를 쓰고, 저장된 메모리 규칙만 쓰며, 선호 문구는 가능한 원문을 보존한다.
- 반복되는 데스크톱 경고는 창을 닫는 데서 멈추지 말고 실제 실행 파일·보안 상태를 확인해 원인을 교체하고, 실제 재실행 결과와 재발 조건을 짧게 보고한다.
- 로컬 설정 분리도 “확인좀해줘”처럼 실제 검증을 기대한다: 명령만 제시하지 말고 새 세션의 유효 지침·`plugin list`·`doctor`까지 확인한다.

## General Tips

- 외부 근거가 필요하면 `research-browser-router`를 먼저 읽는다. Consult는 좁은 공개 판단, Grok+Aside는 로그인 포함 넓은 탐색/정확한 클릭; 성공 시 compact report만 읽고 raw logs는 실패·모순 때만 연다.
- Aside ChatGPT `contenteditable`은 click + `keyboard.insertText()`로 입력하고 fresh snapshot/detached-ref 재탐색을 쓴다. Grok Aside provider는 `xai-grok-oauth`, model은 `grok-4.6`이다.
- Karabiner 단축키가 함께 깨지면 현재 JSON을 안전 백업한 뒤 마지막 정상 backup을 복원한다. JSON/hash/profile/service 확인 후 실제 키 테스트를 요청하며, macOS symbolic hotkey를 먼저 건드리지 않는다.
- Maplog은 새 세션에서 `record/CURRENT.md` → `record/PRODUCT.md` → `record/README.md`를 먼저 읽고, 과거 `record/v2/*`, plans, branchpoint, ops는 근거로만 본다. build와 테스트 보관함 조작은 기술 연결 증거이지 실사진 감상 품질 증거가 아니다.
- OpenAI Game canonical gate는 `/Users/wooojin/App/openaigame/docs/14-execution-gates.md`; 현재 최소 경로는 `START_HERE.md` → `AGENTS.md` → `DECISIONS.md` → `docs/14` §0·§4 → `docs/28`이다.
- OpenAI Game Fable은 independent input일 뿐: phase transition/새 시스템/`REFERENCE`·`DRAFT` 구현 전환에서 medium plan mode로만 쓰고, 실제 플레이·문서 대조와 범위 승인 후 별도 구현으로 넘긴다. [ad-hoc note]
- OpenAI Game aerial comparison lab은 `WORLD_PRESETS[*].forms`를 visual/collision SSOT로 유지한다. CDP는 fresh target + cache-busting 후 `typeof window.game.getPreset === 'function'`을 먼저 확인하고, static pass만으로 사용자 비교/최종 선택을 완료 처리하지 않는다.
- Git 메타데이터가 없는 작업 폴더에서는 `git diff` 대신 대상 파일 hash·mtime·필수 섹션/링크 검사로 변경 범위와 문서 작업을 검증한다.
- Maplog pre-design work는 최소 정보 구조와 native interaction을 먼저 안정시키고, loading/empty/error·복구·접근성·개인정보 경계를 생략하지 않는다. [ad-hoc note]
- 대회는 `한 줄 → 한 사용자 경로 → 한 코드 경로 → 한 검증 명령 → 한 제출 주장`을 먼저 잇고, final PASS는 exact ZIP을 fresh directory에서 재검증한 결과로만 말한다. [ad-hoc note]
- 시간·공고·가격·소셜 지표는 live/time-specific이다. 대규모 조사는 `현재 열린 것만 10개`처럼 범위와 종료 조건을 먼저 자른다.
- Aside에서 `rg` 보안 팝업이 재발하면 `/Users/wooojin/.aside/runtime/native/bin/rg`와 `/opt/homebrew/bin/rg` 링크를 먼저 확인한다. `/usr/sbin/spctl`을 쓰며 xattr 제거만으로 해결됐다고 보지 않는다.
- Codex/Rubato 분리는 `CODEX_HOME`만 바꾸지 말고 cwd도 통제한다. 먼저 `/tmp`에서 `CODEX_HOME="$HOME/App/codex-plain-home" /opt/homebrew/bin/codex`, `codex plugin list`, `codex doctor --json`으로 Rubato path/plugin, provider, MCP 수를 확인한다. 대상 프로젝트에서는 `.codex`를 별도 점검한다.

## What's in Memory

### /Users/wooojin

#### 2026-09-12

- 일반 Codex와 Rubato Codex 분리 실행: CODEX_HOME, /tmp, codex plugin list, codex doctor --json, project .codex, model_instructions_file, No Rubato paths found
  - desc: Rubato가 결합된 기본 Codex에서 순정 Codex를 중립 cwd로 분리·진단한 로컬 설정 사례; cwd=/Users/wooojin.
  - learnings: `CODEX_HOME`만으로는 `/Users/wooojin`의 프로젝트 `.codex` 재주입을 막지 못한다. 새 세션의 유효 지침·플러그인·provider·MCP까지 확인한다.

#### 2026-08-21

- Karabiner Varmilo shortcut rollback: Karabiner, Varmilo, Rectangle, 한영, ⌘⇧3, automatic_backups, keyboard_fn
  - desc: recent Varmilo mappings broke several macOS shortcuts; safe backup rollback, minimal-rule recovery, and real-device validation; cwd=/Users/wooojin.
  - learnings: preserve current `karabiner.json`, restore the closest known-good backup, then verify hash/JSON/profile/service and 한영·capture·Rectangle; EventViewer before any new device rule.

### /Users/wooojin/App/maplog

#### 2026-09-10

- Document reset and Place·Visit approval boundary: record/PRODUCT.md, record/CURRENT.md, Place-first, Visit, Journey, scope-creep, scroll, swipe album
  - desc: 최신 Maplog 입구·제품 정의와 Place·Visit browse가 구현 승인으로 과잉 해석된 사례; cwd=/Users/wooojin/App/maplog.
  - learnings: 문서 정비 → 방향 탐색 → 최소 기술 연결 → 제품 UX 구현을 별도 승인으로 두고, 테스트 보관함 동작을 제품 경험 PASS로 부르지 않는다.

### /Users/wooojin/dev/maple

#### 2026-09-10

- 챌린저스 시즌4 보상 반입과 이지 벨로나: 200레벨 달성의 비약, 월드 리프, 메멘토 큐브, 레공레, Maplescouter, 130.8%, 핀볼
  - desc: 보상/코인샵을 반입 상태로 분류하는 조사와 레공레 이지 벨로나의 스펙·패턴 병목 판단; cwd=/Users/wooojin/dev/maple.
  - learnings: 전체 이벤트별 분류표는 아직 미완결이고, 130.8%는 딜 부족이 아니라 패턴 숙련을 더 봐야 한다는 뜻이다.

### /Users/wooojin/App/openaigame

#### 2026-08-21

- A-world structure proposal: docs/29-aerial-world-structure-exploration-brief.md, aerial-world-sol-medium, speed-wing, glide-wing, open-air, “창가로 항해하는 미완성 하늘배”, collision-outline
  - desc: 지정 문서 하나에 A안의 단일 공중 월드 비전과 열린 공중·두 날개 경로 분기·폐기 기준을 작성한 설계 작업; cwd=/Users/wooojin/App/openaigame.
  - learnings: 큰 형태 사이를 통과하게 하고, 양 날개가 같은 선을 택하거나 glider가 비용 없는 안전선이 되면 폐기한다. 이는 구현 승인이나 최종 승자 판정이 아니다.
- Isolated aerial-world comparison lab: experiments/aerial-world-lab, WORLD_PRESETS, world-presets.js, aerial-world-lab-flight-telemetry-v1, inspectX, V, R, J, F1
  - desc: docs/31 승인 브리프의 A/B/C preset lab 구현과 current-code/browser verification; cwd=/Users/wooojin/App/openaigame.
  - learnings: `WORLD_PRESETS[*].forms` is visual/collision SSOT; 67 `P` parameters matched baseline and browser keys/console were checked. docs/31 changed externally during work; first-impression flights, same-input telemetry replay, and final selection remain unverified.

### Older Memory Topics

#### /Users/wooojin

- Aside `rg` macOS security warning: Aside, rg, ripgrep, com.apple.quarantine, /usr/sbin/spctl, CoreServicesUIAgent, /opt/homebrew/bin/rg
  - desc: quarantined Aside-bundled ripgrep의 반복 보안 경고를 실제 실행 경로 교체로 해결한 로컬 macOS troubleshooting; cwd=/Users/wooojin.
- Consult/Grok+Aside research routing: research-browser-router, run_aside_consult.py, run_grok_research.py, xai-grok-oauth, grok-4.6, grok-report.md
  - desc: implicit lightweight router, Aside ChatGPT Consult, and native Grok execution for public and logged-in browser research; cwd=/Users/wooojin, secondary=/Users/wooojin/dev/maple.

#### /Users/wooojin/App/maplog

- Manual representative cover and native-quality escalation: manual representative-only, rear layers, deterministic, legacy cover order, NMFMarker, scenario expected actual verdict evidence
  - desc: one manual Gathering representative with deterministic automatic rear layers, plus when to pivot a live map from a tuned overlay to native marker rendering; cwd=/Users/wooojin/App/maplog. [ad-hoc note]
- Design-stage boundaries and native pivot: Fable, Terra, scenario expected actual verdict evidence
  - desc: structure-first scope control, model routing, and native pivot; cwd=/Users/wooojin/App/maplog.
- KB AI Challenge final ZIP and Claude skill port: keepitmello/KB-hackaton, KB이음케어_우브라더스_제출_최종.zip, framing, reframing, CLAUDE.md
  - desc: exact private-repository archive lookup and Claude-native skill port; cwd=/Users/wooojin/App/maplog.

#### /Users/wooojin/dev/maple

- Real-use tooling and 레공레 EXP planning: fetch_character.sh, latest_digest.sh, ECONNREFUSED 127.0.0.1:9223, package_share.sh, 1소재=30분, 모멘텀 패스, 메카베리
  - desc: actual CLI-first minimal fixes, honest partial-reconnaissance status, and user-unit/time/meso value calculation; cwd=/Users/wooojin/dev/maple.
- HEXA, research, API, efficiency, and boss workflows: hexaOrder, V core, VI tooltip, Maplescouter, item-equipment.json, boss ratio
  - desc: personalized HEXA delta decisions, challenger research, efficiency calculation, and boss benchmarks; cwd=/Users/wooojin/dev/maple, with live snapshot checks. [ad-hoc note]
- YouTube research playback safety: transcript, subtitles, timestamp, --mute-audio, isolated browser profile
  - desc: transcript-first muted inspection for Maple videos; cwd=/Users/wooojin/dev/maple. [ad-hoc note]

#### /Users/wooojin/App/openaigame

- OpenAI Game document routing and scene-comparison boundary: START_HERE.md, AGENTS.md, DECISIONS.md, docs/14, docs/28, HANDOFF.md, A안, B안, IN PROGRESS
  - desc: canonical entrypoint, archived-library boundary, A/B scene-comparison SSOT, and non-authorization for map implementation; cwd=/Users/wooojin/App/openaigame.
- Dumbfire reference research: Dumbfire, Instagram, Steam 4944600, DcJ3LTtJ7rs, TAS, Workshop, adapter_eof, Grok High
  - desc: partial Instagram/Steam evidence and a physics-clip hook analysis; use for reference research, not feature copying; cwd=/Users/wooojin/App/openaigame.
- OpenAI Game execution gates and later map-redesign input: REFERENCE, DRAFT, v4, anti-forcing, Fable medium, 맵 재설계
  - desc: brief gate, Fable/Telegram boundary, and authoritative later map-design input; cwd=/Users/wooojin/App/openaigame. [ad-hoc note]

#### /Users/wooojin

- Career eligibility, contests, and context transfer: 카카오뱅크, 재학생 인턴, 현재 열림, 마감, 시즌 추정, Smart IT, Hacking Festival, JAVA 경진대회, Codex 토큰
  - desc: official eligibility and current-opening research, contest format comparison, and supported user-context transfer; cwd=/Users/wooojin.
- 백석대 2026-2 수강계획 보류: 기독교세계관, 서현덕 월2, 김은득 수4, 기독교탐사, 월·수·목 등교
  - desc: confirmed courses and the two-person timetable dependency; cwd=/Users/wooojin. [ad-hoc note]
- Hackathon proof-spine workflow: Cofathon, KB AI Challenge, START_HERE.md, DECISIONS.md, CONTRACT.md, RELEASE.md, final ZIP
  - desc: contest worktree integration, claim-evidence chain, and fresh-archive verification; cwd=/Users/wooojin. [ad-hoc note]

#### /Users/wooojin/App/maplog

- Claude selective skill port: framing, reframing, CLAUDE.md, ~/.claude/skills, trigger-evals.json, skill discovery
  - desc: Claude Code에 맞춘 framing/reframing selective port와 fresh-session discovery 검증; cwd=/Users/wooojin/App/maplog.
