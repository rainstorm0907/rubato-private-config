---
name: update-docs
description: Add update section to existing wrap document. Use when continuing work on same context and need to document additional changes, analysis, or decisions.
---

# Update Docs

기존 wrap 문서에 추가 작업 내용을 기록합니다.

문체와 내용 판단은 메모리의 `reference/writing.md`를 따른다. 쓰기 전에 그 파일을
통째로 읽고, 이 스킬은 기존 문서에 내용을 추가하는 역할만 맡는다.

## 워크플로우

```
1. date +"%Y-%m-%d %H:%M"  → 현재 시각 확인
2. 기존 wrap 문서 찾기     → cycles/YYYY-MM/wkN/MM-DD/*-wrap.md
3. 활성 체크포인트 경로 확인 + 전체 히스토리 리플레이
4. 문서 끝에 새 섹션 추가 (이번 변경이 전체 여정에서 어디에 해당하는지 명시)
5. 수정한 문서 경로와 남은 검증 공백 보고
6. stage·commit·push는 하지 않음 — 호출자가 Git 작업을 맡음
```

## 섹션 형식

```markdown
============================================================

## 작업 제목 [HHMM]
```

제목/내용 모두 자유롭게 작성. 아래 템플릿은 **참고용** (필요한 것만 선택해서 사용).

## 참고 템플릿

```markdown
============================================================

## 작업 제목 [HHMM]

**Author**: Claude Opus 4.5
**Time**: YYYY-MM-DD HH:MM

### Checkpoint
- Path: `.codex/checkpoints/YYYYMMDD-HHMM-task-slug.checkpoint.json`
- Status: `in_progress | waiting_input | blocked | done | stopped`
- Replay: `전체 checkpoint 재확인 완료 시각 HH:MM`

### What Changed
[추가로 분석하거나 작업한 내용]
- 변경 1: [무엇을] — [왜]
- 변경 2: [무엇을] — [왜]

### Decisions Made
[의사결정 내용과 근거]
- **결정**: [선택한 것]
- **이유**: [왜 그렇게 했는지]
- **대안**: [고려했지만 버린 것] (있다면)

### Files Modified
- `path/to/file.ts`: [한 줄 설명]

### Notes
[추가 메모, 발견한 것, 후속 작업 등]
```

## Codex-Followup 후 사용 시

`codex-followup` 완료 후 문서화할 때:

```markdown
============================================================

## Codex-Followup [HHMM]
```

## 체크리스트 (참고용)

- [ ] 현재 시각 확인했나?
- [ ] 기존 wrap 문서 경로 맞나?
- [ ] 체크포인트 전체 히스토리를 재확인했나?
- [ ] 체크포인트 경로와 상태/Replay 시각을 기록했나?
- [ ] What Changed에 "무엇을 왜" 포함했나?
- [ ] Decisions에 근거가 있나?
- [ ] Files Modified 빠진 거 없나?
- [ ] 수정한 문서 경로와 남은 검증 공백을 보고했나?
