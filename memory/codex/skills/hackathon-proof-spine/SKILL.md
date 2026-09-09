---
name: hackathon-proof-spine
description: 열린 해커톤을 시작하거나 제출 직전일 때, `한 줄 → 한 사용자 경로 → 한 코드 경로 → 한 검증 명령 → 한 제출 주장` proof spine과 clean ZIP 검증을 정렬한다.
argument-hint: "[contest-repo-or-brief]"
disable-model-invocation: true
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# When to use

- 새 해커톤의 초기 운영 방식, worktree/task packet, phase transition을 잡을 때
- `제출 전`, `final ZIP`, `claim-evidence`, `통합`처럼 구현과 제출 증거를 연결해야 할 때
- Cofathon/KB AI Challenge처럼 열린 문제에서 제품 선택과 재현성 모두가 중요한 경우

쓰지 말 것:

- 이미 좁게 정의된 일반 버그 수정
- 대회 원문, 제출 규격, 사람의 제품 선택이 아직 제공되지 않았는데 그것을 임의로 결정하는 경우

# Inputs / context to gather

1. 대회 원문과 정확한 제출 규격을 고정한다.
2. 현재 프로젝트의 `START_HERE.md`, `DECISIONS.md`, `CONTRACT.md`, `RELEASE.md`, `AGENTS.md` 존재와 최신성을 확인한다.
3. 대표 사용자 경로 하나와 이를 뒷받침할 코드 경로·검증 명령·제출 주장 후보를 적는다.
4. shared host, 각자/agent worktree, integration owner, clean release worktree를 식별한다.
5. dirty tree와 현재 contract 변경 사항을 먼저 확인한다.

# Procedure

1. 대회 원문을 프로젝트의 짧은 현재 진입점에 고정하고, 상세 history/research와 분리한다.
2. 독립 탐색과 사람의 제품 선택 뒤, 대표 문장마다 `사용자 경로 → 코드 경로 → 검증 명령 → 제출 주장`을 한 줄로 매핑한다.
3. 입력 1건부터 결과 복귀까지 proof spine을 실제로 연결한다. 이 전에는 UI/runtime/docs/추가 시나리오의 병렬 확장을 시작하지 않는다.
4. 문서 권위를 분리한다: 현재 사실·결정·계약·release 상태는 project docs에, durable safety rules만 `AGENTS.md`에 둔다. 개인 판단 노트는 공유 결정 문서와 섞지 않는다.
5. worktree별 owner 범위를 packet으로 나누고, integration owner가 60–90분 단위 통합을 한다. contract 변경은 즉시 함께 확인한다. 같은 파일 동시 수정은 pair session으로 전환한다.
6. release에서 새 기능을 동결한다. 정확한 제출 ZIP을 새 디렉터리에 풀고 install, build, test, hero smoke, PDF render, claim-evidence 대조를 실행한다.

# Efficiency plan

- 먼저 대표 경로 한 개만 완주해 넓은 병렬 작업이 fixture-only가 되는 것을 막는다.
- 각 claim의 증거 명령과 출력 위치를 한 표/짧은 목록에 캐시한다.
- stop rule: clean release directory에서 모든 제출 주장에 대응하는 재실행 증거가 있을 때만 final PASS로 보고한다.

# Pitfalls and fixes

- 증상: 문서는 많은데 SSOT가 계속 바뀌거나 runtime이 fixture UI와 분리된다.
  - 원인: 문서의 권위와 phase gate가 불명확하다.
  - 수정: project current docs와 durable `AGENTS.md`를 분리하고 proof spine부터 잠근다.
- 증상: GitHub `main` push/pull이 실시간 handoff가 되고 통합 비용이 커진다.
  - 원인: worktree/owner 경계가 없다.
  - 수정: 독립 worktree와 integration owner를 쓰고 GitHub는 milestone backup/final publication으로 제한한다.
- 증상: 작업 저장소는 통과하지만 제출물이 실패한다.
  - 원인: final archive를 다시 검증하지 않았다.
  - 수정: exact ZIP을 새 디렉터리에 재추출해 release checklist를 다시 실행한다.

# Verification checklist

- 대표 claim마다 사용자 경로, 코드 경로, 검증 명령, 제출 증거가 있다.
- proof spine이 입력 1건부터 결과 복귀까지 실제로 동작한다.
- `AGENTS.md`에는 durable safety rules만 있고 현재 제품/상태/긴 history는 project docs에 있다.
- owner, integration owner, clean release worktree가 명확하다.
- exact final ZIP을 fresh directory에서 install/build/test/hero smoke/PDF render/claim-evidence 비교했다.
- 작업 checkout의 성공과 제출 아카이브의 성공을 구분해 기록했다.
