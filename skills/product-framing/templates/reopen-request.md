# REOPEN_REQUEST 양식

동결 해제 사유는 `references/04-lock-and-reopen.md`를 따른다. 새 관찰 또는 결정권자의 명시적인 목표 변경을 구별해 적는다.
"구현이 귀찮다", 에이전트가 다른 UI를 선호한다는 사실만으로는 바꾸지 않는다.
승인자·승인 기록·기존 외부 약속 검토를 생략하지 않는다.
결정권자의 요청은 실제 발화나 승인 기록으로 확인한다. "우진이 좋아할 것"이라는 에이전트의 추측이나 부분 호감은 그 요청이나 승인으로 사용하지 않는다.

```markdown
REOPEN_REQUEST
current_frame: <frame_id + version>
change_reason: <새 관찰 또는 결정권자의 명시적인 목표 변경>
observed_evidence: <관측 자료 또는 변경 요청 원문. 선호 변경을 시장 사실로 쓰지 않는다>
which_invariant_failed: <충돌하거나 바꾸려는 불변 조건>
impact_on_existing_commitments: <이미 한 약속·안전·개인정보·운영 책임에 미치는 영향>
why_solution_iteration_is_insufficient: <구현 변경(가변 요소)으로는 왜 해결이 안 되는가>
candidate_new_frames: <선택을 바꿀 만큼 다른 구상과 기존 방향 유지. 후보 수를 채우지 않는다>
decision_owner: <사람>

--- 결정 기록 (REOPEN_REQUESTED 이후의 종결 전이는 이 블록만이 일으킨다) ---
decision: APPROVED | REJECTED
approved_by: <사람>
approved_at:
decision_note:
```

## 제출 후 상태 규칙

- 제출 즉시 프레임 status는 `REOPEN_REQUESTED`가 된다. 이 동안 **불변식에 의존하는 새 구현 착수는 중단**하고, 진행 중인 가변 요소 작업(UI·구현 방식)은 마무리해도 된다.
- **decision: APPROVED** (approved_by·approved_at 필수): 기존 버전을 SUPERSEDED로 바꾸고, 새 버전 DRAFT로 점검표를 다시 판정한다. 대체 프레임 없이 접기로 한 승인이면 SUPERSEDED 대신 RETIRED로 종료한다(`references/02`의 전이표 참조). 새 lock이 ACTIVE가 되기 전까지 구현 위임은 재개하지 않는다.
- **decision: REJECTED**: status를 LOCKED로 되돌린다. 기존 gate_verdict와 동결이 그대로 복원된다.
- 요청 제출이 일으킬 수 있는 전이는 `LOCKED → REOPEN_REQUESTED` 하나뿐이다. 그 이후의 종결 전이(SUPERSEDED·RETIRED 또는 LOCKED 복귀)를 결정 기록 없이 수행하는 세션은 프로토콜 위반이다. 이전 프레임이 SUPERSEDED가 되는 시점은 **동결 해제 승인 시**가 유일하다.
