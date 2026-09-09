---
name: shared-rubato-clone-hazard
description: "/Users/wooojin/dev/Rubato 클론은 여러 세션이 동시에 쓴다, 브랜치·워킹트리 조작 전 reflog로 다른 세션 확인"
metadata:
  node_type: memory
  type: project
---

`/Users/wooojin/dev/Rubato`(= `dev/rubato`, APFS 대소문자 무시라 같은 디렉터리) 는 **여러 세션이 동시에 쓰는 공유 작업공간이다.** 내 세션 전용이 아니다.

2026-08-28 에 이걸 모르고 밟았다. 다른 세션이 그 안에서 커밋하고 `reset` 하고 새 브랜치(`feat/msearch-resilience`)를 체크아웃하는 동안, 나는 같은 클론에서 브랜치 5 개를 지우고 워크트리를 prune 했다. 그리고 `git status` 에 낯선 수정 파일 9 개가 뜨는 걸 **내가 띄운 서브에이전트가 파일을 망가뜨린 것**으로 오독했다. 실제로는 그 세션의 진행 중인 작업이었다. 훅이 `git restore` 를 막지 않았으면 남의 작업을 날렸다.

**조작 전 확인 순서.**

```sh
git -C <클론> reflog -8          # 최근 checkout/commit/reset 이 내 것인가
ls -lat <클론>/.git | head -5    # HEAD·index·config mtime 이 방금인가
git -C <클론> branch --show-current
```

reflog 에 내가 안 한 항목이 있으면 **워킹트리를 건드리지 않는다.** 브랜치 삭제·prune·restore·checkout 전부 보류한다.

**안전한 우회는 워크트리다.** `git worktree add /tmp/<이름> <브랜치>` 로 별도 디렉터리를 만들면 공유 워킹트리를 안 건드리고 작업할 수 있다. 새 워크트리에는 `node_modules` 가 없어서 테스트가 `ERR_MODULE_NOT_FOUND` 로 죽는데, 공유 클론 것을 심볼릭 링크하면 된다(읽기만 하므로 안전, 커밋 전 링크는 지운다).

관련: [[rubato-bridge-auth-env]], [[rubato-update-tty-gated]], [[preserve-working-environment]]
