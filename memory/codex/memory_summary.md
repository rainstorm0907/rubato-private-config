v1

## User Profile

우진은 Maplog, MapleStory 도구, OpenAI Game, Rubato/Codex 환경과 대회 작업을 반복해서 다뤄. 실제 파일·실행 결과·원문·정확한 오류를 근거로 결론 내리길 원하고, 설치 성공·기술적 가능·사용자 체험 완료·머지 권장을 서로 섞지 않아. Maplog에서는 private-first 사진 경험, 한 장만 수동 선택하는 cover contract, 네이티브 계층까지 포함한 핵심 조작 품질을 중시해. 문서 정비·방향 탐색과 제품 UX 구현은 별도 승인이고, OpenAI Game은 단계·한 가설·근거 문서와 실제 플레이가 있을 때만 구현해. 공유 작업에서는 기존 변경·개인 설정·세션을 보존하는 쪽을 우선해. [ad-hoc note]

## User preferences

- “우리 세팅 그대로인지 확인”이면 성공 실행만 말하지 말고, pre/post 설정·인증·모델 저장소와 실제 UI 상태로 보존을 증명해.
- 기존 개인 커밋·설정·세션은 off-limits로 두고, 복구는 새 세션으로 우회해. PR이 mergeable이어도 빨간/pending CI가 남으면 머지 권장과 분리해서 보고해.
- “읽어만 봐. 아직 작업 아니야” 같은 읽기·문서 정비·방향 탐색은 구현 승인이 아니야. 구현 전 대상·범위·완료 조건을 짧게 확인하고, 감상·선택 UX는 하나를 고정하기 전에 대안을 비교해.
- OpenAI Game 구현·위임 전 `현재 단계 / 판정할 가설 하나 / 근거 문서와 절`을 제시해. `REFERENCE`·`DRAFT`와 음향 비교 중 맵 재설계 메모는 구현 허가가 아니야. [ad-hoc note]
- Maple 조사 답은 “모든 보상들”이면 직접 수령/리프 반입/리프 불가 표부터, 보스는 스펙상 가능과 첫 클리어 체감 난이도를 분리해서 말해.
- 핵심 조작감·지도·미디어·실시간 UI는 튜닝한 타협안보다 가능한 정석 native/platform 계층을 먼저 검토해. [ad-hoc note]

## General Tips

- Rubato GUI는 `/Users/wooojin/dev/Rubato`에서 `bash harness/t3-integration/install-gui.sh --apply`; GUI `~/.rubato/t3-home`와 기존 CLI `~/.rubato/agent`는 분리돼. 실제 UI와 codesign까지 확인해.
- stale queue는 pending message를 자동 삭제하지 말고 Resume/Discard와 replay-failure 보존을 확인해. `gh pr view`, `gh pr checks`, 실패 job 로그로 변경 파일과 CI 소유 영역을 분리해 봐.
- Codex/Rubato 분리는 `CODEX_HOME`만 바꾸지 말고 cwd도 통제해. `/tmp`에서 plain home, `codex plugin list`, `codex doctor --json`으로 유효 지침·plugin·provider·MCP를 확인해.
- Maplog 새 세션은 `record/CURRENT.md` → `record/PRODUCT.md` → `record/README.md`부터 읽어. 테스트 보관함의 동작은 연결 증거일 뿐 실제 사진 감상 품질 증거는 아니야.
- OpenAI Game canonical gate는 `/Users/wooojin/App/openaigame/docs/14-execution-gates.md`; Fable은 독립 입력일 뿐이고 구현 승인이나 파일 수정 권한이 아니야. [ad-hoc note]
- Aside `rg` 보안 팝업은 bundled path, `/usr/sbin/spctl`, `/opt/homebrew/bin/rg` 링크부터 확인하고 Aside 업데이트 뒤 재점검해.
- 대회는 `한 줄 → 한 사용자 경로 → 한 코드 경로 → 한 검증 명령 → 한 제출 주장`을 먼저 잇고, final PASS는 exact ZIP을 fresh directory에서 재검증한 결과로만 말해. [ad-hoc note]

## What's in Memory

### /Users/wooojin/dev/Rubato

#### 2026-09-15

- Rubato desktop GUI 설치와 T3 stale queue PR: install-gui.sh, t3-home, rubato-pi, /Applications/Rubato.app, stale-queue, pendingMessageCount, PR #12, restart-profile.test.mjs
  - desc: 기존 CLI 설정 보존을 hash/UI로 검증한 GUI 설치와 Maplog queued message 복구·PR #12의 머지 보류 판단; cwd=/Users/wooojin/dev/Rubato.
  - learnings: 설치 UI 성공과 CLI 보존을 따로 증명하고, `MERGEABLE`이어도 `UNSTABLE` CI·pending check이면 작업 세션을 보존하며 머지 결정을 미뤄.

### /Users/wooojin

#### 2026-09-12

- 일반 Codex와 Rubato Codex 분리 실행: CODEX_HOME, /tmp, codex plugin list, codex doctor --json, project .codex, model_instructions_file
  - desc: Rubato가 결합된 기본 Codex에서 순정 Codex를 중립 cwd로 분리·진단한 로컬 설정 사례; cwd=/Users/wooojin.
  - learnings: `CODEX_HOME`만으로는 프로젝트 `.codex` 재주입을 막지 못해. 새 세션의 유효 지침·플러그인·provider·MCP까지 확인해.

### /Users/wooojin/App/maplog

#### 2026-09-10

- Document reset and Place·Visit approval boundary: record/PRODUCT.md, record/CURRENT.md, Place-first, Visit, Journey, scope-creep, scroll, swipe album
  - desc: 최신 Maplog 입구·제품 정의와 Place·Visit browse가 구현 승인으로 과잉 해석된 사례; cwd=/Users/wooojin/App/maplog.
  - learnings: 문서 재정비 → 방향 탐색 → 최소 기술 연결 → 제품 UX 구현은 별도 승인이고, date browse의 핵심 대안을 먼저 열어.

### /Users/wooojin/dev/maple

#### 2026-09-10

- 챌린저스 시즌4 보상 반입과 이지 벨로나: 200레벨 달성의 비약, 월드 리프, 메멘토 큐브, 레공레, Maplescouter, 130.8%, 핀볼
  - desc: 보상/코인샵을 반입 상태로 분류하는 조사와 레공레 이지 벨로나의 스펙·패턴 병목 판단; cwd=/Users/wooojin/dev/maple.
  - learnings: 전체 이벤트별 분류표는 미완결이고, 130.8%는 딜 부족보다 패턴 숙련을 더 봐야 한다는 뜻이야.

### Older Memory Topics

#### /Users/wooojin

- Aside rg macOS security warning: Aside, rg, ripgrep, com.apple.quarantine, /usr/sbin/spctl, CoreServicesUIAgent, /opt/homebrew/bin/rg
  - desc: quarantined Aside-bundled ripgrep의 반복 보안 경고를 실제 실행 경로 교체로 해결한 troubleshooting; cwd=/Users/wooojin.
- 백석대 2026-2 수강계획 보류: 기독교세계관, 서현덕 월2, 김은득 수4, 기독교탐사, 월·수·목 등교
  - desc: 확정 과목과 두 사람 시간표 의존성 때문에 분반 선택을 보류한 기록; cwd=/Users/wooojin. [ad-hoc note]
- Hackathon proof-spine: Cofathon, KB AI Challenge, START_HERE.md, DECISIONS.md, CONTRACT.md, RELEASE.md, final ZIP
  - desc: worktree 통합, claim-evidence chain, fresh-archive 제출 검증; cwd=/Users/wooojin. [ad-hoc note]

#### /Users/wooojin/App/maplog

- Manual representative, native map quality, and prompt routing: manual representative-only, deterministic rear layers, NMFMarker, Fable, Terra, provenance
  - desc: 하나의 수동 대표 사진과 자동 rear layer 계약, native marker escalation, 구현 프롬프트 모델 추천·보고 경계; cwd=/Users/wooojin/App/maplog. [ad-hoc note]
- Structure-first implementation boundary: 2026-07-12_product_development_plan.md, interaction spec, fixture, runtime, scope control
  - desc: 구조·계약을 먼저 고정하고 fixture와 runtime을 분리하는 Maplog 구현 단계 경계; cwd=/Users/wooojin/App/maplog. [ad-hoc note]

#### /Users/wooojin/dev/maple

- HEXA, challenger research, efficiency, and boss workflows: hexaOrder, V core, VI tooltip, item-equipment.json, Maplescouter, boss ratio, 레공레, 오렌지솥밥
  - desc: HEXA delta, 챌섭 시세/커뮤, Maplescouter API, precise-vs-rough 효율, 실제 보스 benchmark; cwd=/Users/wooojin/dev/maple. [ad-hoc note]
- YouTube research playback safety: transcript, subtitles, timestamp, --mute-audio, isolated browser profile
  - desc: transcript-first muted inspection for Maple videos; cwd=/Users/wooojin/dev/maple. [ad-hoc note]

#### /Users/wooojin/App/openaigame

- OpenAI Game execution gates and later map-redesign input: docs/14-execution-gates.md, REFERENCE, DRAFT, v4, anti-forcing, Fable medium, 맵 재설계
  - desc: brief gate, Fable/Telegram boundary, and later map-design input that does not authorize implementation; cwd=/Users/wooojin/App/openaigame. [ad-hoc note]
