---
name: wrapping-sessions
description: "작업을 마무리하거나 다음 담당에게 이어줄 기록을 만든다. 같은 과제의 기존 대표 문서를 우선 갱신하고, 새로운 회고가 필요한 때만 새 파일을 만든다. 단순 상태 질문이나 매 대화마다 실행하지 않는다."
---

# 현재 작업을 이어갈 기록을 남긴다

[공통 작성 원칙](references/documentation.md)을 적용해. 이미 같은 판본을 읽었으면 다시 읽지 않아.
이 스킬은 문서를 쓰는 입구야. checkup이나 update-docs를 추가 단계로 실행하지 않아.

프로젝트의 현재 문서와 이번 결과를 보고, 기존 파일을 갱신할지 새 회고가 필요한지 판단해.
다음 담당이 현재 목표·유효한 결정·실제 결과·남은 질문·원문 위치를 찾을 만큼 기록해.
전체 대화를 복사하거나 모든 과제에 같은 제목과 체크리스트를 강제하지 않아.

새 회고 위치에 프로젝트 규약이 없으면 기존 `cycles/YYYY-MM/wkN/MM-DD/HHMM-topic-wrap.md`를
사용해. 날짜와 시각은 실제 환경에서 확인하고, wk1은 1–7일, wk2는 8–14일,
wk3은 15–21일, wk4는 22–28일, wk5는 나머지 날이야. 검색이 쓰는 frontmatter와
`Files Changed` 표는 유지해:

```markdown
---
date: YYYY-MM-DD
scope: [module1, tech1]
type: feature | fix | refactor | debug
---
```

절 이름(TL;DR, Context, Decision, Files Changed 등)은 참고일 뿐 순서와 개수를 강제하지 않아.

기록을 썼으면 생성·갱신한 경로와 중요한 남은 공백을 짧게 돌려줘.
이 스킬은 stage·commit·push나 자동 기억 승격을 하지 않아. 해당 권한은 호출한 작업이 맡아.
