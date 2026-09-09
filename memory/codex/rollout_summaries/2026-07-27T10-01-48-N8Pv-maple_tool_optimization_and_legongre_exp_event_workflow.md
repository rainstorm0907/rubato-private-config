thread_id: 019fa306-06b3-71f3-a29a-649ca3a279a1
updated_at: 2026-08-13T14:05:16+00:00
rollout_path: /Users/wooojin/.codex/sessions/2026/07/27/rollout-2026-07-27T19-01-48-019fa306-06b3-71f3-a29a-649ca3a279a1.jsonl
cwd: /Users/wooojin/dev/maple
git_branch: main

# Maple 프로젝트 도구를 실제 실행하며 최소 개선하고, 이후 레공레 경험치·이벤트 상담까지 진행한 롤아웃

Rollout context: `/Users/wooojin/dev/maple`에서 프로젝트 문서와 도구를 읽고 실제 캐릭터 스냅샷, CLI, 리서치 다이제스트, 공유 패키징을 실행했다. 사용자는 데이터 freshness를 30분으로 강제하지 말고 “오늘 갱신한 데이터는 약 2주 재사용”하길 원했다.

## Task 1: Maple 저장소 오리엔테이션 및 작업 시작 계획

Outcome: success

Preference signals:

- 사용자가 “메이플 프로젝트의 작업 관련 파일들 분석해보고 이 세션 작업 시작 계획세워봐”라고 요청했고, 이후 코드 개선을 선택했다 -> 먼저 문서·현재 상태·실제 실행 가능 범위를 읽고 계획을 제안하는 흐름을 선호한다.
- 사용자가 “데이터 며칠 오래되어도 괜찮아. 일단 오늘 한번 업뎃하고 2주정돈 괜찮”이라고 명시했다 -> 캐릭터 snapshot에 고정된 15~30분 freshness gate를 적용하지 말고, 사용자가 오늘 갱신한 데이터는 약 14일 재사용하되 경매장·이벤트 일정·주간 진행은 별도 최신 확인한다.

Reusable knowledge:

- 새 세션 진입 문서 순서는 `AGENTS.md` → `kb/codex-brief.md` → `kb/session-handoff.md`; 대상 캐릭터를 확정한 뒤 필요한 상태만 갱신한다.
- 프로젝트의 중심은 자동 결론 앱이 아니라 Open API snapshot, `manual-state.json`, `doctor/today/skill`, 경매장·Maplescouter·리서치 도구를 연결하는 상담 도구다.
- 과거 `examples/woojin-case-study/`는 계산 검증 사례이며 활성 캐릭터의 현재 상태로 사용하지 않는다.

References:

- `/Users/wooojin/dev/maple/AGENTS.md`
- `/Users/wooojin/dev/maple/kb/codex-brief.md`
- `/Users/wooojin/dev/maple/kb/session-handoff.md`
- `./scripts/fetch_character.sh <캐릭터명>`

## Task 2: 실제 Maple 도구 실행 및 최소 코드 개선

Outcome: success

Key steps:

- `레공레`를 `./scripts/fetch_character.sh 레공레`로 갱신해 2026-07-27 19:09 KST 기준 Lv.282 레테, API 15/15 상태를 확인했다.
- `doctor`, `today`, `skill 레공레 '보이드 오리진'`을 실행해 실제 출력과 노이즈를 확인했다.
- `today`의 UTC ISO 표시를 KST 표시로 변경하고, 해방 상태를 추적하지 않는 캐릭터에 불필요한 해방 blocker가 생성되지 않도록 수정했다.
- `latest_digest.sh`는 브라우저(CDP `127.0.0.1:9223`) 실패를 기존처럼 성공으로 끝내지 않고 부분 결과를 보존하면서 종료 코드 1을 반환하도록 수정했다.
- `package_share.sh` 보안 검사가 KB의 `/Users/...` 경로를 탐지해 실패했으며, 개인 로컬 경로를 일반 표현으로 바꾼 뒤 secret scan과 zip 생성이 통과했다.

Failures and how to do differently:

- `quiet-browse`가 `ECONNREFUSED 127.0.0.1:9223`로 실패했는데도 기존 다이제스트 스크립트가 성공 종료했다. 브라우저 섹션 실패 수를 추적하고 exit 1을 반환해야 한다.
- `package_share.sh`의 보안 정규식을 느슨하게 하지 말고, 공유 문서에 남은 개인 경로를 제거하는 방식으로 해결했다.
- `today` 출력은 사용자 timezone에 맞춘 KST가 이해하기 쉽다.

Reusable knowledge:

- 핵심 테스트와 정적 검증은 `npm test`, `bash -n scripts/*.sh`, `node --check tools/auction-scan.js`.
- 최종 검증 결과 growth 테스트 7개, auction fixture/429 backoff 테스트가 모두 통과했고 공유 zip 생성 및 secret scan도 통과했다.
- `latest_digest.sh`는 RSS 유튜브 결과만 남더라도 브라우저 섹션이 실패하면 전체 최신 정찰 성공으로 간주하지 않는다.

References:

- 수정 파일: `tools/growth-assistant.mjs`, `tools/growth-assistant.test.mjs`, `scripts/latest_digest.sh`, `AGENTS.md`, `kb/codex-brief.md`, `kb/session-handoff.md`, `kb/research-workflow.md`, `kb/branchpoints/2026-07-22-weekly-boss-runtime.md`
- 검증 문자열: `부분 실패: kb/latest-digest.md ..., 브라우저 섹션 5개 실패`
- 검증 결과: `7 pass`, `auction-scan parse fixture PASS (6 items) + 429 backoff PASS`, `package_share PASS`

## Task 3: 레공레 경험치·모멘텀 패스·메카베리 상담

Outcome: success

Preference signals:

- 사용자는 “실제 평균 경험치 세팅으로 30분 사냥을 1소재라고 해”처럼 자신의 단위와 실제 세팅으로 환산해 달라고 했다 -> 일반적인 시간/경험치 설명보다 사용자 정의 단위(소재)와 메소 환산으로 결론을 먼저 제시한다.
- 사용자는 “시간대비 몇억 정도까지라고 결론내줘”, “억당 1600원이라고 가정”이라고 좁혀 요청했다 -> 계산 과정은 짧게 유지하고 구매 상한·추천 여부를 명확히 제시한다.
- 사용자가 모멘텀 패스를 구매한 뒤 “사용 순서 중요해?”라고 물었다 -> 이미 구매한 선택을 전제로 손실 여부와 최적 사용 순서를 실측 계산으로 확인한다.

Reusable knowledge:

- Mapleroad 계산기 실측에서 레공레의 경험치 세팅과 최상층 통로 2 기준 1소재(30분)는 대략 0.545~0.581%였다.
- 유료 모멘텀 패스 보상은 메카베리 10장 + 상급 EXP 9,000장으로 약 160~171소재, 80~85시간 사냥 상당으로 계산되었다. 49,800원, 억당 1,600원 가정 시 31.125억 메소 상당이다.
- 당시 결론은 30억까지 확실히 납득 가능, 35억까지 시간 절약 목적이면 허용, 레공레가 실제로 구매했고 이후 Lv.284 76.386% 스크린샷으로 예상보다 높은 결과를 확인했다.
- 메카베리와 상급 EXP 사용 순서는 실측상 거의 차이가 없었다: 메카베리→EXP 약 Lv.284 69.360%, EXP→메카베리 약 69.359%. 따라서 메카베리부터 써도 된다.
- 공식 메카베리 안내상 피버는 경험치 배율이 아니라 `슈피겔버스트`를 쿨타임 없이 쓰게 하는 상태다. 경험치 증가 효과는 적용되지 않으며, 30분 제한 내 복구율 100% 달성이 중요하다. 피버 중 퇴장하면 게이지가 초기화된다.

Failures and how to do differently:

- 초기에 모멘텀 패스 결과를 Lv.284 69%대로 예측했지만 실제 스크린샷 결과는 Lv.284 76.386%였다. 실제 사용 직전 경험치와 화면값을 우선해 예측을 갱신하고, 계산값은 범위/조건과 함께 제시한다.
- “4배 경쿠 3시간”을 전부 절약 시간으로 계산하지 않고, 평소 3배 세팅 대비 추가 경험치만 절약분에 포함해야 한다.

References:

- 사용자 정의 단위: `1소재 = 30분 사냥`
- 공식 메카베리 안내: `https://maplestory.nexon.com/news/update/790`
- 계산 엔드포인트: `https://mapleroad.kr/lib/calculator/golden_berry`, `https://mapleroad.kr/lib/calculator/exp`, `https://mapleroad.kr/lib/exp_calculator/hunt`

## Task 4: 렌 스킬/창룡파천검 질문

Outcome: partial

Key steps:

- `./scripts/fetch_character.sh 렌`은 Nexon API `OPENAPI00004` 및 HTTP 400으로 실패했다. 캐릭터명이 유효하지 않다고 단정하지 않고 오류 응답을 확인했다.
- 웹 검색 결과에서 렌의 창룡파천검 관련 트리거/승천/심검 정보는 일부 확인했지만, 최종 답변까지 완결된 검증은 남지 않았다.

Failures and how to do differently:

- `rg`를 `character` 전체에 실행하면 대형 JSON이 수십만 토큰으로 출력될 수 있다. 특정 파일·필드·`jq` projection으로 제한해야 한다.
- API가 400 JSON을 반환할 때 traceback만 노출하지 말고 HTTP 상태와 API error body를 먼저 짧게 출력하는 fetch 오류 처리가 필요하다.

References:

- 오류: `{"error":{"name":"OPENAPI00004","message":"Please input valid parameter"}}`
- 검색 결과에는 `창룡파천검 : 승천`, `망혼검 절기 : 심검 이후 발동` 관련 자료가 있었으나, 공식 스킬 사용 순서로 확정하지 않았다.
