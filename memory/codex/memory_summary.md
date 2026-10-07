v1

## User Profile

우진은 Maplog, MapleStory, Rubato/Codex 환경, OpenAI Game, 해커톤을 반복해서 다뤄. 실제 파일·실행 결과·정확한 오류를 근거로 결론 내리고, 설치 성공·기술적 가능·사용자 체험 완료·머지 권장을 구분해. 개인 설정·확장·세션·기존 변경을 함부로 건드리지 않는 보존 경계를 중시해. Maplog에서는 private-first 사진 경험, 한 장만 수동 선택하는 cover contract, 핵심 조작감에는 네이티브 계층까지 포함한 정석 품질을 요구해. 문서 정비·방향 탐색과 제품 UX 구현은 별도 승인이고, OpenAI Game은 단계·한 가설·근거 문서와 실제 플레이가 있을 때만 구현해. [ad-hoc note]

## User preferences

- “최신 업뎃대로 맞추면서 개인 오버레이는 냅두고” 또는 “우리 세팅 그대로인지 확인”이면 개인 설정·확장·오버레이·세션을 off-limits로 두고, pre/post manifest와 실제 UI로 보존을 증명해.
- 재시작·빌드 exit 0만 성공으로 말하지 말고, 실제 창의 기존 프로젝트·세션·모델과 필요한 bridge/runtime 상태까지 확인해.
- 기존 개인 커밋·설정·세션은 보존하고, 복구는 새 세션으로 우회해. PR이 mergeable이어도 빨간/pending CI가 남으면 머지 가능과 권장을 분리해서 보고해.
- “읽어만 봐. 아직 작업 아니야” 같은 읽기·문서 정비·방향 탐색은 구현 승인이 아니야. 구현 전 대상·범위·완료 조건을 짧게 확인하고, 감상·선택 UX는 하나를 고정하기 전에 대안을 비교해.
- OpenAI Game 구현·위임 전 `현재 단계 / 판정할 가설 하나 / 근거 문서와 절`을 제시해. `REFERENCE`·`DRAFT`와 음향 비교 중 맵 재설계 메모는 구현 허가가 아니야. [ad-hoc note]
- Maple 조사에서는 “모든 보상들”이면 직접 수령/리프 반입/리프 불가 표부터, 보스는 스펙상 가능과 첫 클리어 체감 난이도를 분리해서 말해.
- 핵심 조작감·지도·미디어·실시간 UI는 튜닝한 타협안보다 가능한 정석 native/platform 계층을 먼저 검토해. [ad-hoc note]

## General Tips

- Rubato 패키징 오류는 source freshness만 믿지 말고 설치된 `~/.rubato-pi/stock-engine`의 feature/package closure와 실제 import를 확인해. 재빌드 뒤에는 bridge, codesign, 실제 GUI를 분리 검증해.
- Rubato 업데이트 뒤 멈춤은 중복 Electron, `pi.sock` 연결, `pi-server.log`/`t3-bridge.log`, `EMFILE`부터 확인해. 종료 요청을 받으면 GUI·launcher·고아 engine까지 PID로 재확인해.
- Codex/Rubato 분리는 `CODEX_HOME`만 바꾸지 말고 cwd도 통제해. `/tmp`에서 plain home, `codex plugin list`, `codex doctor --json`으로 유효 지침·plugin·provider·MCP를 확인해.
- Maplog 새 세션은 `record/CURRENT.md` → `record/PRODUCT.md` → `record/README.md`부터 읽어. 테스트 보관함 동작은 연결 증거일 뿐 실제 사진 감상 품질 증거는 아니야.
- 대회는 `한 줄 → 한 사용자 경로 → 한 코드 경로 → 한 검증 명령 → 한 제출 주장`을 먼저 잇고, final PASS는 exact ZIP을 fresh directory에서 재검증한 결과로만 말해. [ad-hoc note]

## What's in Memory

### /Users/wooojin/dev/Rubato

#### 2026-09-24

- Rubato engine recovery and personal-overlay preservation: request-images.mjs, ERR_MODULE_NOT_FOUND, contextNoteSources, build-active-engine, stock-engine, personal_manifest=identical, catalogue ok 22
  - desc: 패키징 목록 누락으로 설치 엔진이 시작하지 않은 사례의 최소 수정·재빌드·실제 GUI 검증; 작업은 `/Users/wooojin/dev/Rubato`, rollout cwd는 `/Users/wooojin/App/maplog`로 기록됨.
  - learnings: source가 최신이어도 설치본 closure를 검사하고, 개인 파일 manifest와 GUI/bridge를 모두 확인해.

#### 2026-09-15

- Rubato desktop GUI install and T3 stale-queue PR: install-gui.sh, t3-home, rubato-pi, stale-queue, Resume, Discard, PR #12, restart-profile.test.mjs
  - desc: 기존 CLI 보존을 hash/UI로 검증한 T3 GUI 설치와 queued message 복구·PR 머지 보류 판단; cwd=/Users/wooojin/dev/Rubato.
  - learnings: `MERGEABLE`이어도 `UNSTABLE` CI·pending check이면 실행 중 세션을 보존하고 머지를 미뤄.

### /Users/wooojin

#### 2026-09-21

- Post-update Rubato session freeze and shutdown: duplicate-GUI, pi.sock, EMFILE: too many open files, watch, start-electron, pgrep -lf
  - desc: 중복 GUI·끊긴 Unix socket·고아 `pi-server`가 함께 나타난 세션 정지의 진단과 완전 종료 검증; cwd=/Users/wooojin.
  - learnings: `osascript` 성공만 믿지 말고 socket/log와 owned PID·창이 모두 사라졌는지 확인해.

### Older Memory Topics

#### /Users/wooojin

- Plain Codex isolation: CODEX_HOME, /tmp, codex plugin list, codex doctor --json, project .codex
  - desc: cwd의 프로젝트 config 재주입을 피하며 순정 Codex를 검증하는 절차; cwd=/Users/wooojin.
- Aside rg security warning: Aside, com.apple.quarantine, spctl, /opt/homebrew/bin/rg
  - desc: quarantined Aside-bundled ripgrep 보안 팝업을 실행 경로 교체로 고친 사례; cwd=/Users/wooojin.
- 백석대 2026-2 수강계획: 기독교세계관, 서현덕 월2, 김은득 수4, 기독교탐사
  - desc: 여자친구 시간표가 정해진 뒤 공용 분반을 고르는 보류 결정; cwd=/Users/wooojin. [ad-hoc note]
- Hackathon proof-spine: Cofathon, KB AI Challenge, START_HERE.md, CONTRACT.md, RELEASE.md, final ZIP
  - desc: worktree 통합, claim-evidence chain, fresh-archive 제출 검증; cwd=/Users/wooojin. [ad-hoc note]

#### /Users/wooojin/App/maplog

- Document reset and Place·Visit approval boundary: record/CURRENT.md, record/PRODUCT.md, Place-first, Visit, Journey, scroll, swipe album
  - desc: 최신 제품 입구와 Place·Visit browse가 구현 승인으로 과잉 해석된 사례; cwd=/Users/wooojin/App/maplog.
- Manual representative and native map quality: manual representative-only, deterministic rear layers, NMFMarker, native overlay
  - desc: 한 장의 수동 대표와 자동 rear layer contract, marker sync 품질의 native escalation; cwd=/Users/wooojin/App/maplog. [ad-hoc note]
- Structure, provenance, and model routing: 2026-07-12_product_development_plan.md, fixture, runtime, Fable, Terra, decision status
  - desc: 구조-first 구현 단계, 완료 보고 provenance, visual prototype와 production integration의 분리; cwd=/Users/wooojin/App/maplog. [ad-hoc note]

#### /Users/wooojin/dev/maple

- Challenger rewards and Easy Bellona: 200레벨 달성의 비약, 월드 리프, 메멘토 큐브, 레공레, Maplescouter, 130.8%, 핀볼
  - desc: 반입 상태 보상 분류와 스펙·패턴 병목을 분리한 보스 판단; cwd=/Users/wooojin/dev/maple.
- HEXA, market, and boss workflows: hexaOrder, VI tooltip, item-equipment.json, quiet-browse, Maplescouter API, boss ratio, 레공레, 오렌지솥밥
  - desc: HEXA delta, 챌섭 시세/커뮤니티, direct API, precise-vs-rough 효율, 캐릭터별 실제 보스 benchmark; cwd=/Users/wooojin/dev/maple. [ad-hoc note]
- YouTube research playback safety: transcript, subtitles, timestamp, --mute-audio, isolated browser profile
  - desc: Maple 영상은 transcript-first, 필요한 timestamp만 muted isolated browser로 보는 절차; cwd=/Users/wooojin/dev/maple. [ad-hoc note]

#### /Users/wooojin/App/openaigame

- OpenAI Game execution gates and map-redesign input: docs/14-execution-gates.md, REFERENCE, DRAFT, v4, anti-forcing, 맵 재설계
  - desc: brief gate, Fable/Telegram boundary, 후속 맵 입력이 구현 승인이 아닌 경계; cwd=/Users/wooojin/App/openaigame. [ad-hoc note]
