# 함께 생각하기 실험판의 호출 방식

이 후보는 사용자의 직접 요청과 에이전트가 관찰한 중요한 해석 불일치에 metaFrame을 사용한다.
사용자 스탠스 문구의 정본은 리드 지침이며, 그 지침에서 이 스킬로 연결한다.
2026-09-10 Fable의 로컬 리뷰는 미노출 원인을 disable-model-invocation: true로 확인했다.
아래 수동 호출 설명은 이전 판의 기록이며 현재 호출 규정은 SKILL.md를 따른다.
이 폴더 전체를 개인 오버레이로 보존해야 업데이트 후에도 변경이 유지된다.
공개 명세의 대소문자 규칙을 Rubato 미노출의 원인으로 사용하지 않는다.
이 설명 자체는 수정본이 실제로 등록됐다는 증거가 아니다. 설치 뒤 새 세션에서 확인한다.

---

# metaFrame v3

metaFrame is a manually invoked Claude Code skill for opening a small amount of problem space before committing to a frame. It is meant to improve the use of capability already present in the model, not to replace the model with a decision system.

## What this version keeps

- the user's request and explicit boundaries as the center of gravity;
- the first framing as provisional only when another view could change the action;
- direct action when the task is already clear;
- focused clarification when only the user knows the decisive preference or goal;
- sources, tests, prototypes, and observations as ways for reality to answer back;
- an optional fresh context when the current conversation may be anchoring the view;
- a return to concrete work rather than visible metacognitive performance.

## What this version removes

- automatic invocation;
- `direct / ask / probe / scout` as an explicit routing taxonomy;
- scoring rubrics, pass thresholds, contrast-case suites, and speculative release gates;
- mandatory blind-brief templates and detailed scout protocols;
- scripts whose main purpose was to validate the evaluation package rather than the skill's behavior.

## Install

The canonical copy lives in the shared skill store:

```text
~/.agents/skills/metaFrame/
```

Each CLI (`~/.claude/skills/`, `~/.codex/skills/`, `~/.grok/skills/`) symlinks to it. For a project-local install, copy into `.claude/skills/metaFrame/`.

Invoke it manually:

```text
/metaFrame
```

or pass the task as an argument:

```text
/metaFrame Review this product decision before implementation.
```

`disable-model-invocation: true` keeps the skill out of Claude's context until you invoke it. Once invoked, the skill text remains in that session, so use a new session or clear the context before unrelated work when you want a clean baseline.

## Package shape

```text
metaFrame/
├── SKILL.md
├── README.md
├── DESIGN_NOTES.md
├── HISTORY.md
├── metadata/version.txt
└── references/
    ├── CALIBRATION.md
    └── FRESH_CONTEXT.md
```

The two reference files are optional. The core skill tells Claude to read them only when they would add signal.
