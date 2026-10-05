# Maintenance Playbook

이 문서는 스킬을 **고치는 사람**(디스패처 세션의 Claude, 또는 사람)을 위한 것이다.
Codex 워커는 이 파일을 읽지 않는다 — SKILL.md 라우팅 테이블에 등록하지 말 것.

## 배경

- 이 스킬은 Codex가 프론트엔드를 데이터-퍼스트로 만드는 실패(주석 같은 카피, 사용자
  여정 부재, 클러터)를 막기 위해 존재한다. 원점이 된 사고 기록:
  `references/task-design-failure-case-study.md` (2026-07-12, Arcaea 채보 검수 UI).
- 정본·설치 경로는 아래 「정본·설치·공유 저장소」 절을 따른다. 실행 시 실제로 선택된 경로는 해당 실행의 기록으로 확인한다.
- 공유 레포: https://github.com/keepitmello/frontend-ux-router (gh 계정: keepitmello)
- 디스패처 쪽 연동: 예전에는 fresh-eyes PASS 기록을 `VERIFIED` 조건으로 썼다. 현재 스킬은 독립 검토를
  중요한 결정을 바꿀 수 있을 때만 쓰고, 실제로 한 검사의 범위를 이름 붙여 보고한다(SKILL.md #8·Completion, frontend-creation §10).

## 개선 루프 (개판 발견 → 스킬 강화)

입력은 셋 중 하나다: 사용자의 "이거 개판이네" 보고, fresh-eyes 리뷰어의 FAIL
트랜스크립트, 또는 배포 전 자체 발견.

### 1. 증거를 그 자리에서 확보

식은 뒤 재구성하면 케이스 스터디의 가치(구체성)가 사라진다. 즉시 수집:

- 렌더된 화면 스크린샷 (문제 상태 그대로)
- 사용자가 정확히 뭐라고 지적했는지 (원문)
- 워커가 시도한 패치들의 순서와 각 패치가 왜 실패했는지
- fresh-eyes FAIL이면 리뷰어의 원문 답변 전체 (그 자체가 미니 케이스 스터디다)

### 2. 진단: 어느 층의 실패인가

| 질문 | 답이 yes면 |
|---|---|
| 현재 SKILL.md 책임(#1~#14)이 다루는데 지켜지지 않은 실패인가? | **집행 문제.** 스킬을 고치지 말고 왜 안 지켜졌는지 추적 — 워커가 스킬을 읽었나, 브리프에 판단할 결정·보호 조건이 갔나, 렌더한 경로를 실제로 걸어 봤나. |
| 형식만 채우고 원래 질문을 못 풀었나? | **판단 기준이 흐린 문제.** 그 책임을 무엇을 보고 판단하는지(관찰 가능한 장면·상태)로 구체화한다. 숫자 버짓·금지어 목록·삭제 목록 같은 범용 관문은 되살리지 않는다(frontend-creation §2·§8). |
| 어떤 규칙도 이 실패를 다루지 않나? | **새 실패 모드.** 3단계로 — 케이스 스터디를 쓰고 규칙으로 증류한다. |

### 3. 케이스 스터디 작성

`references/task-design-failure-case-study.md`를 템플릿으로 사용. 필수 골격:

1. 사고 맥락 (제품/사용자/구현 상황)
2. 사용자가 실제로 필요했던 것 (한 문단)
3. 실패 타임라인 — **각 패치 시도가 왜 실패했는지**가 핵심 자산
4. 근본 원인 패턴 (failure signature + correction 형식)
5. SKILL.md용 압축 규칙 후보

저장: `references/<slug>-case-study.md` → SKILL.md 라우팅 테이블에 한 줄 등록.

### 4. 규칙으로 증류

케이스 스터디에서 본편으로 끌어올릴 때의 우선순위:

1. 실제 실패 장면을 `frontend-creation.md`의 해당 절(§3 구성, §4 문구, §5 시각 개념 등)에 관찰 가능한 기준으로 추가. §2 버짓은 사용자·제품·플랫폼이 준 한도만 담는다
2. stop-and-redesign 트리거에 새 시그니처 추가
3. SKILL.md의 Responsibilities and boundaries는 기존 책임으로 설명되지 않는 핵심 누락이 있을 때만 고친다

### 5. 정본·설치·공유 저장소

이 개인 오버레이의 정본은 `/Users/wooojin/App/rubato-private-config/overlays/skills/frontend-ux-router/`다. `~/.agents/skills/frontend-ux-router/`는 설치본이고, 오버레이 적용(`scripts/apply-rubato-overlays.sh --apply`) 때 정본에서 rsync로 덮어써진다. 설치본을 직접 고쳐 정본을 대신하지 않는다.

`~/.claude/skills`는 `~/.agents/skills`를 가리키는 심링크다. Codex의 `~/.codex/skills/frontend-ux-router/`는 별도 사본이며 이 오버레이 적용으로 갱신되지 않는다. 다른 실행 경로도 실제 연결을 확인하기 전에는 같은 본문을 받는다고 가정하지 않는다.

공유 레포에 올릴 때는 정본 폴더에서 보낸다. README.md는 레포에만 있다(rsync에서 exclude). 정본 수정·설치·공유 저장소 반영은 현재 요청의 쓰기·배포 권한을 따른다.

```bash
cd $(mktemp -d) && gh repo clone keepitmello/frontend-ux-router repo && cd repo
rsync -a --delete --exclude .git --exclude README.md --exclude .rubato-private-overlay /Users/wooojin/App/rubato-private-config/overlays/skills/frontend-ux-router/ .
git add -A && git commit -m "<what failure this addresses>"
gh auth switch --user keepitmello && git push && gh auth switch --user mysubb01
```

하위 참조 디렉토리의 진입점은 `guide.md`다 — `SKILL.md`로 되돌리지 마라. 중첩 `SKILL.md`가 없어야 Claude 스킬 로더가 최상위 하나만 스킬로 잡는다. SKILL.md 라우트 표가 `references/<name>/guide.md`로 직접 부르므로 이름을 바꾸면 링크가 깨진다.

### 번들된 참조의 upstream 출처

아래 넷은 원래 `~/.agents/skills/` 아래 독립 스킬로도 깔려 있었으나, 라우터를 통해서만 진입하면 되므로 2026-07-28에 독립 사본을 제거하고 이 안의 사본만 남겼다. 번들 사본은 upstream 원본이 아니라 **깨진 상호참조를 이 스킬 구조에 맞게 고친 판본**이다. upstream을 다시 당길 일이 있으면 링크 수정분이 날아가지 않게 diff부터 뜰 것.

| 참조 | upstream |
|---|---|
| `references/software-ux-research/` | https://github.com/vasilyu1983/ai-agents-public (`frameworks/shared-skills/skills/software-ux-research`) |
| `references/nng-ux-heuristics/` | https://github.com/phazurlabs/ux-ui-mastery (`skills/nng-ux-heuristics`) |
| `references/performance-states-patterns/` | https://github.com/phazurlabs/ux-ui-mastery (`skills/performance-states-patterns`) |
| `references/information-architecture/` | https://github.com/aj-geddes/useful-ai-prompts (`skills/information-architecture`) |

제거 전 백업: `~/.agents/skill-backups/standalone-ux-skills-20260728/`

## 설계 원칙 — 미래 세션이 지켜야 할 것

이 스킬이 작동하는 이유는 아래 네 가지다. 개선하다가 이걸 깨면 퇴화다.

1. **형용사 대신 관찰할 수 있는 기준.** "깔끔하게"는 안 먹힌다. 판단 기준은 무엇을 보고
   판단하는지(렌더한 경로, 상태 전이, 첫 화면에서 읽히는 것)로 적는다. 다만 숫자 버짓·금지어·삭제 목록을
   모든 화면의 관문으로 되살리지 않는다 — 형식 통과가 원래 질문을 가렸던 것이 이 스킬을 고친 이유다.
2. **빼기는 렌더한 화면에서 판단한다.** 목적 없는 요소는 구성 중과 렌더 뒤에 덜어 낸다. 요소별 장부나
   삭제 할당량, 별도 보고는 요구하지 않는다(frontend-creation §8).
3. **이해도 검토는 만든 맥락과 분리한다.** 이해만 보는 fresh-eyes 검토에는 만든 사람의 설명을 주지 않는다.
   목표·품질 검토에는 그 검토가 확인할 요구를 숨기지 않는다(frontend-creation §10).
4. **구체적 실패 사례가 최고의 교보재다.** "빨간 소리" 같은 실제 실패 예시가
   일반론보다 잘 먹힌다. 증류하면서 사례의 구체성을 버리지 말고, 사례는 사례
   문서에 살려두고 규칙만 본편으로 올린다.

하지 말 것: SKILL.md 비대화(라우터+책임 목록만), 관찰할 수 없는 형용사 조항 추가,
이해 실패를 스킬 문서의 설명 추가로 때우기(제품에서 금지한 걸 스킬에서 하는 셈).

## 백로그 (실전 데이터 확보 후)

- `scripts/copy-lint.sh`: §4 금지어 목록의 grep 자동화 (첫 실전 투입 후)
- fresh-eyes FAIL 트랜스크립트 아카이브 → 반복 패턴이 보이면 규칙 증류
- Codex가 라우터를 실제로 타는지 확인: 첫 디스패치 브리프에 `$frontend-ux-router`
  명시, 반환에 결과물·관찰한 동작·남은 공백이 오는지 확인(SKILL.md Completion)
