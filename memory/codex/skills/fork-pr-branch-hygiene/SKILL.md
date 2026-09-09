---
name: fork-pr-branch-hygiene
description: 외부 GitHub repo를 fork 기반으로 작업할 때 `pr 직전까지`, `fork하고 pull request`, `커밋 정리` 같은 요청에 맞춰 upstream 비교, clean branch 생성, PR 히스토리 정리를 수행한다.
argument-hint: "[repo-path]"
disable-model-invocation: true
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# When to use

- 외부 repo를 로컬에서 수정 가능한지 확인해야 할 때
- fork/origin/upstream 구조에서 PR-ready branch를 준비해야 할 때
- 사용자가 `pr 직전까지`, `이전에 한 커밋은 빼줘`처럼 clean PR state를 요구할 때

쓰지 말 것:

- 이미 로컬 단일 repo에서 단순 코드 수정만 하면 되는 경우
- 사용자가 히스토리 rewrite를 원하지 않거나 shared branch 안전성이 불분명한 경우

# Inputs / context to gather

1. 정확한 repo URL 또는 `owner/name`을 확인한다.
2. 현재 폴더가 git repo인지 확인한다.
3. `origin`과 `upstream`이 어떻게 연결돼야 하는지 확인한다.
4. push 권한과 네트워크 제약 유무를 확인한다.
5. 사용자가 PR 생성까지 원하는지, `pr 직전까지`에서 멈추길 원하는지 확인한다.

# Procedure

1. 현재 checkout 확인:
   - `git status --short --branch`
   - `git remote -v`
2. repo 접근성 확인:
   - exact repo URL 기준으로 접근 가능 여부를 본다.
   - `gh auth status`가 깨져 있으면 CLI만 믿지 않는다.
3. fork 구조 정리:
   - 필요하면 clone
   - `git remote add upstream <upstream-url>`
   - `git fetch origin upstream`
4. branch base 검증:
   - `git rev-list --left-right --count upstream/main...origin/main`
   - fork `main`이 ahead/behind면 `upstream/main`에서 새 작업 브랜치를 만든다.
5. push 가능성 확인:
   - `git push --dry-run origin HEAD:refs/heads/<branch>`
6. 코드 import/정리 후 검증:
   - 의존성 설치
   - lint/build 또는 해당 repo의 검증 명령
7. 사용자가 clean history를 원하면:
   - commit squash 또는 `git commit --amend --no-edit`
   - remote update는 `--force-with-lease`
8. 사용자가 `pr 직전까지`를 원하면 PR 생성은 하지 않고 브랜치 상태와 다음 명령만 남긴다.

# Efficiency plan

- repo 이름이 모호하면 broad search보다 exact URL 확보를 먼저 한다.
- remote divergence는 로그를 길게 읽기보다 `git rev-list --left-right --count`로 먼저 본다.
- push 전에는 항상 dry-run으로 권한/remote path를 확인한다.
- generated artifacts는 검증 후 제거한다.
- stop rule: branch push 가능, 검증 통과, 사용자 요구한 commit hygiene 충족이면 PR 생성 직전에서 멈춘다.

# Pitfalls and fixes

- 증상: 현재 폴더가 repo가 아니라서 모든 git 명령이 헛돈다.
  - 원인: checkout 위치 오판.
  - 수정: 시작할 때 git repo 여부부터 확인한다.
- 증상: fork `main`에서 바로 작업해 unrelated commit이 PR에 섞인다.
  - 원인: upstream divergence 미확인.
  - 수정: upstream과 origin을 비교하고 필요하면 fresh branch를 upstream에서 딴다.
- 증상: `gh` auth 오류만 보고 repo 접근 불가로 결론낸다.
  - 원인: auth 문제와 repo existence 문제를 혼동.
  - 수정: exact repo URL, clone 가능 여부, remotes를 분리해서 본다.
- 증상: amend 후 push가 거절된다.
  - 원인: 히스토리 rewrite 후 normal push 사용.
  - 수정: `git push --force-with-lease`를 쓴다.

# Verification checklist

- 현재 폴더가 실제 git repo인지 확인했다.
- `origin`/`upstream` 구성이 명확하다.
- divergence를 확인하고 적절한 base branch를 골랐다.
- dry-run push 또는 동등한 확인으로 push 경로를 검증했다.
- lint/build 등 검증 명령 결과를 남겼다.
- 사용자가 원한 stopping point가 `PR 생성 전`인지 `PR 생성까지`인지 맞췄다.
