# 제작 지침을 고칠 때의 기준

이 문서는 스킬을 수정하는 담당을 위한 것이고, 실제 제작자가 매번 읽는 절차가 아니다. SKILL.md 라우팅 표에 필수로 추가하지 않는다. 원점이 된 사례는 `references/task-design-failure-case-study.md`이며, 과거의 해법이 모든 새 화면의 정답은 아니다.

## 실제로 전달된 지침과 행동을 함께 본다

사용자 원문, 당시 결과와 해당 수정·관찰을 연결한다. 모델의 사후 반성은 원인 증명이 아니다. 기존 문장에 같은 뜻이 있다는 것만으로 집행 문제라고 단정하지 않는다. 지침이 실제로 도달했는지, 원칙을 적용할 상황을 잘못 구별했는지, 필요한 전문 지식이나 관찰이 없었는지에 따라 고칠 곳이 달라진다.

자료가 부족하면 필요한 자료를 주고, 출처를 잘못 연결했다면 판단을 가르는 차이를 설명한다. 이미 하는 검사를 더 시켜도 눈에 보이는 구성 문제를 못 찾는다면 검사 횟수보다 검사하는 질문을 바꾼다. 도구나 모델의 한계가 드러나면 설정 문구만 계속 늘리는 해법에 고정되지 않는다.

## 사례에서 적용 조건을 남긴다

새 사례가 기존 원칙을 더 잘 설명한다면 해당 문단을 대체하거나 짧은 대조를 넣는다. 같은 “복잡하다”에도 중복은 덜어내고 필요한 정보는 재배치하는 차이가 중요하다. 모든 사건을 새 금지어·요소 개수·재시도 횟수로 바꾸지 않는다.

성공적인 대응은 실제로 고친 내용과 유지한 목적까지 보여준다. 새로 구성한 이상적인 예시는 실제 관찰과 구별한다. 긴 실패 기록은 이유를 다시 찾아야 할 때만 참조하고, 본문에는 새로운 선택을 가능하게 하는 최소한의 맥락을 남긴다. 같은 사례를 가르치고 그 사례만 잘 처리했다고 일반화 성과로 보고하지 않는다.

## 필요한 지침만 한 역할에 남긴다

공통의 권한·피드백·보고 책임을 전문 스킬마다 다시 정의하지 않는다. 다만 별도 작업자가 공통 지침을 받지 못하면 필수 계약을 그 작업자에게 전달해야 한다. 실제 화면 제작에는 장면·관계·내용 선택·조작과 관찰에 필요한 구별을 남긴다. 파일 개수보다 실제 읽는 경로와 반복되는 절차를 줄인다.

바꾼 지침, 보존한 계약, 달라지길 기대하는 행동을 함께 기록한다. 최종 모델 입력, 실제 결과, 사용자가 다시 설계해줘야 한 일을 구별해서 확인한다. 텍스트 감소와 정적 검사 통과만으로 제작 성능이 좋아졌다고 말하지 않는다.

## 정본·설치·공유 저장소

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

## 변경 뒤 확인할 것

기존 역할·접근성·보호 조건·도구 계약을 유지했는지 본다. 관찰이나 인용의 정확성을 확인하는 검사와, 그 자료로 무엇을 말할 수 있는지 판단하는 안내는 구별한다. 넓은 변경은 대표 작업과 안내에 넣지 않은 장면에서 확인하되, 유료 모델 실행과 설치는 현재 권한을 따른다.

현재 목차·직접 참조·프런트매터·검색용 경로가 깨지지 않게 확인한다. 특히 §4의 보편적인 금지어 목록을 되살리는 검사기는 만들지 않는다. 표면 문자열로 판정할 수 없는 의미 문제는 그 차이를 설명하는 사례와 실제 결과의 대조로 다룬다.
