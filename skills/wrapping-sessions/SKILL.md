---
name: wrapping-sessions
description: "Generate RAG-optimized wrap documents for cycles/. TRIGGERS: -마무리 -문서화 -wrap"
---

<role>
Document sessions so a fresh AI agent can fully onboard from this document alone.

문체와 형식의 정본은 메모리의 `reference/writing.md`다. wrap을 쓰기 전에 그 파일을
통째로 읽고 원문 표본을 따라 써라. 이 스킬의 안내가 writing.md의 판단과 부딪히면
writing.md가 이긴다.
</role>

<core_principle>
**Onboarding-Ready Documentation**

A new agent should understand from this document:
- **Why**: Background, why this work was needed
- **How**: Analysis/debugging process, how you found the cause
- **What**: What was changed
- **Decision**: Why this approach, what alternatives were considered
- **Impact**: System effects, side effects, caveats

Sections are flexible. Content must be detailed enough for full context transfer.
</core_principle>

<instructions>
1. Run `date +"%Y-%m-%d %H:%M"` to get current time
2. Create file at `cycles/YYYY-MM/wkN/MM-DD/HHMM-topic-wrap.md`
3. Write with enough detail for agent onboarding
4. Return the created path and any open verification gap
5. Do not stage, commit, or push; the caller owns Git operations
</instructions>

<week_mapping>
Days 1-7: wk1 | Days 8-14: wk2 | Days 15-21: wk3 | Days 22-28: wk4 | Days 29-31: wk5
</week_mapping>

<writing_guide>
**Context** - Not just "bug fix":
- What situation triggered this work
- What symptoms users experienced
- Why this matters

**Investigation/Analysis** (when applicable):
- What hypotheses you had
- How you verified (logs, debugging, tests)
- How you narrowed down the cause

**What Didn't Work** - Lessons from failures:
- What you tried
- Why it failed (specific reason)
- Takeaway for future

**Decision Rationale** (when applicable):
- Alternatives considered
- Pros/cons of each
- Why you chose this approach

**Work Accomplished** - What + Why + How:
- Not just "modified file"
- Why you implemented it this way
- Key logic/patterns explained

**Architecture Impact** (when applicable):
- Components affected
- Caveats, side effects
- Notes for future related work
</writing_guide>

<template>
아래는 참고용 예시다. 절 이름과 순서를 그대로 강제하지 마라. 무엇을 남기고 뺄지는
writing.md의 독자 기준으로 정하고, frontmatter(date/scope/type)와 Files Changed처럼
검색·이력에 쓰이는 항목만 유지하면 된다.

```markdown
---
date: YYYY-MM-DD
scope: [module1, tech1]
type: feature | fix | refactor | debug
---

## TL;DR
[1-2 sentences: what + why + result]

## Keywords
`keyword1` `keyword2` `function_name`

## Context
[Background, problem situation, why it matters - detailed]

## Investigation (when debugging/analyzing)
[Hypothesis → Verification → Discovery]

## What Didn't Work (when applicable)
### ❌ [Failed approach]
- Tried: [what]
- Problem: [why failed]
- Lesson: [takeaway]

## Decision Rationale (when significant decisions made)
[Alternatives compared, why this choice]

## Work Accomplished
### 1. [Change group]
[What, why, how - detailed]
- File: `path/file.ts:line`

## Architecture Impact (when applicable)
[Scope of impact, caveats]

## Files Changed
| File | Change |
|------|--------|
| `path/file.ts` | [description] |

```
</template>

<checklist>
After writing:
- [ ] Can a new agent fully onboard from this document?
- [ ] Is Why/How/What sufficiently explained?
- [ ] Are decision rationales recorded (when applicable)?
- [ ] Are failed attempts and lessons recorded (when applicable)?
</checklist>

