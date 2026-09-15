# Raw Memories

Merged stage-1 raw memories (stable ascending thread-id order):

## Thread `019fa306-06b3-71f3-a29a-649ca3a279a1`
updated_at: 2026-08-13T14:05:16+00:00
cwd: /Users/wooojin/dev/maple
rollout_path: /Users/wooojin/.codex/sessions/2026/07/27/rollout-2026-07-27T19-01-48-019fa306-06b3-71f3-a29a-649ca3a279a1.jsonl
rollout_summary_file: 2026-07-27T10-01-48-N8Pv-maple_tool_optimization_and_legongre_exp_event_workflow.md

---
description: Maple 프로젝트 실제 사용 기반 도구 개선, 14일 snapshot 재사용 정책, 레공레 경험치/메카베리 계산 및 운영 규칙
 task: maple-tool-optimization-and-legongre-exp-planning
 task_group: maple-growth-assistant
 task_outcome: success
 cwd: /Users/wooojin/dev/maple
 keywords: maple-growth-assistant, growth-assistant, latest_digest, package_share, 레공레, 모멘텀-패스, 메카베리, 소재, KST, quiet-browse, ECONNREFUSED
---

### Task 1: 실제 도구 실행과 최소 개선

task: run-maple-tools-and-fix-observed-friction
task_group: maple-tooling
task_outcome: success

Preference signals:
- 사용자가 “오늘 한번 업뎃하고 2주정돈 괜찮”이라고 했다 -> snapshot에 고정 30분 freshness gate를 두지 말고 오늘 갱신한 데이터는 약 14일 재사용한다. 단, 경매장 매물·이벤트 일정·주간 진행은 별도 최신 확인.
- 사용자는 도구 코드를 실제로 사용해 보며 최적화할 것을 요청했다 -> 문서만 보고 과잉 설계하지 말고 실제 CLI 실행에서 관찰된 마찰만 최소 수정한다.

Reusable knowledge:
- 진입 문서: `AGENTS.md` → `kb/codex-brief.md` → `kb/session-handoff.md`.
- 실제 갱신 명령: `./scripts/fetch_character.sh <캐릭터명>`.
- `today`는 KST로 표시해야 한다. `formatSeoulTimestamp()`가 UTC ISO 출력 문제를 해결했다.
- 해방 필드는 실제로 추적 중인 캐릭터에서만 blocker를 만들고, `manual.liberation`이 완전히 비어 있으면 blocker를 만들지 않는다.
- 브라우저 정찰 실패는 부분 결과를 보존하되 `latest_digest.sh`가 exit 1을 반환해야 한다. 검증 실패 사례: `ECONNREFUSED 127.0.0.1:9223`.
- `package_share.sh` 보안 검사는 느슨하게 하지 않는다. KB에 남은 `/Users/...` 경로를 제거하면 공유 zip과 secret scan이 통과한다.

Failures and how to do differently:
- `rg`를 `character` 전체에 실행하면 대형 JSON으로 출력이 폭발한다. 특정 파일/필드와 `jq` projection을 사용한다.
- 브라우저 섹션 실패를 파일 생성만으로 성공 판단하지 않는다.

References:
- `npm test` → growth 테스트 7개 통과, auction fixture/429 backoff 통과.
- `bash -n scripts/*.sh && node --check tools/auction-scan.js` 통과.
- `package_share PASS (non-empty archive, secret scan passed)`.

### Task 2: 레공레 경험치·모멘텀 패스·메카베리

task: calculate-legongre-exp-bm-and-mechaberry-order
task_group: maple-exp-planning
 task_outcome: success

Preference signals:
- 사용자는 “1소재=30분”으로 계산하고 “시간대비 몇억까지인지 결론”을 원했다 -> 답변은 소재/시간/메소 환산과 구매 상한을 결론 먼저 제시한다.
- 구매 후에는 실제 사용 직전 수치와 스크린샷을 우선해 계산을 갱신한다.

Reusable knowledge:
- 레공레 기준 1소재(30분)는 약 0.545~0.581% EXP.
- 모멘텀 패스 유료 보상은 메카베리 10장 + 상급 EXP 9,000장. 당시 추정은 약 160~171소재, 80~85시간 사냥 상당.
- 49,800원, 억당 1,600원 가정 시 31.125억 메소 상당. 30억까지 확실히 납득 가능, 35억까지 시간 절약 목적이면 허용.
- 메카베리→상급 EXP와 상급 EXP→메카베리는 실측 차이가 반올림 오차 수준(약 Lv.284 69.360% vs 69.359%). 편한 순서로 사용해도 된다.
- 메카베리 피버는 경험치 배율이 아니다. 피버 중 `슈피겔버스트`를 쿨타임 없이 사용하게 할 뿐이다. 추가 경험치 효과도 적용되지 않는다. 30분 제한 내 복구율 100%를 달성하고, 피버 중 퇴장하면 재입장 시 게이지가 초기화된다.

Failures and how to do differently:
- 4배 경쿠 3시간 전체를 절약 시간으로 세지 말고, 평소 3배 대비 추가분만 분리한다.
- 예측값보다 실제 스크린샷이 우선이다. 실제 사용 후 결과는 Lv.284 76.386%로 이전 예측보다 높았다.

References:
- `1소재 = 30분 사냥`
- `https://maplestory.nexon.com/news/update/790`
- `https://mapleroad.kr/lib/calculator/golden_berry`
- `https://mapleroad.kr/lib/calculator/exp`
- `https://mapleroad.kr/lib/exp_calculator/hunt`

### Task 3: 렌 창룡파천검 질문

task: explain-ren-changryongpacheongeom-activation
task_group: maple-skill-help
 task_outcome: partial

Preference signals:
- 사용자는 “쉽게 설명좀해줘”라고 했다 -> 스킬 사용법은 복잡한 원리보다 게임 내 입력 순서와 핵심 조건을 짧게 설명한다.

Reusable knowledge:
- `./scripts/fetch_character.sh 렌`은 API HTTP 400, `OPENAPI00004 Please input valid parameter`로 실패했다.
- 전체 JSON grep은 출력 폭발 위험이 있다. 관련 파일을 좁혀 읽어야 한다.

Failures and how to do differently:
- API 400 시 traceback 대신 상태 코드와 error body를 먼저 출력한다.
- 검색 자료에서 창룡파천검 관련 트리거가 일부 보였지만, 공식 입력 순서를 확정하지 못했으므로 다음 실행에서는 공식 스킬 설명/툴팁을 먼저 검증한다.

References:
- `{"error":{"name":"OPENAPI00004","message":"Please input valid parameter"}}`
- 검색 핸들: `창룡파천검 : 승천`, `망혼검 절기 : 심검 이후 발동`

## Thread `019fcaac-6218-7d51-9588-26b61af9a752`
updated_at: 2026-08-04T14:50:45+00:00
cwd: /Users/wooojin/App/maplog
rollout_path: /Users/wooojin/.codex/sessions/2026/08/04/rollout-2026-08-04T11-48-42-019fcaac-6218-7d51-9588-26b61af9a752.jsonl
rollout_summary_file: 2026-08-04T02-48-42-CVQC-kb_ai_submission_check_and_claude_skill_port.md

---
description: GitHub에서 KB AI Challenge 최종 제출 ZIP을 확인하고, Codex용 framing/reframing 사고 스킬을 Claude Code용으로 이식·검증·설치한 작업
 task: kb-ai-challenge-submission-and-claude-skill-port
 task_group: contest-workflow-and-cross-agent-skill-installation
 task_outcome: success
 cwd: /Users/wooojin/App/maplog
 keywords: KB-hackaton, KB이음케어_우브라더스_제출_최종.zip, GitHub, framing, reframing, Claude Code, Agent, meight, consult, staging, skill discovery
---

### Task 1: GitHub 최종 제출물 확인

task: locate and verify KB AI Challenge final ZIP in GitHub
task_group: contest submission verification
task_outcome: success

Reusable knowledge:
- 최종 제출 저장소는 비공개 `keepitmello/KB-hackaton`이며, 최종 ZIP은 `KB이음케어_우브라더스_제출_최종.zip`이다.
- ZIP은 2026-08-03 16:05:42 KST 커밋 `587c9dec032e8043c303829e29ce0636dad633c7`에 포함됐고 약 6.78MB다.
- 저장소 트리에서 기술설명서 PDF, 참가 서류, 프로토타입 코드, 스크린샷이 함께 제출된 것을 확인했다.

Failures and how to do differently:
- 개인 저장소만 검색하면 대상이 누락될 수 있다. GitHub API에서 `affiliation=owner,collaborator,organization_member`로 소속 저장소까지 조회해야 한다.

References:
- `https://github.com/keepitmello/KB-hackaton`
- `KB이음케어_우브라더스_제출_최종.zip`
- `587c9dec032e8043c303829e29ce0636dad633c7`

### Task 2: Claude Code용 framing/reframing 이식

task: adapt Codex framing/reframing skills to Claude Code and install them
task_group: cross-agent skill installation
 task_outcome: success

Preference signals:
- 사용자가 “매번 사용이 아니라 특이 사항 설계 간에서 사용하는 것”이라고 했으므로 두 스킬을 일반 작업의 상시 게이트로 만들지 말고 명시적·선택적 호출 도구로 유지한다.
- 사용자가 Claude 환경에 맞춰 “다시 Fable한테 ... 수정해서 설치”하라고 했으므로 Codex 파일을 그대로 복사하지 말고 대상 환경의 `CLAUDE.md`, 기존 스킬 관례, 실제 도구명을 먼저 확인한다.

Reusable knowledge:
- Claude의 실제 위임 명칭은 `Agent`; Codex 작업은 `meight`, 외부 고품질 검토는 `consult` 경로로 연결한다.
- `~/.claude/skills` 직접 쓰기는 민감 경로 보안 경계로 차단될 수 있다. `/Users/wooojin/Downloads/claude-framing-skills-staging` 같은 허용 staging에 먼저 작성하고 최종 이동한다.
- 설치 후 검증 순서: 파일 트리 → frontmatter → 상대 링크 존재 여부 → JSON 유효성 → Codex 전용 잔재 grep → 새 Claude 세션에서 `/framing`, `/reframing` smoke test.
- 최종 설치 위치: `/Users/wooojin/.claude/skills/framing`, `/Users/wooojin/.claude/skills/reframing`.

Failures and how to do differently:
- Fable의 직접 설치 시도는 `sensitive file` 권한 오류로 차단됐다. 처음부터 staging 생성과 최종 이동을 분리한다.
- 초기 이식본에 `Task(Agent)`, 존재하지 않는 `roo-channel` 링크, 잘못된 `references/...` 상대경로가 남았다. 실제 Claude 설정과 파일 기준 경로를 대조해 설치 전에 제거·수정한다.

References:
- `/Users/wooojin/.claude/CLAUDE.md`
- `/Users/wooojin/.claude/skills/framing/SKILL.md`
- `/Users/wooojin/.claude/skills/reframing/SKILL.md`
- Smoke 결과: `/framing`은 상시 게이트가 아닌 명시적 호출 도구로, `/reframing`은 사용자 승인 후 수동 실행 도구로 정상 discovery됨.

## Thread `01a010c2-1a1d-7b41-a3f8-3f38339acecf`
updated_at: 2026-08-17T17:35:41+00:00
cwd: /Users/wooojin/App/openaigame
rollout_path: /Users/wooojin/.codex/sessions/2026/08/18/rollout-2026-08-18T02-25-51-01a010c2-1a1d-7b41-a3f8-3f38339acecf.jsonl
rollout_summary_file: 2026-08-17T17-25-51-AJQ3-independent_aerial_scene_comparison_grok_4_6.md

---
description: 독립 공중 맵 장면 A/B 분석을 규약대로 단일 파일에 작성 완료; A안 판정과 엄격한 입력·출력·검증 절차
 task: independent-aerial-scene-comparison
 task_group: openaigame-scene-design
 task_outcome: success
 cwd: /Users/wooojin/App/openaigame
 keywords: openaigame, scene-comparison-protocol, aerial-map, Grok-4.6, docs/23, glide-boost, apply_patch, git-status
---

### Task 1: 독립 공중 장면 A/B 비교

task: `docs/28-scene-comparison-protocol.md`에 따른 독립 분석 파일 작성
task_group: openaigame scene design
task_outcome: success

Preference signals:
- 사용자는 “공통 입력 패킷만 지정 순서로 읽으세요”라고 요구했다 -> 유사한 독립 분석에서는 지정 문서만 정확한 순서로 읽는다.
- 사용자는 “다른 분석 세션의 존재나 결과를 찾거나 읽거나 언급하지 마세요”라고 요구했다 -> 교차 세션 오염을 피하고 다른 결과를 탐색하지 않는다.
- 사용자는 “유일한 산출물은 ... 지정된 파일 하나”라고 요구했다 -> 승인된 파일 하나만 수정하고 나머지 프로젝트 파일은 건드리지 않는다.
- 사용자는 좌표·픽셀 수치·블록맵·구조도·코드 산출 금지를 명시했다 -> 장면·감각·물리 문법 수준에서만 분석한다.

Reusable knowledge:
- 현재 프로젝트 단계는 열린 공중 맵 장면 비교다. A/B 중 하나를 선택하기 전 구조도·블록맵·좌표·구현으로 내려가지 않는다.
- `docs/23-measured-balance-patch.md`에서 속도날개 I의 약 32,000px 도달은 검증됐지만, 활공 상승 부스터와 패치 후 카메라 감각은 `[예상]`으로 남겨야 한다.
- 규약 §3 필수 출력 제목은 A/B 각각 `대표 비행 1회 서사`, `속도날개 경로 vs 활공날개 경로`, `랜드마크 3개`, `다시 오고 싶은 구석 1곳`, `실패 위험`이며, 이후 `## 판정`과 `## 이 판정을 뒤집을 수 있는 것`을 포함한다.
- 최종 산출물은 `/Users/wooojin/App/openaigame/docs/reviews/scene-comparison-grok-4.6-high.md`에 작성됐고, 필수 섹션 검사는 모두 통과했다.
- 분석 판정은 A안 「거대한 매달린 형태」였다. 큰 매달린 형태의 위·아래 공간이 급강하→속도→상승→활공 문법과 속도날개/활공날개의 대가 차이를 더 명확히 보여준다는 논리였다.

Failures and how to do differently:
- `apply_patch` 호출은 문자열/래퍼 형식 오류로 반복 실패했다. 긴 단일 문서 작성에서는 이 환경의 `exec` 내부 Python heredoc으로 대상 파일만 쓰는 방식이 성공했다.
- `git status`는 해당 디렉터리가 Git 저장소가 아니어서 실패했다(`fatal: not a git repository`). 변경 검증은 Git에 의존하지 말고 파일 존재, 필수 제목, 크기, 내용 직접 검사로 대체한다.
- 초기 셸 출력이 비었고 JS 실행기에는 `console`이 없었다. `text(...)`와 반환 객체의 `.output`을 사용해야 한다.

References:
- `/Users/wooojin/App/openaigame/docs/28-scene-comparison-protocol.md`
- `/Users/wooojin/App/openaigame/docs/reviews/scene-comparison-grok-4.6-high.md`
- 검증: 필수 섹션 모두 `OK`; 파일 크기 11089 bytes, 56 lines.
- 판정 비행 전 조건: 활공 상승 부스터·활공날개 II 안전성·카메라 선행 개선은 아직 실제 비행으로 확정되지 않음.

## Thread `01a010c2-1fc1-7060-82f6-5f8df8d6bc42`
updated_at: 2026-08-17T17:26:23+00:00
cwd: /Users/wooojin/App/openaigame
rollout_path: /Users/wooojin/.codex/archived_sessions/rollout-2026-08-18T02-25-52-01a010c2-1fc1-7060-82f6-5f8df8d6bc42.jsonl
rollout_summary_file: 2026-08-17T17-25-52-x82e-independent_airborne_scene_comparison_incomplete.md

---
description: Independent airborne scene A/B comparison was only initiated; protocol was read, but required inputs and output were not completed. Preserve strict isolation, file-scope, and qualitative-analysis constraints for continuation.
task: independent airborne scene A/B comparison
 task_group: /Users/wooojin/App/openaigame scene comparison workflow
task_outcome: partial
cwd: /Users/wooojin/App/openaigame
keywords: scene-comparison-protocol, airborne-scenes, Opus-5, independent-analysis, scene-comparison-opus-5-high.md, speedwing, glider, flight-grammar
---

### Task 1: Independent airborne scene comparison

task: Analyze A안 「거대한 매달린 형태」 versus B안 「듬성듬성한 스카이라인」 independently under the scene comparison protocol.
task_group: airborne scene comparison
 task_outcome: partial

Preference signals:
- The user required no cross-session contamination: do not find, read, or mention other analysis sessions or their outputs. Future independent analyses should preserve strict context isolation.
- The user required the sole artifact to be `/Users/wooojin/App/openaigame/docs/reviews/scene-comparison-opus-5-high.md` and said to write directly there. Avoid edits elsewhere.
- The user prohibited coordinates, pixel quantities, block maps, structure diagrams, and code output; keep the result qualitative and scene-focused.

Reusable knowledge:
- The protocol is at `/Users/wooojin/App/openaigame/docs/28-scene-comparison-protocol.md` and mandates reading the common packet in order: `START_HERE.md` + `DECISIONS.md`; `docs/14-execution-gates.md`; `HANDOFF.md` stage 3; `docs/23-measured-balance-patch.md`; `docs/20-growth-branch-decision.md`; `docs/21-concrete-scene-table.md`; `docs/frame/raw-brief-growth-branch.md`; `experiments/speed-feedback-v1/`; then `docs/24`, `docs/25` for reusable scene material only.
- Required fixed output sections are five sections for each A/B option, then `## 판정`, then `## 이 판정을 뒤집을 수 있는 것`.
- The verdict must use measured physics and the flight grammar `급강하→속도→상승→활공`; preference-only reasoning is insufficient.
- The protocol distinguishes `[검증]` from `[예상]` equipment behavior, and requires stating which expected result from the four-combination validation flight would change the verdict.

Failures and how to do differently:
- The rollout stopped after reading the protocol. The required input packet was not read and the designated Markdown output was not created. Continue from the protocol, respecting the exact order and restrictions; do not claim completion without confirming the file exists.

References:
- Protocol command used: `cat /Users/wooojin/App/openaigame/docs/28-scene-comparison-protocol.md`
- Protocol status: `READY — 미실행`
- Sole output path: `/Users/wooojin/App/openaigame/docs/reviews/scene-comparison-opus-5-high.md`

## Thread `01a01218-e960-74f1-bdc9-b2aca428d6c9`
updated_at: 2026-08-20T10:14:19+00:00
cwd: /Users/wooojin
rollout_path: /Users/wooojin/.codex/sessions/2026/08/18/rollout-2026-08-18T08-40-17-01a01218-e960-74f1-bdc9-b2aca428d6c9.jsonl
rollout_summary_file: 2026-08-17T23-40-17-o5At-openaigame_doc_routing_and_dumbfire_research.md

---
description: OpenAI Game 문서 입구를 단일화하고 장기 설계 자료를 보존했으며, Dumbfire Instagram 사례 조사에서 재사용할 브라우저/Grok 절차와 조사 한계를 확인함
 task: openaigame 문서 라우팅 정리 및 Dumbfire 사례 조사
task_group: /Users/wooojin/App/openaigame
 task_outcome: partial
cwd: /Users/wooojin/App/openaigame
keywords: OpenAI Game, START_HERE, AGENTS.md, CLAUDE.md, DECISIONS.md, HANDOFF.md, docs/14, docs/28, Dumbfire, Instagram, aside-browser, browser-cli, grok-4.6, adapter_eof
---

### Task 1: 대표 문서 라우팅 정리

task: Claude/Codex가 OpenAI Game에서 중복 없이 현재 작업과 장기 설계를 구분하도록 대표 문서를 정리
task_group: openaigame 문서 운영
task_outcome: success

Preference signals:
- 사용자가 “대표 문서들만 최적화하고 통합”하길 원했고 큰 맥락 계획은 보존하길 확인함 -> 입구를 짧게 만들되 기존 설계 자료를 삭제하거나 폴더 재분류하지 않는다.
- `cs sub`로 Opus 5 High와 논의 후 수정하길 요청함 -> 중요한 구조 결정은 독립 검토를 참고하되 메인 세션이 최종 통합한다.

Reusable knowledge:
- 새 세션 최소 읽기 경로는 `START_HERE.md` → `AGENTS.md` → `DECISIONS.md` → `docs/14` §0·§4 → `docs/28-scene-comparison-protocol.md`.
- 파일 역할: `START_HERE`=현재 단계/읽기 라우팅, `AGENTS.md`=고정 규약, `DECISIONS.md`=append-only 이력, `docs/14`=허용·금지 게이트, `docs/28`=A/B 비교 절차·입력 패킷, `HANDOFF.md`=닫힌 세션 기록, `CLAUDE.md`=AGENTS 포인터.
- 장기 설계·감성 자료는 `docs/08`, `docs/10`, `docs/11`, `docs/19`, `docs/20`, `docs/21`, `docs/frame/raw-brief-*`에 보존된다. 대부분 `DRAFT`/구현 허가 아님이다.
- 프로젝트에는 Git 저장소가 없어 커밋 검증은 불가능하다.

Failures and how to do differently:
- `apply_patch`는 형식 오류로 실패했으므로 Python 파일 쓰기로 전환했다.
- 긴 `cs sub` 호출은 stdout이 비어도 프로세스·출력 파일(`/tmp/openaigame-doc-opt/opus-response.md`)을 확인해 실제 응답 여부를 판단한다.

References:
- `/Users/wooojin/App/openaigame/START_HERE.md`
- `/Users/wooojin/App/openaigame/AGENTS.md`
- `/Users/wooojin/App/openaigame/CLAUDE.md`
- `/Users/wooojin/App/openaigame/HANDOFF.md`
- `/Users/wooojin/App/openaigame/docs/14-execution-gates.md`
- `/Users/wooojin/App/openaigame/docs/28-scene-comparison-protocol.md`
- `cs sub --model opus --effort high -p ...`

### Task 2: Dumbfire Instagram 사례 조사

task: 공개 Instagram 릴스·댓글과 공식 Steam 자료를 조사해 Dumbfire의 주목 원리와 OpenAI Game에 옮길 수 없는 표면 요소를 분리
 task_group: 외부 게임 사례 리서치
 task_outcome: partial

Preference signals:
- 사용자는 Dumbfire를 우리와 같은 계열로 억지 비교하지 말고 “이목을 끈 로켓 게임 사례”로 조사하길 원함 -> 유사 장르 판단보다 훅·반응·전이 가능한 원리를 분리한다.
- 댓글은 즉시 기능 백로그로 만들지 말고 감탄, 숙련 욕망, 플레이/구매 신호, 확장 상상, 혼선으로 분류한다.
- 공개 자료만 읽고 좋아요/팔로우/댓글/메시지 등 외부 상태 변경은 하지 않는다.

Reusable knowledge:
- 직접 관찰한 릴스: `DcJ3LTtJ7rs` 그래플(약 8.7천 좋아요/234댓글), `DbdcYQYJUYQ` 정확도(약 4.3천/141), `DbQy_Bgpi6b` 멀티 타깃(약 1.3만/235), `DboFffGp8Z6` 업데이트 조작(약 3.5천/129).
- 반복 댓글: 조작 감탄, 지글 물리·그래플 반응, TAS/타임트라이얼, demo/release 요구, Mac·모바일·Xbox, sandbox/custom maps/level editor/Workshop, POV/fixed camera/FPV 조작 질문.
- Dumbfire의 조사 가치는 “짧은 클립에서 물리 한 줄과 성공/실패가 읽히면 관객이 숙련을 상상하는가”를 보는 사례라는 점이다. 그래플·3D 장애물·군사 톤·밈을 복사하지 않는다.
- Steam/itch의 제품 루프는 발사 → 운동량·기수 조작 → 좁은 코스/타깃 통과·격파 → 기록/별 → 즉시 재시작으로 요약되며, 우리 OpenAI Game의 급강하→속도→상승→활공과는 다르다. 위시리스트·판매량·전환율은 확인되지 않았다.

Failures and how to do differently:
- Aside 조사에서 `page.waitForTimeout is not a function`, 잘못된 `:has-text` selector, REPL 스코프 오류, `adapter_eof`가 발생했다. `sleep()`과 fresh snapshot을 사용하고 릴스 표본을 나눠 조사한다.
- Grok 4.6 High는 웹 탐색만 반복하고 최종 응답이 늦었다. 리서치 범위·최대 턴을 좁히고 충분한 증거가 모이면 추가 검색 없이 결론을 닫는다.
- 이번 Grok 응답은 롤아웃 종료 시점에 완전히 회수되지 않았으므로, 최종 보고서에서 직접 관찰·공식 확인·Grok 해석을 각각 표시한다.
- `.codex` 전체를 넓게 `rg`하지 않는다. 프로젝트 경로와 명시적 glob만 검색한다.

References:
- `https://www.instagram.com/dumbfiregame?igsh=dXBnd25yMmplcm5z`
- `https://www.instagram.com/dumbfiregame/reel/DcJ3LTtJ7rs/`
- `https://www.instagram.com/dumbfiregame/reel/DbdcYQYJUYQ/`
- `https://www.instagram.com/dumbfiregame/reel/DbQy_Bgpi6b/`
- `https://www.instagram.com/dumbfiregame/reel/DboFffGp8Z6/`
- `https://store.steampowered.com/app/4944600/Dumbfire`
- `grok --model grok-4.6 --reasoning-effort high --permission-mode bypassPermissions --no-subagents --max-turns 12 ...`
- Grok session: `/Users/wooojin/.grok/sessions/%2FUsers%2Fwooojin%2FApp%2Fopenaigame/01a018bf-6ab3-7ec3-b108-df076b2e7025/events.jsonl`

## Thread `01a01240-6ac7-7db1-8c62-4dcdf522026c`
updated_at: 2026-08-18T01:32:38+00:00
cwd: /Users/wooojin
rollout_path: /Users/wooojin/.codex/sessions/2026/08/18/rollout-2026-08-18T09-23-26-01a01240-6ac7-7db1-8c62-4dcdf522026c.jsonl
rollout_summary_file: 2026-08-18T00-23-26-kfik-career_research_internships_baekseok_contests_context_transf.md

---
description: 취업 가능성 조사와 백석대 공모전·재학생 인턴 탐색을 통해 사용자 선호, 검증 기준, 공모전 참가 전략, 컨텍스트 이전 형식을 확인함
task: career-research-and-context-transfer
task_group: /Users/wooojin 취업·공모전·사용자 메모리
 task_outcome: partial
cwd: /Users/wooojin
keywords: 카카오뱅크, 재학생-인턴, 백석대, Smart-IT, Hacking-Festival, JAVA-경진대회, Codex-토큰, Aside, 컨텍스트-이전, 원문-검증
---

### Task 1: 카카오뱅크 자격 및 휴학 판단

task: 카카오뱅크 AI Native 서비스 기획자 채용연계형 인턴의 재학·휴학 지원 가능성 확인
task_group: 취업 자격 검증
task_outcome: success

Preference signals:
- 사용자가 “지원 버튼은 절대 누르지 마”라고 반복함 -> 채용 조사는 읽기와 검증만 수행하고 지원·제출은 하지 않는다.
- 사용자가 “원문 근거로만 판정”을 요구함 -> 공식 공고와 로컬 학점 자료를 분리해 제시한다.

Reusable knowledge:
- 공식 공고 `https://recruit.kakaobank.com/jobs/263159`는 `기졸업자 또는 졸업 요건을 모두 갖춘 수료자`만 허용하고, `수업(온라인 포함), 시험 등 인턴 기간 중 학업 병행이 필요한 분은 지원이 불가합니다.`라고 명시했다.
- 로컬 이수 현황은 120학점 중 84.5학점 취득, 35.5학점 부족, 전공 54학점 중 33학점 취득이었다. 휴학은 이 수료 요건을 충족시키지 않으므로 공고 자격 우회 수단이 아니다.

Failures and how to do differently:
- LinkedIn 원본 URL이 깨져 `페이지 없음`이 나왔고 `kr.linkedin.com` 링크로 재탐색했다.
- Aside REPL에서 stale ref와 중복 `const` 선언이 반복됐다. 매 액션 후 새 snapshot과 새 변수명을 사용한다.

References:
- `/Users/wooojin/Downloads/2022학년도 입학자 졸업소요 취득학점.xlsx`
- `https://recruit.kakaobank.com/jobs/263159`

### Task 2: 재학생 인턴 대안 조사

task: 2026-08-18 기준 재학생 지원 가능 인턴과 주요 기업 채용 현황 탐색
task_group: 재학생 취업 탐색
task_outcome: partial

Preference signals:
- 사용자가 “많이많이 찾아줘”라고 요청한 뒤 실제 열린 공고만 원문으로 재검증하는 방향을 수용함 -> 넓은 후보 수집 후 현재 열림·마감·시즌 추정을 분리한다.

Reusable knowledge:
- 딥오토 AI Engineer: `재학/휴학/졸업생 모두 가능`, `https://www.wanted.co.kr/wd/379363`.
- 피치에이아이 AI/ML Engineer: `방학 중인 재학생, 휴학생, 졸업예정자 또는 기졸업자`, 학기 수업 병행 불가, `https://www.wanted.co.kr/wd/376376`.
- 카카오뱅크 AI 운영 어시스턴트와 대출비교서비스 운영 어시스턴트는 학력 제한보다 6개월 풀타임 조건이 핵심이다: `https://recruit.kakaobank.com/jobs/262683`, `https://recruit.kakaobank.com/jobs/262837`.
- 2026-08-18 확인 결과 네이버는 네이버웹툰 체험형 인턴 1건, 삼성은 인턴 0건, 카카오·우아한형제들·무신사는 진행 인턴 공고가 없었다.

Failures and how to do differently:
- 초기 20개 목록에는 시즌 추정과 원문 미검증 자격이 섞였다. 다음에는 처음부터 `현재 열림 / 마감 / 시즌 추정`을 분리한다.

References:
- `https://www.wanted.co.kr/wd/379363`
- `https://www.wanted.co.kr/wd/376376`
- `https://recruit.kakaobank.com/jobs/262683`

### Task 3: 백석대 교내 공모전 3종 전략

task: Smart IT, Hacking Festival, JAVA 경진대회의 상금·개인 참가·팀 구성·2026-2 일정 예측 확인
task_group: 백석대 교내 공모전
 task_outcome: success

Preference signals:
- 사용자가 “가능하면 1인이 좋은데 안되면 친구 한명까진 ㄱㅊ”이라고 함 -> 개인 참가를 우선하고 2인 구성을 대안으로 제시한다.
- 사용자가 “현실적으로 내가 그렇게 3개정도 한다면”이라고 범위를 좁힘 -> 대회별 상금, 참가 형태, 일정, 노력 배분을 함께 비교한다.

Reusable knowledge:
- Smart IT: 개인 또는 5인 이내 팀, 대상 100만 원, 금상 60만 원, 은상 40만 원, 동상 20만 원, 장려상 10만 원. `https://community.bu.ac.kr/info/1788/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGaW5mbyUyRjg5NyUyRjUyNjYxJTJGYXJ0Y2xWaWV3LmRv`
- Hacking Festival: 백석대 재학생, 팀 단위 시상, 대상 50만 원, 금상 40만 원, 은상 20만 원, 장려상 10만 원. 본문에 1인 금지나 팀 인원 제한은 없었다. `https://community.bu.ac.kr/info/1788/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGaW5mbyUyRjg5NyUyRjUxNjk4JTJGYXJ0Y2xWaWV3LmRv`
- JAVA: 개인 온라인 문제풀이, 대상 20만 원, 금상 15만 원, 은상 10만 원, 동상 5만 원. 친구 불필요. `https://community.bu.ac.kr/info/1788/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGaW5mbyUyRjg5NyUyRjUxNzAzJTJGYXJ0Y2xWaWV3LmRv`
- 과거 공지 월 기반 추정: Smart IT 9~11월, Hacking Festival 9~10월, JAVA 10~11월 모집 및 12월 진행. 2026 공고 확정 사실은 아니다.
- 제안된 노력 배분은 Smart IT 70%, Hacking Festival 20%, JAVA 10%이며, Smart IT는 혼자 또는 2인, Hacking Festival은 친구 1명, JAVA는 혼자 하는 구성이 사용자 조건에 맞는다.

Failures and how to do differently:
- 게시판 검색에서 잘못된 selector와 접근 불가 URL이 반복됐다. 검색 결과에서 정확한 게시물 href를 먼저 추출한 뒤 직접 연다.

References:
- Smart IT 원문: `신청대상 : 컴퓨터공학부 재학생(개인 또는 5인 이내 팀/ 타학부 참여 가능)`
- JAVA 원문: `참여대상 : 백석대학교 재학생`

### Task 4: 토큰 사용량·비용 설명

task: 대규모 브라우저 조사에 사용된 토큰과 비용의 대략적 의미 설명
task_group: Codex 사용량
 task_outcome: success

Preference signals:
- 사용자가 조사 뒤 “토큰 얼마나 써?”를 별도로 물음 -> 대규모 조사 전 범위와 예상 사용량을 먼저 설명하는 것이 유용하다.

Reusable knowledge:
- 공식 문서상 GPT-5.4 API는 입력 1M 토큰 $2.50, 캐시 입력 $0.25, 출력 $15.00이다.
- Codex 정액제는 직접 API 청구가 아니라 플랜별 사용량 한도·크레딧으로 소비된다.
- 정확한 이번 세션 사용량은 확인되지 않았으므로 입력 80만~150만, 출력 8만~15만 토큰은 추정치로만 취급한다.
- 다음 대규모 조사에서는 `현재 열린 것만 10개`, `백석대 교내만`처럼 범위를 선제적으로 줄인다.

References:
- `https://learn.chatgpt.com/docs/pricing.md`
- `https://developers.openai.com/api/docs/pricing.md`

### Task 5: 컨텍스트 이전용 사용자 요약 형식

task: 저장 메모리를 다른 AI 어시스턴트로 이전하기 위한 사용자 프로필 요약
task_group: 메모리·컨텍스트 이전
 task_outcome: success

Preference signals:
- 사용자가 “1인칭 대명사와 2인칭 대명사는 사용하지 말아 줘”라고 요청함 -> 이전 문서에서는 ‘사용자’와 중립 표현만 사용한다.
- 사용자가 “특히 요청 사항 및 선호 사항의 경우에 해당 사용자의 문구를 그대로 유지해 줘”라고 요청함 -> 규칙과 선호는 가능한 한 원문 인용을 유지한다.
- 사용자가 “저장된 메모리에 있는 규칙만 포함해야 해”라고 요청함 -> 임시 대화 내용과 추론을 저장 규칙으로 승격하지 않는다.
- 사용자가 마지막 텍스트를 `가져온 위치: <name>`으로 고정함 -> 지정된 카테고리 순서와 마지막 문구를 보존한다.

Reusable knowledge:
- 메모리 요약 카테고리 순서: 인구통계 정보, 관심분야 및 선호 사항, 인간관계, 날짜가 지정된 이벤트·프로젝트·계획, 요청 사항.
- 사용자 선호: 한국어 존댓말, 결과 먼저·원인 다음, 짧고 쉬운 문장, 실제 파일·live state·정확한 오류·검증 증거 중심.
- 본인 명의 취업 글: 담백한 평서문, 수치 근거, 가운뎃점과 과장된 격언조 회피.

Failures and how to do differently:
- 최종 요약에는 Aside 메모리의 민감한 개인정보까지 포함될 위험이 있었다. 향후 컨텍스트 이전용 요약에서는 사용자가 명시적으로 요청한 범위에 필요한 정보만 포함하고, 이메일·전화번호·주소·토큰 등은 불필요하면 제외한다.

References:
- `/Users/wooojin/.codex/memories/MEMORY.md`
- `/Users/wooojin/.codex/memories/memory_summary.md`
- `/Users/wooojin/.aside/u/0/memory/users/jung-woojin.md`

## Thread `01a01eac-0c17-76a0-80b8-cba135b66726`
updated_at: 2026-08-20T12:32:54+00:00
cwd: /Users/wooojin
rollout_path: /Users/wooojin/.codex/sessions/2026/08/20/rollout-2026-08-20T19-16-26-01a01eac-0c17-76a0-80b8-cba135b66726.jsonl
rollout_summary_file: 2026-08-20T10-16-26-Z7ls-aside_grok_research_routing.md

---
description: Sol이 최종 작업·비교를 맡고 Consult/Grok/Aside를 최소 호출로 라우팅하는 환경을 구축했으며, Grok은 Aside의 로그인 브라우저에서 reversible 탐색과 정확한 클릭까지 직접 수행하도록 설정됨
 task: research-browser-router-and-aside-grok-execution
 task_group: cross-session research workflow
 task_outcome: success
 cwd: /Users/wooojin
 keywords: research-browser-router, run_grok_research.py, consult, run_aside_consult.py, Aside, xai-grok-oauth, grok-4.6, GPT-5.6-Sol, MCP, browser tabs
---

### Task 1: 경량 리서치 라우팅 및 Grok+Aside 실행

task: 자동 리서치 라우팅, Consult Aside 백엔드, Grok Aside 브라우저 실행기 구축
task_group: cross-session research workflow
task_outcome: success

Preference signals:
- 사용자는 “Sol이 작업 및 비교, 에이전트로 Grok이 경매장 Aside 브라우저에서 탐색”하는 구조를 원한다 -> Sol은 브라우저를 직접 따라가지 말고 compact report를 받아 최종 비교·판결만 한다.
- 공개 웹에는 Consult도 포함하고, “정확한 클릭같은 것도 알아서 에이전트가 끝내게” 하며 Sol 토큰을 아끼길 원한다 -> Consult는 좁은 공개 판단, Grok은 넓은 공개·로그인 브라우저 탐색으로 라우팅한다.
- “별도 grok-aside-research 스킬은 없는 게 낫다”, “그록 실행기까지만”을 요청했다 -> 별도 중복 스킬·공용 라이브러리·자동 체이닝 없이 라우터와 두 실행기만 유지한다.

Reusable knowledge:
- `research-browser-router`는 implicit invocation이 켜져 있어 “리서치해줘”, “최신 자료 확인”, “로그인 페이지 확인” 요청에서 먼저 로드되지만, 로컬 근거로 충분하면 외부 호출을 생략한다.
- Grok native Aside 설정은 `provider=xai-grok-oauth`, `model=grok-4.6`, `effort=high`다. `xai/grok-4.6`은 실패한다.
- `/Users/wooojin/.codex/skills/research-browser-router/scripts/run_grok_research.py`는 Aside native Grok agent를 호출하고, 공개 웹·로그인 브라우저의 reversible 작업을 수행하게 한다. 페이지/액션/시간 예산, 구조화 보고서, 부분 결과, process-group cleanup, task-tab cleanup을 담당한다.
- Grok report는 `직접 관찰`, `공식 확인`, `해석`, `미확인`, `브라우저 작업`, `상태 변경`, `승인 필요`를 포함한다. Sol은 성공 시 `grok-report.md`와 compact `grok-run.json`만 읽고 raw logs는 실패·모순 때만 읽는다.
- 구매·제출·삭제·메시지·계정/보안 변경은 explicit approval 없이는 실행하지 않는다. 검색·필터·상세 열기·정확한 클릭·읽기 전용 다운로드는 Grok이 끝낸다.
- `/Users/wooojin/.codex/skills/consult/scripts/run_aside_consult.py`는 ChatGPT Pro의 `GPT-5.6 Sol + 매우 높음` quick 및 `GPT-5.6 Sol + Pro` deep을 검증하고, 패킷 업로드·응답 저장·대화 URL·작업 탭 정리를 수행한다.
- Consult 모델 선택이 검증되지 않으면 fail-closed한다. Aside ChatGPT UI의 contenteditable 입력에는 `click()` 후 `keyboard.insertText()`를 사용한다.

Failures and how to do differently:
- 초기 Grok runner가 WebSearch/WebFetch만 허용해 로그인 경매장을 다루지 못했다. 로그인 웹의 넓은 탐색은 Grok+Aside runner로 보내야 한다.
- `aside exec`에서 잘못된 provider ID를 쓰면 “Requested model ... not available”이 난다. Aside 모델 카탈로그에서 provider를 확인하고 `xai-grok-oauth`를 사용한다.
- 진행 중인 다른 세션은 환경 변경을 자동으로 재로드하지 않는다. 라우터·실행기 변경 후에는 해당 thread에 짧은 follow-up을 보내고 이미 완료한 작업은 반복하지 않는다.
- Grok native Wikipedia 클릭 검증은 성공했다: 기존 Maple Auction/메이플 가이드 탭 보존, 새 Wikipedia 탭 생성·English 클릭·`en.wikipedia.org` 확인·작업 탭 종료, `orphanCheck=gone`.

References:
- `/Users/wooojin/.codex/skills/research-browser-router/SKILL.md`
- `/Users/wooojin/.codex/skills/research-browser-router/scripts/run_grok_research.py`
- `/Users/wooojin/.codex/skills/consult/SKILL.md`
- `/Users/wooojin/.codex/skills/consult/scripts/run_aside_consult.py`
- Successful pilot: `/Users/wooojin/dev/maple/.research/aside-native-grok-click/grok-run.json`
- Successful report: `/Users/wooojin/dev/maple/.research/aside-native-grok-click/grok-report.md`
- Verified model catalog entry: `~/.aside/u/0/models.json` provider key `xai-grok-oauth`, model `grok-4.6`

## Thread `01a01f5c-e998-7b62-96fb-5484a42b5beb`
updated_at: 2026-08-20T13:32:41+00:00
cwd: /Users/wooojin
rollout_path: /Users/wooojin/.codex/sessions/2026/08/20/rollout-2026-08-20T22-29-37-01a01f5c-e998-7b62-96fb-5484a42b5beb.jsonl
rollout_summary_file: 2026-08-20T13-29-37-oMyf-fix_aside_rg_macos_security_warning.md

description: Resolved recurring macOS security warning caused by Aside's quarantined bundled rg; replaced it with verified Homebrew ripgrep and confirmed searches run without new warnings.
task: eliminate recurring Aside rg security popup
 task_group: macos-desktop-troubleshooting
 task_outcome: success
cwd: /Users/wooojin
keywords: macOS, Aside, rg, ripgrep, quarantine, com.apple.quarantine, spctl, syspolicyd, CoreServicesUIAgent, xattr

### Task 1: Replace Aside's blocked rg

task: stop repeated macOS warning from Aside's bundled ripgrep
task_group: macOS desktop troubleshooting
task_outcome: success

Preference signals:
- When the warning kept appearing, the user said: "이것좀 그만 뜨게해봐!!!!!!!!!!" -> prioritize removing the recurring root cause, not merely dismissing the current dialog, and report concise verification.

Reusable knowledge:
- Aside's problematic executable was `/Users/wooojin/.aside/runtime/native/bin/rg`; it had quarantine/provenance metadata and `/usr/sbin/spctl` reported it as rejected.
- The process was invoked by Aside and could hang while macOS security services repeatedly evaluated it.
- The working fix was to preserve the original as `/Users/wooojin/.aside/runtime/native/bin/rg.blocked-original-20260820` and symlink the original path to `/opt/homebrew/bin/rg`.
- The replacement reported `ripgrep 15.1.0`; an actual search completed, no new security warning was logged, and CoreServicesUIAgent had zero windows.

Failures and how to do differently:
- Use `/usr/sbin/spctl`, not `/usr/bin/spctl`, on this macOS environment.
- Removing xattrs alone was insufficiently durable; replacing the quarantined bundled binary with the trusted Homebrew binary stopped the warning. Recheck after Aside updates because updates may restore the bundled file.

References:
- `/Users/wooojin/.aside/runtime/native/bin/rg`
- `/opt/homebrew/bin/rg`
- `/Users/wooojin/.aside/runtime/native/bin/rg.blocked-original-20260820`
- `xattr -l <path>`
- `/usr/sbin/spctl --assess --type execute --verbose=4 <path>`
- `log show --predicate '(process == "syspolicyd" OR process == "CoreServicesUIAgent") ...'`

## Thread `01a022f5-a89b-7671-978c-f79906f9abdd`
updated_at: 2026-08-21T06:22:00+00:00
cwd: /Users/wooojin
rollout_path: /Users/wooojin/.codex/sessions/2026/08/21/rollout-2026-08-21T15-15-19-01a022f5-a89b-7671-978c-f79906f9abdd.jsonl
rollout_summary_file: 2026-08-21T06-15-19-V1Kd-karabiner_rollback_fixes_varmilo_shortcuts.md

description: Karabiner의 최근 Varmilo 키 변환 규칙 때문에 한영, Rectangle, ⌘⇧3 캡처가 모두 깨졌으나 8월 16일 백업으로 롤백해 해결함
 task: karabiner-varmilo-shortcut-rollback
 task_group: macos-keyboard-configuration
 task_outcome: success
 cwd: /Users/wooojin
 keywords: Karabiner, Varmilo, Rectangle, 한영, keyboard_fn, apple_vendor_top_case_key_code, ⌘⇧3, automatic_backups, rollback

### Task 1: Karabiner 설정 롤백

task: 최근 Varmilo 규칙 변경으로 망가진 macOS 단축키 복구
task_group: macos-keyboard-configuration
task_outcome: success

Preference signals:
- 사용자가 “며칠 전으로 돌릴 수 없나?”라고 요청함 -> 새 규칙을 즉시 추가하기보다 가장 가까운 정상 백업으로 복구하는 접근을 우선할 것.
- 사용자는 복구 후 한영 전환, `⌘⇧3`, Rectangle 단축키를 직접 확인했고 “다 된다”고 확인함 -> 유사한 키보드 복구에서는 이 세 가지를 최소 검증 목록으로 사용할 것.
- 사용자는 EventViewer의 실제 Varmilo 키값을 기준으로 최소 수정하는 후속 작업을 수용할 수 있음 -> 물리 입력을 추정하지 말고 이벤트 확인 후 장치별 규칙을 추가할 것.

Reusable knowledge:
- 설정 파일은 `/Users/wooojin/.config/karabiner/karabiner.json`, 백업은 `/Users/wooojin/.config/karabiner/automatic_backups/`에 있음.
- 현재 문제가 생긴 설정에는 Varmilo 장치(`vendor_id: 1241`, `product_id: 41169`)에 대해 Ctrl, left_command, Caps를 서로 여러 방향으로 변환하는 규칙이 겹쳐 있었다. 이 규칙들이 Command 조합과 한영/Rectangle을 연쇄적으로 깨뜨린 원인으로 추정됨.
- 복구에 사용한 백업은 `karabiner_20260820-161923-before-moonlight-except.json`이며, 내용상 최근 Varmilo 수정 전의 8월 16일 상태다.
- 롤백 전 현재 설정은 `karabiner_20260821-152022-before-rollback-to-20260816.json`으로 별도 보존됨.
- 복구 후 SHA-256은 소스 백업과 현재 파일이 동일했고, `jq` JSON 검사, `Default profile`, Karabiner 프로세스 및 CLI 상태가 정상이었다.

Failures and how to do differently:
- 최근 Varmilo 전용 규칙은 같은 물리 키를 여러 변환 규칙이 다시 매핑하는 구조였음. 향후에는 먼저 현재 설정을 백업하고, EventViewer의 실제 키 이벤트와 장치 식별자를 확인한 뒤 최소한의 단일 변환만 추가할 것.
- `⌘⇧3` 문제는 macOS 캡처 symbolic hotkey 비활성화보다 Command 변환 이상과 관련된 것으로 확인됨. 캡처 설정을 먼저 변경하지 말고 Karabiner의 Command/Fn 변환부터 점검할 것.

References:
- `/Users/wooojin/.config/karabiner/karabiner.json`
- `/Users/wooojin/.config/karabiner/automatic_backups/karabiner_20260820-161923-before-moonlight-except.json`
- `/Users/wooojin/.config/karabiner/automatic_backups/karabiner_20260821-152022-before-rollback-to-20260816.json`
- 관련 이벤트 키 문자열: `apple_vendor_top_case_key_code`, `keyboard_fn`
- 최종 검증: 사용자가 “다 된다”라고 확인함.

## Thread `01a024a9-c89d-7ef3-84eb-d0ecf22a31ca`
updated_at: 2026-08-21T16:55:15+00:00
cwd: /
rollout_path: /Users/wooojin/.codex/sessions/2026/08/21/rollout-2026-08-21T23-11-41-01a024a9-c89d-7ef3-84eb-d0ecf22a31ca.jsonl
rollout_summary_file: 2026-08-21T14-11-41-Xjho-aerial_world_lab_comparison_build.md

---
description: Built an isolated three-preset aerial-world comparison lab from an approved brief; static checks and headless browser interaction passed, while user first-impression flight and final world selection remain unverified.
task: implement-approved-aerial-world-comparison-lab
task_group: openaigame-aerial-world-implementation
 task_outcome: partial
cwd: /Users/wooojin/App/openaigame
keywords: aerial-world-lab, WORLD_PRESETS, world-presets.js, presetId, sceneId, world_first_impression, flightTime, collisionShapes, V-key, headless-Chrome, CDP, node-check
---

### Task 1: Implement and verify isolated aerial-world comparison lab

task: implement-approved-aerial-world-comparison-lab
task_group: /Users/wooojin/App/openaigame
 task_outcome: partial

Preference signals:
- The user explicitly required writes only under `experiments/aerial-world-lab/**` and said not to modify the baseline, docs, or use commit/reset/clean/revert -> keep future implementation strictly scoped and report conflicts rather than broadening.
- The user required actual browser interaction and a report separating changed files, checks, browser-confirmed items, and unverified items -> preserve this verification/reporting structure.

Reusable knowledge:
- Approved brief hash: `2a8a82fc1454213f54bd88a881a6974dc1e1a133f2dd81ef61488c02624cb0cf`.
- Lab files: `experiments/aerial-world-lab/{README.md,game.js,index.html,telemetry.js,world-presets.js}`.
- `WORLD_PRESETS` owns world placement. Rendering and collision generation consume the same form parts; forms include `layer`, `collide`, material, `assetKey`, and optional deterministic motion.
- Presets are A/Grok, B/Fable, C/Sol. `V` cycles only while on the bench; `R` resets the current world/equipment. Telemetry uses `aerial-world-lab-flight-telemetry-v1` and records `presetId`, `sceneId`, per-flight environment, and `world_first_impression`.
- Static checks passed: `node --check` for all three JS files. Baseline `speed-feedback-v1` hashes and approved `docs/31` hash remained unchanged.
- Headless Chrome confirmed `J` inspection blocks `V`, bench cycling `A→B→C→A`, equipment preservation across switching, state reset, telemetry tagging, and collision counts matching form parts: A 12, B 10, C 14.
- B’s moving collision form is derived from `flightTime`: offset zero at `flightTime=0`, approximately `{x:560,y:49.497}` at `2.125` seconds.

Failures and how to do differently:
- Large inline patches repeatedly failed from nested backticks/template strings. Use small file-based scripts or correctly formatted patches and run syntax checks incrementally.
- CDP/browser runs encountered stale cache and short-lived processes. Start a fresh target, cache-bust script URLs, and assert `typeof window.game.getPreset === 'function'` before interaction.
- Screenshot verification initially captured stale/start-like frames; force an exposed lab-only render after camera mutation.
- Existing old telemetry storage was observed in the browser, so report “new key is isolated” rather than claiming the old key is absent.
- User first-impression flights, A→B→C and reverse comparison, and final world selection were not performed; do not mark the comparison decision complete.

References:
- Brief: `/Users/wooojin/App/openaigame/docs/31-aerial-world-playable-comparison-implementation-brief.md`
- Run: `cd /Users/wooojin/App/openaigame/experiments/aerial-world-lab && python3 -m http.server 8654`
- Verification handles: `WORLD_PRESETS`, `window.game.getPreset()`, `window.game.collisionShapes()`, localStorage key `aerial-world-lab-flight-telemetry-v1`.
- Hook note: local `codex-native-hook.js` Stop invocation returned exit code 0 and stdout `{}`; repeated hook prompts were infrastructure behavior, not implementation blockers.

## Thread `01a024a9-cb4b-7851-bf7d-6b80ef0f140b`
updated_at: 2026-08-21T14:15:36+00:00
cwd: /Users/wooojin/App/openaigame
rollout_path: /Users/wooojin/.codex/sessions/2026/08/21/rollout-2026-08-21T23-11-42-01a024a9-cb4b-7851-bf7d-6b80ef0f140b.jsonl
rollout_summary_file: 2026-08-21T14-11-42-qFpV-independent_aerial_world_sol_medium_structure_exploration.md

---
description: A안의 단일 공중 월드 비전을 지정 문서에 작성하고 검증함; 강한 하나의 세계에 베팅하며 코드·기존 문서는 건드리지 않는 작업 방식이 확인됨
task: write-independent-aerial-world-structure-proposal
task_group: openaigame-world-design
task_outcome: success
cwd: /Users/wooojin/App/openaigame
keywords: aerial-world, world-structure, aerial-world-sol-medium, docs-29, speed-wing, glide-wing, open-air, blockout, collision-outline
---

### Task 1: A안 공중 월드 구조 제안

task: write-independent-aerial-world-structure-proposal
task_group: openaigame-world-design
task_outcome: success

Preference signals:
- 사용자가 “구조 유형을 미리 분류하지 말고”, “안전한 평균안 대신 하나의 응집된 월드 비전에 베팅하세요”라고 요청함 -> 유사한 창작 설계에서는 대안 목록보다 하나의 강한 비전, 트레이드오프, 폐기 기준을 제시한다.
- 사용자가 “지정된 산출물 파일 하나만 작성”하고 완료 후 “그 파일 경로만 짧게 보고”라고 요청함 -> 명시된 산출물 범위를 넘지 않고 최종 보고도 최소화한다.
- 브리프가 `압도적이지만 자유로운 거대한 놀이방 70 / 근접 비행 긴장 30`을 고정함 -> 거대한 형태 사이의 열린 공중을 중심으로 설계하고 연속 코스·촘촘한 장애물로 변질시키지 않는다.

Reusable knowledge:
- 작성된 세계는 “창가로 항해하는 미완성 하늘배”: 아이 방 전체의 선체·갈비뼈·돛·추·선수가 하나의 거대한 천장 배를 이루지만, 플레이어는 표면이 아니라 부품 사이 열린 공중을 자기 궤적으로 연결한다.
- 속도날개는 선체 안쪽의 낮고 깊은 진입 뒤 늦은 상승을 택하고, 활공날개는 전진 속도를 남긴 긴 바깥 상승과 높은 활공을 택한다. 두 경로는 주돛 앞에서 갈라지고 넓은 공간에서 다시 합류한다.
- 블록아웃 데이터는 공간 기준점, 비행층, 충돌 외곽, 교체 자산, 움직임 역할, 소리 역할, 랜드마크 가림/노출을 분리해야 최종 아트 교체 때 구조를 재작성하지 않는다.
- 폐기 기준: 두 날개가 같은 선을 택함, 활공 윗길이 대가 없는 안전선이 됨, 플레이어가 먼 목표보다 작은 틈 암기에 집중함, 속도 II에서 보기 전에 충돌함.

Failures and how to do differently:
- `git status --short`는 `fatal: not a git repository`를 반환했다. 저장소 여부를 전제하지 말고 대상 파일 존재와 내용 검증을 직접 수행한다.

References:
- 브리프: `docs/29-aerial-world-structure-exploration-brief.md`
- 결과 파일: `/Users/wooojin/App/openaigame/docs/reviews/aerial-world-sol-medium.md`
- 검증 결과: 148줄; 필수 `##` 섹션, 실제 충돌 외곽, 코드 없이 검증할 가설이 확인됨.

## Thread `01a02546-d269-77a2-b0f7-2e3d866d61cc`
updated_at: 2026-08-21T17:50:14+00:00
cwd: /Users/wooojin/App/openaigame
rollout_path: /Users/wooojin/.codex/sessions/2026/08/22/rollout-2026-08-22T02-03-13-01a02546-d269-77a2-b0f7-2e3d866d61cc.jsonl
rollout_summary_file: 2026-08-21T17-03-13-D4yU-aerial_world_lab_implementation_verification.md

description: 승인된 세 월드 비교용 플레이 빌드를 제한된 경로에서 보강하고 브라우저 QA까지 수행했으나 일부 공정성·첫인상 검증은 사용자 몫으로 남은 작업
 task: complete-and-verify-aerial-world-playable-comparison-build
 task_group: openaigame-aerial-world-lab
 task_outcome: partial
 cwd: /Users/wooojin/App/openaigame
 keywords: aerial-world-lab, WORLD_PRESETS, speed-feedback-v1, telemetry, world_first_impression, presetId, sceneId, node-check, agent-browser, V, R, J, F1

### Task 1: 세 월드 비교 빌드 완성 및 검증

task: 승인된 docs/31 구현 브리프에 맞춰 `experiments/aerial-world-lab/**`만 수정하고 실제 브라우저에서 비교 흐름을 검증
 task_group: openaigame-aerial-world-lab
 task_outcome: partial

Preference signals:
- 사용자는 “단독 쓰기 범위는 experiments/aerial-world-lab/** 뿐”이라고 명시했다 -> 유사 작업에서 기준본, docs, START_HERE, 훅/로그를 수정하지 말고 변경 파일을 엄격히 제한해야 한다.
- 사용자는 기존 구현을 믿지 말고 “실제 코드·실행 결과만 기준”으로 직접 점검하라고 했다 -> 자기보고나 이전 세션 로그보다 현재 파일과 실행 증거를 우선한다.
- 사용자는 계획만 보고 멈추지 말고 “실제 브라우저 조작 증거”와 미확인 항목을 구분하라고 했다 -> 렌더·키 입력·콘솔·가독성 검증을 완료 보고에 포함한다.

Reusable knowledge:
- `WORLD_PRESETS`가 월드 배치·구역·형태·레이어·충돌·자산 키를 소유한다. 렌더와 `collisionShapes()`는 동일한 `forms` 배열을 순회한다.
- 충돌 이동은 B의 `rocking-horse` 하나이며 `flightTime`에서 파생된다. 검증 시 `flightTime=2.125`에서 렌더 변환과 collision shape의 x/y가 동일했다.
- 기준본과 lab의 `P` 파라미터 67개가 텍스트·값 모두 동일했고, `WORLD={floor:4200, ceil:-1400, left:20, right:48000}`, `R=13`, 시작점 `(190,886)`도 확인했다. 증거는 `experiments/aerial-world-lab/verify/params-identity.json`.
- 프리셋 전환은 `state.mode === 'bench'`에서만 허용된다. 전환 시 날개·추진기는 보존하고 bestX, attempts, flightLog, 궤적, 파티클, 카메라, barrier 상태, flightTime 등을 초기화한다.
- 텔레메트리 저장 키는 `aerial-world-lab-flight-telemetry-v1`이며 기본 테스트는 `world_first_impression`; configuration/environment와 샘플에 `presetId`, `sceneId`가 포함된다.
- 서버는 `python3 -m http.server 8654`로 `experiments/aerial-world-lab`을 서빙했고 브라우저 URL은 `http://127.0.0.1:8654/`였다.

Failures and how to do differently:
- `apply_patch`가 환경에서 형식 오류로 실패해 Python 치환 스크립트로 전환했다. 이 환경에서는 패치 도구 실패 시 작은 검증 가능한 Python 치환을 사용한다.
- 최초 J 검사 위치가 구역 시작점이라 대표 형태를 비껴갔다. 각 zone에 `inspectX`를 추가하고 `jumpToZone()`이 이를 사용하도록 고쳤다.
- `node --check`는 모두 PASS했고 브라우저 페이지도 로드됐지만, 기준본과 lab의 동일한 짧은 입력에 대한 위치·속도 텔레메트리 재현은 실행하지 않았다. 파라미터 동일성만 확인했으므로 이 항목은 미검증으로 유지한다.
- A→B→C 및 C→B→A를 속도날개 I/활공날개 I로 모두 날리는 첫인상 판정과 속도 II 충돌 전 노출 시간은 수행하지 않았고 사용자 직접 플레이 몫으로 남겼다.
- 작업 중 docs/31과 START_HERE가 다른 세션에서 갱신되어 초기 승인 해시 `2a8a82fc1454213f54bd88a881a6974dc1e1a133f2dd81ef61488c02624cb0cf`와 최종 확인 해시 `7ec1034df70a41143e6afe59994bca3895da3b63a486d483f53a781ea3991996`가 달라졌다. 해당 문서들은 수정하지 않았으며 향후 보고 시 해시 변화를 명시해야 한다.

References:
- `experiments/aerial-world-lab/game.js`
- `experiments/aerial-world-lab/world-presets.js`
- `experiments/aerial-world-lab/telemetry.js`
- `experiments/aerial-world-lab/index.html`
- `experiments/aerial-world-lab/README.md`
- `experiments/aerial-world-lab/verify/params-identity.json`
- Screenshots: `verify/12-A-bones.png`, `verify/14-A-moon.png`, `verify/15-B-horse.png`, `verify/16-C-sail.png`, `verify/13-A-bones-F1.png`, `verify/17-C-sail-F1.png`, `verify/18-B-horse-F1.png`
- Commands: `node --check experiments/aerial-world-lab/game.js && node --check experiments/aerial-world-lab/world-presets.js && node --check experiments/aerial-world-lab/telemetry.js`; `shasum -a 256 docs/31-aerial-world-playable-comparison-implementation-brief.md`
- Browser evidence: title `장난감 세계 로켓 — 세 월드 비교용`; no output from `agent-browser errors` or `console`; actual key checks for `3`, `V`, `R`, `J`, `F1`; browser URL `http://127.0.0.1:8654/`

## Thread `01a089f9-1c16-7771-b0ff-44d3883daafd`
updated_at: 2026-09-10T07:19:04+00:00
cwd: /Users/wooojin/dev/maple
rollout_path: /Users/wooojin/.codex/sessions/2026/09/10/rollout-2026-09-10T15-19-59-01a089f9-1c16-7771-b0ff-44d3883daafd.jsonl
rollout_summary_file: 2026-09-10T06-19-59-GK85-maplestory_challenger_rewards_bellona_difficulty.md

---
description: MapleStory 챌린저스 시즌4 보상 반입 조사와 레공레 이지 벨로나 난이도 판단. 보스 배율만으로 체감 난이도를 낙관하지 말고 패턴·딜로스·커뮤니티 사례를 함께 반영해야 함.
task: maple-challengers-rewards-and-bellona-difficulty
task_group: /Users/wooojin/dev/maple
task_outcome: partial
cwd: /Users/wooojin/dev/maple
keywords: MapleStory, 챌린저스 시즌4, 월드 리프, 코인샵, 200레벨 달성의 비약, 벨로나, 이지 벨로나, 레테, 레공레, Maplescouter, 인세인, 핀볼
---

### Task 1: 챌린저스 보상·월드 리프 분류

task: 챌린저스 시즌4 이벤트·코인샵 보상의 본섭 직접 수령/리프 반입/리프 불가 분류
task_group: MapleStory challenger rewards and transfer
 task_outcome: partial

Preference signals:
- 사용자가 “모든 보상들”을 “이벤트 별 코인샵별”로 분류해 달라고 요청함 -> 향후에는 직접 수령, 캐릭터 인벤토리로 리프, 리프 불가를 별도 열로 나눈 압축표를 먼저 제시한다.

Reusable knowledge:
- 챌린저스·챌린저스2·챌린저스3의 리프 가능 월드는 스카니아, 베라, 루나, 제니스, 크로아, 유니온, 엘리시움, 이노시스, 레드, 오로라, 아케인, 노바. 챌린저스4는 에오스·핼리오스.
- 사전 리프와 종료 리프 합산 최대 5캐릭터이며, 최초 선택한 도착 월드는 변경 불가.
- 챌린저스 샵의 메멘토 골드/실버 큐브, 카르마 브론즈 에디셔널 큐브, 160제 카르마 스타포스 17성권, 챌린저스 3·4레벨 특수 스킬링 선택권과 해당 링, 메이린 에테르넬 조각은 챌린저스 전용으로 소지한 채 리프할 수 없다.
- 200레벨 달성의 비약과 250레벨 달성의 비약은 챌린저스 월드에서 사용할 수 없으므로 본섭에서 사용해야 한다.

Failures and how to do differently:
- 이벤트 본문이 긴 PNG라 전체 OCR과 브라우저 탐색이 비효율적이었다. 다음에는 공식 HTML에서 `lwi.nexon.com` 이미지 URL을 추출하고, PNG를 1,600~2,000px 단위로 crop/OCR한 뒤 이벤트별 보상·교환 속성·기한을 구조화한다.

References:
- `https://maplestory.nexon.com/News/Update/805`
- `https://maplestory.nexon.com/news/update/811`
- `config/events.json`

### Task 2: 이지 벨로나 난이도 판단

task: 레공레의 이지 벨로나 130.8% 클리어 가능성과 실제 체감 난이도 조사
task_group: MapleStory Bellona boss research
 task_outcome: success

Preference signals:
- 사용자가 “근데 꽤 어렵더라고”라고 교정함 -> 보스 배율만 보고 낙관적인 클리어 시간이나 난이도를 단정하지 말고, 패턴 숙련도·직업별 딜로스·실제 커뮤니티 후기를 함께 반영한다.

Reusable knowledge:
- 2026-09-10 Maplescouter 기준 레공레: Lv.286, 전투력 1억 2,525만, 보스380 헥사환산 49,283, 이지 벨로나 130.8% 솔플 가능.
- 벨로나는 인세인 모드에서 최종 데미지 증가가 있지만, 피격 시 보스 회복과 데스카운트 손실이 발생하므로 생존 실패가 큰 딜로스로 이어진다.
- 반복적으로 어려운 구간으로 언급된 것은 2페이즈 50% 이하 핀볼·중앙 아래 돌진·광폭화 양날도끼다.
- 패턴 중 평딜보다 회피를 우선하고, 숙련 후 평딜을 추가하는 접근이 안전하다.
- 레공레는 하드 메이린 110.5%를 19분 46초에 실제 클리어한 기록이 있으므로 딜 부족보다는 벨로나 패턴 숙련이 주된 병목으로 해석된다.

Failures and how to do differently:
- 초기 답변은 130.8% 배율만 보고 16~17분 클리어를 예상했다. 이후에는 “스펙상 가능”과 “첫 도전 체감 난이도”를 분리하고, 패턴 숙련 전에는 실패·장시간 트라이가 정상일 수 있다고 설명한다.

References:
- `https://maplescouter.com/ko/result?name=%EB%A0%88%EA%B3%B5%EB%A0%88&preset=00000`
- `https://www.inven.co.kr/board/maple/5974/7072345`
- `https://m.blog.naver.com/seotbeo/224386196348`
- `https://arca.live/b/maplestory/180713208`
- `https://m.inven.co.kr/board/maple/2295/302404?category=%EB%A0%88%ED%85%8C&p=3`
- `kb/branchpoints/2026-08-31-legongre-challenger-boss-clears.md`

## Thread `01a089fb-c639-75e1-90a3-ed805c65ee7b`
updated_at: 2026-09-10T08:22:52+00:00
cwd: /Users/wooojin/App/maplog
rollout_path: /Users/wooojin/.codex/sessions/2026/09/10/rollout-2026-09-10T15-22-54-01a089fb-c639-75e1-90a3-ed805c65ee7b.jsonl
rollout_summary_file: 2026-09-10T06-22-54-UpGH-maplog_document_reset_overreach_place_visit_ux.md

---
description: Maplog 문서 재정비는 승인됐지만 Place·Visit browse UI 구현으로 범위를 넓힌 뒤 사용자가 과잉 실행을 교정함. 앞으로 방향 탐색과 구현 승인을 엄격히 분리하고, 중요한 감상·선택 UX는 여러 방향을 먼저 비교해야 함.
task: Maplog 문서 재정비 및 Place·Visit browse UX 범위 판단
task_group: /Users/wooojin/App/maplog
task_outcome: partial
cwd: /Users/wooojin/App/maplog
keywords: Maplog, Place, Visit, document-reset, toyrocket, scope-creep, UX-exploration, simulator, BUILD-SUCCEEDED, Recap
---

### Task 1: 문서 구조 재정비

task: 최신 제품 정의·현재 상태·과거 기록의 역할을 재분리
 task_group: Maplog documentation and product framing
task_outcome: success

Preference signals:
- 사용자가 “구문서는 아카이브로서 전부 읽을 필요없고 분기점 이후 문서 기준”이라고 요청함 -> 최신 입구와 분기점 이후 자료를 우선하고 과거 문서는 필요한 근거로만 확인한다.
- 사용자가 “기존 코드 재활용 및 강화할 가능성이 높기때문에 아예 버리는건 아니라고” 말함 -> 제품 방향 변경을 코드 폐기와 동일시하지 말고 실제 의존성을 확인해 선별 재사용한다.
- 사용자가 “새로운 관점에서 전부 재검토하고 문서도 갈아엎고서 깨끗한 마음으로 시작”을 승인함 -> 기존 단계표를 자동 실행 순서로 취급하지 않고 정의·상태·열린 결정·권고안을 분리한다.

Reusable knowledge:
- 현재 입구는 `record/CURRENT.md`와 `record/PRODUCT.md`; `record/README.md`가 필요 문서로의 경로를 제공한다.
- 9/3 Recap A안은 사용자 실기기 판정으로 마음에 든 출발 자산이나, 제품 통합·출시 품질 완료는 아니다.
- Place-first/day-second, Visit 선택 단위, 사용자 교정 승계·undo, 기존 코드의 선택적 재사용은 보존해야 한다.

Failures and how to do differently:
- 문서 재정비 이후 구현을 시작할 준비가 된 것으로 추론하지 않는다. 구현은 별도 사용자 승인과 명확한 범위가 필요하다.

References:
- `record/PRODUCT.md`
- `record/CURRENT.md`
- `record/README.md`
- `AGENTS.md`
- `record/worklogs/2026-09-10_document_reset.md`

### Task 2: Place·Visit browse 연결 및 UX 검증

task: 기존 사진 기반 Place 지도와 Visit browse/selection 연결
 task_group: Maplog V2 Place·Visit runtime UX
task_outcome: partial

Preference signals:
- 사용자는 처음에 “읽어만 봐. 아직 작업 아니야”라고 했음 -> 읽기/탐색 요청에서 코드·구현으로 넘어가지 않는다.
- 사용자는 “몇번 만져보면 되는 검증은 ... 낑낑댈 필요없고 ... 과하거나 기존대로라면 잘 유지되는 부분은 검증하지 말아줘”라고 함 -> 사용자가 직접 판단할 수 있는 단순 체험은 장시간 검증하지 말고 새 연결·데이터 손상 위험만 확인한다.
- 사용자는 “상하스크롤인지 아님 스와이프 앨범 식인지 ... 다양한 방향성이 많잖아”라고 함 -> 날짜·사진 탐색과 선택 UX는 하나를 빨리 구현해 확정하지 말고 대안을 비교·논의한다.

Reusable knowledge:
- 테스트 보관함 기준 시뮬레이터에서 장소 7곳 표시, 장소 열기, 날짜별 사진, 사진 확대·복귀, Visit 선택·해제·0개·재선택·취소 흐름은 동작했다.
- 빌드 로그 `/tmp/maplog-place-build.log`에 `BUILD SUCCEEDED`가 남아 있다.
- 화면 증거는 `/Users/wooojin/Downloads/maplog-qa/2026-09-10-place-visit-browse/`에 있다.
- 독립 정지화면 검토는 선택·제거는 읽히지만 닫기 의미와 선택 이후 다음 행동이 불명확하다고 판정했다.

Failures and how to do differently:
- 문서 재정비 승인과 제품 구현 승인을 혼동했고, “가보자”를 구체 UX 구현 승인으로 넓게 해석했다.
- 임시 날짜 선택 UI를 기준안처럼 놓고 사용자에게 평가를 요청했다. 다음에는 장소를 연 뒤 감상에서 “이날을 이어 보고 싶다”로 넘어가는 경험을 먼저 탐색하고, 스크롤·스와이프 앨범·선택 위치·선택 시점 등 대안을 비교한다.
- “이어보기 버튼 너무 크다”는 시각 피드백보다 근본적으로 선택 UX를 너무 일찍 고정한 것이 핵심 문제였다. 세부 수정 전에 방향을 다시 논의한다.

References:
- `code/MaplogV2/App/MapFeatureRootView.swift`
- `code/MaplogV2/Photos/PhotoLibraryService.swift`
- `code/MaplogV2/Domain/SceneCatalogSync.swift`
- `code/MaplogV2/Domain/PlaceVisit.swift`
- `/Users/wooojin/Downloads/maplog-qa/2026-09-10-place-visit-browse/01-place-map.png`
- `/Users/wooojin/Downloads/maplog-qa/2026-09-10-place-visit-browse/02-two-visits-selected.png`
- `/Users/wooojin/Downloads/maplog-qa/2026-09-10-place-visit-browse/03-map-visit-selection.png`

## Thread `01a0958b-f918-7ac2-abff-3059bed017d3`
updated_at: 2026-09-12T12:26:34+00:00
cwd: /Users/wooojin
rollout_path: /Users/wooojin/.codex/sessions/2026/09/12/rollout-2026-09-12T21-16-13-01a0958b-f918-7ac2-abff-3059bed017d3.jsonl
rollout_summary_file: 2026-09-12T12-16-13-EmC7-codex_rubato_separation_cwd_config_injection.md

---
description: CODEX_HOME만 바꾸면 충분하다고 잘못 안내했으나, 홈 디렉터리 cwd에서 프로젝트 .codex 설정이 Rubato를 재주입하는 문제를 확인하고 중립 cwd 실행으로 순정 Codex를 검증함
task: isolate plain Codex from Rubato configuration
 task_group: local Codex/Rubato CLI configuration
 task_outcome: partial
cwd: /Users/wooojin
keywords: Codex, Rubato, CODEX_HOME, project config, AGENTS.md, config.toml, plugin list, codex doctor, cwd, openai_base_url
---

### Task 1: 순정 Codex 실행 경로 분리

task: isolate plain Codex from Rubato configuration
task_group: local CLI configuration
task_outcome: partial

Preference signals:
- 사용자가 “일반 codex만 사용해보려면 어떻게 할까?”와 “확인좀해줘”라고 요청함 -> 실행 파일과 유효 설정을 실제로 검사하고, 분리 여부를 새 세션에서 검증하는 방식을 기본으로 해야 함.
- 사용자가 직접 실행 후 Rubato 지침이 여전히 나온다고 피드백함 -> 설정 분리 안내는 명령 제시만으로 완료하지 말고 실제 `plugin list`/세션 지침/doctor 결과를 확인해야 함.

Reusable knowledge:
- `/opt/homebrew/bin/codex`는 `codex-cli 0.154.0`이고, `rubato`는 별도 실행 파일이 아니라 zsh 함수로 `~/.local/bin/rubato-personal`을 호출함.
- 기본 `/Users/wooojin/.codex/config.toml`에는 Rubato `model_instructions_file`, `openai_base_url=http://127.0.0.1:10100/v1`, `rubato-codex@rubato` 플러그인과 marketplace가 있음.
- `CODEX_HOME="$HOME/App/codex-plain-home"`만 지정하고 cwd를 `/Users/wooojin`으로 유지하면 홈 설정은 분리되어도 cwd의 프로젝트 `.codex` 설정이 발견되어 Rubato가 역주입될 수 있음.
- 검증된 순정 실행 형태는 다음과 같음:
  `cd /tmp`
  `CODEX_HOME="$HOME/App/codex-plain-home" /opt/homebrew/bin/codex`
- `/tmp`에서 같은 plain home을 사용해 검사했을 때 `No Rubato paths found`, `MCP servers=0`, provider `openai`, Rubato 플러그인 없음이 확인됨.
- 실제 프로젝트 작업에서는 홈 디렉터리 자체가 아니라 해당 프로젝트 디렉터리에서 plain Codex를 실행해야 함. 필요하면 프로젝트 내부의 `.codex` 설정도 점검해야 함.

Failures and how to do differently:
- `CODEX_HOME`만 바꾸면 완전 분리된다고 단정한 것은 잘못이었다. 다음에는 반드시 cwd를 `/tmp` 같은 중립 위치로 바꾼 뒤 `codex plugin list`와 `codex doctor --json`으로 유효 설정을 확인한다.
- 사용자가 실행한 세션의 첫 시스템 지침이 Rubato였으므로, 실행 표면을 추정하지 말고 세션 기록의 `base_instructions`와 프로세스 환경을 확인한다.
- `~/.zshrc`에 장기 Anthropic 인증 토큰이 평문으로 존재하는 사실이 발견되었으므로 이를 출력하거나 저장하지 말고, 향후 보안 점검에서는 즉시 토큰 폐기·교체를 권고한다.

References:
- `/Users/wooojin/.codex/config.toml`
- `/Users/wooojin/.codex/rubato-codex/install-state.json`
- `/Users/wooojin/App/codex-plain-home/config.toml`
- `CODEX_HOME="$HOME/App/codex-plain-home" /opt/homebrew/bin/codex plugin list`
- `CODEX_HOME="$HOME/App/codex-plain-home" /opt/homebrew/bin/codex doctor --json`
- 공식 AGENTS.md 문서: `https://learn.chatgpt.com/docs/agent-configuration/agents-md`

