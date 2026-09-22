v1

## User Profile

우진님은 Maplog, MapleStory 도구, OpenAI Game, 제품/해커톤을 반복적으로 다룬다. 실제 파일·live state·정확한 오류·원문과 검증 증거를 근거로 결론 내리기를 선호한다. Maplog에서는 private-first 사진 경험, native interaction, 명확한 provenance, 한 장만 수동으로 고르는 cover contract를 중시한다. 문서 정비·방향 탐색과 제품 UX 구현의 승인은 분리한다. OpenAI Game은 현재 단계·한 가설·문서 근거·실제 플레이를 갖춘 경우에만 구현한다. 공중 월드 비교 lab은 구현·브라우저 검증됐지만 사용자 체험과 최종 월드 선택은 아직 미완료다. 열린 대회는 재현 가능한 proof spine과 제품 서사를 함께 만든다. [ad-hoc note]

## User preferences

- Shared dirty checkout에서는 “commit/reset/clean/revert하거나 다른 작업을 정리하지 마세요”: 먼저 `git status --short`를 보고 unrelated changes를 보존한다.
- 리서치는 “Sol이 작업 및 비교”, “정확한 클릭같은 것도 알아서 에이전트가 끝내게”: Sol은 compact report로 최종 판단하고, 넓은 로그인/브라우저의 reversible 작업은 에이전트에 맡긴다. 구매·제출·메시지·삭제·계정/보안 변경은 승인 전 하지 않는다.
- “최대한 경량화”, “그록 실행기까지만”: 중복 스킬·공용 라이브러리·자동 체이닝을 늘리지 않고 router + runners를 유지한다. 로컬 근거가 충분하면 외부 리서치를 생략한다.
- OpenAI Game 구현·위임 전 `현재 단계 / 판정할 가설 하나 / 근거 문서와 절`을 제시한다. `REFERENCE`·`DRAFT`와 음향 비교 중 맵 재설계 메모는 구현 허가가 아니다. [ad-hoc note]
- 독립 분석은 “공통 입력 패킷만 지정 순서”, 다른 세션 결과는 “찾거나 읽거나 언급하지 마세요”, 지정된 단일 산출물만 편집한다. 미검증 물리는 `[예상]`으로 남긴다.
- Maplog에서 “읽어만 봐. 아직 작업 아니야” 같은 읽기·문서 정비·방향 탐색은 구현 승인이 아니다. 구현 전 대상·범위·완료 조건을 확인하고, 감상·선택 UX는 대안을 먼저 비교한다.
- Maple 도구 개선은 실제 CLI를 먼저 써 보고 관찰된 마찰만 최소 수정한다. EXP/구매 상담은 사용자 단위·실제 스크린샷을 우선하고 결론·구매 상한부터 제시한다.
- Maplog completed-work 보고는 무엇이 바뀌었고 원래 계획과 어떻게 연결되며 지금 무엇을 할 수 있고 무엇이 남았는지 평이한 한국어로 먼저 설명한다. 출처와 `proposed/user-confirmed/implemented/verified` 상태를 분리한다. [ad-hoc note]

## General Tips

- `research-browser-router`: Consult는 좁은 공개 판단, Grok+Aside는 로그인 포함 넓은 탐색/정확한 클릭; 성공 시 compact report만 읽고 raw logs는 실패·모순 때만 연다.
- Aside ChatGPT `contenteditable`은 click + `keyboard.insertText()`로 입력하고 fresh snapshot/detached-ref 재탐색을 쓴다. Grok Aside provider는 `xai-grok-oauth`, model은 `grok-4.6`이다.
- Karabiner는 current JSON 백업 → 마지막 정상 backup 복원 → JSON/hash/profile/service → 실제 키 테스트 순서다.
- Maplog 새 세션은 `record/CURRENT.md` → `record/PRODUCT.md` → `record/README.md`를 먼저 읽는다.
- OpenAI Game canonical gate는 `/Users/wooojin/App/openaigame/docs/14-execution-gates.md`; 최소 경로는 `START_HERE.md` → `AGENTS.md` → `DECISIONS.md` → `docs/14` §0·§4 → `docs/28`이다.
- OpenAI Game Fable은 independent input일 뿐: phase transition/새 시스템/`REFERENCE`·`DRAFT` 전환에서 medium plan mode로 쓰고, 실제 플레이·문서 대조와 범위 승인 후 별도 구현으로 넘긴다. [ad-hoc note]
- OpenAI Game aerial lab은 `WORLD_PRESETS[*].forms`가 visual/collision SSOT다. static pass만으로 사용자 비교/최종 선택을 완료 처리하지 않는다.
- Git 메타데이터가 없는 폴더에서는 `git diff` 대신 대상 파일 hash·mtime·필수 섹션/링크 검사로 검증한다.
- 대회는 `한 줄 → 한 사용자 경로 → 한 코드 경로 → 한 검증 명령 → 한 제출 주장`을 먼저 잇고, final PASS는 exact ZIP을 fresh directory에서 재검증한 결과로만 말한다. [ad-hoc note]
- 시간·공고·가격·소셜 지표는 live/time-specific이다. 대규모 조사는 범위와 종료 조건을 먼저 자른다.
- Aside `rg` 보안 팝업은 bundled path와 `/opt/homebrew/bin/rg` 링크, `/usr/sbin/spctl`을 먼저 확인한다.
- Codex/Rubato 분리는 `CODEX_HOME`만 바꾸지 말고 cwd도 통제한다. `/tmp`에서 plain home, `codex plugin list`, `codex doctor --json`으로 유효 지침·plugin·provider·MCP를 확인한다.

## What's in Memory

### /Users/wooojin

#### 2026-09-12

- 일반 Codex와 Rubato Codex 분리 실행: CODEX_HOME, /tmp, codex plugin list, codex doctor --json, project .codex, model_instructions_file
  - desc: Rubato가 결합된 기본 Codex에서 순정 Codex를 중립 cwd로 분리·진단한 로컬 설정 사례; cwd=/Users/wooojin.
  - learnings: `CODEX_HOME`만으로는 프로젝트 `.codex` 재주입을 막지 못한다. 새 세션의 유효 지침·플러그인·provider·MCP까지 확인한다.

#### 2026-08-21

- Karabiner Varmilo shortcut rollback: Karabiner, Varmilo, Rectangle, 한영, ⌘⇧3, automatic_backups, keyboard_fn
  - desc: recent Varmilo mappings broke several macOS shortcuts; safe backup rollback, minimal-rule recovery, and real-device validation; cwd=/Users/wooojin.
  - learnings: preserve current `karabiner.json`, restore the closest known-good backup, then verify hash/JSON/profile/service and actual keys.

### /Users/wooojin/App/maplog

#### 2026-09-10

- Document reset and Place·Visit approval boundary: record/PRODUCT.md, record/CURRENT.md, Place-first, Visit, Journey, scope-creep, scroll, swipe album
  - desc: 최신 Maplog 입구·제품 정의와 Place·Visit browse가 구현 승인으로 과잉 해석된 사례; cwd=/Users/wooojin/App/maplog.
  - learnings: 문서 정비 → 방향 탐색 → 최소 기술 연결 → 제품 UX 구현을 별도 승인으로 둔다.

### /Users/wooojin/dev/maple

#### 2026-09-10

- 챌린저스 시즌4 보상 반입과 이지 벨로나: 200레벨 달성의 비약, 월드 리프, 메멘토 큐브, 레공레, Maplescouter, 130.8%, 핀볼
  - desc: 보상/코인샵을 반입 상태로 분류하는 조사와 레공레 이지 벨로나의 스펙·패턴 병목 판단; cwd=/Users/wooojin/dev/maple.
  - learnings: 전체 이벤트별 분류표는 미완결이고, 130.8%는 딜 부족이 아니라 패턴 숙련을 더 봐야 한다는 뜻이다.

### /Users/wooojin/App/openaigame

#### 2026-08-21

- A-world structure proposal: docs/29-aerial-world-structure-exploration-brief.md, aerial-world-sol-medium, speed-wing, glide-wing, open-air, collision-outline
  - desc: 지정 문서 하나에 A안의 단일 공중 월드 비전과 열린 공중·두 날개 경로 분기·폐기 기준을 작성한 설계 작업; cwd=/Users/wooojin/App/openaigame.
  - learnings: 큰 형태 사이를 통과하게 하고, 양 날개가 같은 선을 택하거나 glider가 비용 없는 안전선이 되면 폐기한다. 구현 승인이나 최종 승자 판정은 아니다.
- Isolated aerial-world comparison lab: experiments/aerial-world-lab, WORLD_PRESETS, world-presets.js, aerial-world-lab-flight-telemetry-v1, inspectX, V, R, J, F1
  - desc: docs/31 승인 브리프의 A/B/C preset lab 구현과 current-code/browser verification; cwd=/Users/wooojin/App/openaigame.
  - learnings: `WORLD_PRESETS[*].forms` is visual/collision SSOT; first-impression flights, same-input telemetry replay, and final selection remain unverified.

### Older Memory Topics

#### /Users/wooojin

- Aside rg macOS security warning: Aside, rg, ripgrep, com.apple.quarantine, /usr/sbin/spctl, CoreServicesUIAgent, /opt/homebrew/bin/rg
  - desc: quarantined Aside-bundled ripgrep의 반복 보안 경고를 실제 실행 경로 교체로 해결한 로컬 macOS troubleshooting; cwd=/Users/wooojin.
- Consult/Grok+Aside research routing: research-browser-router, run_aside_consult.py, run_grok_research.py, xai-grok-oauth, grok-4.6, grok-report.md
  - desc: implicit lightweight router, Aside ChatGPT Consult, and native Grok execution for public and logged-in browser research; cwd=/Users/wooojin, secondary=/Users/wooojin/dev/maple.
- 백석대 2026-2 수강계획 보류: 기독교세계관, 서현덕 월2, 김은득 수4, 기독교탐사, 월·수·목 등교
  - desc: confirmed courses and the two-person timetable dependency; cwd=/Users/wooojin. [ad-hoc note]
- Hackathon proof-spine workflow: Cofathon, KB AI Challenge, START_HERE.md, DECISIONS.md, CONTRACT.md, RELEASE.md, final ZIP
  - desc: contest worktree integration, claim-evidence chain, and fresh-archive verification; cwd=/Users/wooojin. [ad-hoc note]

#### /Users/wooojin/App/maplog

- Manual representative cover and native-quality escalation: manual representative-only, rear layers, deterministic, legacy cover order, NMFMarker, scenario expected actual verdict evidence
  - desc: one manual Gathering representative with deterministic automatic rear layers, plus when to pivot a live map from a tuned overlay to native marker rendering; cwd=/Users/wooojin/App/maplog. [ad-hoc note]
- Design-stage boundaries, reporting, and model routing: 2026-07-12_product_development_plan.md, Fable, Terra, provenance, user-confirmed, native interaction
  - desc: structure-first scope control, completed-work reporting, model-routing recommendation, and native pivot; cwd=/Users/wooojin/App/maplog. [ad-hoc note]

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
