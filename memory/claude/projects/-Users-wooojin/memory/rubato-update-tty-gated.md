---
name: rubato-update-tty-gated
description: "rubato update는 tty 없으면 안내만 하고 빠진다, 게다가 실행 비트가 빠지면 알림 자체가 조용히 죽는다, 가끔 --yes로 직접 돌려야 함"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7002d851-1b9d-4eaa-9389-cff6aca1539a
  modified: 2026-08-29T05:10:00.000Z
---

`rubato-update.sh` 는 `MODE != yes` 이고 tty 가 없으면 "비대화 환경입니다. 받으려면: rubato update --yes" 만 찍고 `exit 0` 한다. **세션 시작 때 백그라운드로 도는 자동 업데이트는 알림만 하고 절대 적용하지 않는다.**

여기에 로컬 전용 커밋이 쌓이면 `git merge --ff-only` 가 영영 성립하지 않아 뒤처짐이 누적된다. 2026-08-28 에 origin 보다 **10 ahead / 15 behind** 인 채로 발견했고, 그날 하루 종일 쫓은 버그(브리지 증발, 컴팩션 `stopReason: toolUse`)가 **둘 다 업스트림엔 이미 고쳐져 있었다.** 낡은 코드를 디버깅하느라 하루를 썼다.

**증상을 만나면 업스트림 상태부터 확인한다.** `git rev-list --left-right --count HEAD...origin/rubato/base` 와 `ls patches/` 아래 패치 파일 이름. 패치 이름이 증상을 그대로 적어 두는 편이라(예: `compaction-toolcall-retry-without-tools`) 거기서 바로 걸린다.

`rubato update --yes` 는 안전하게 설계돼 있다. 더티 파일을 stash 했다가 되돌리고, 로컬 커밋은 `rubato/update-backup-<ts>-<pid>` 브랜치로 남긴 뒤 `reset --hard origin` 한다. 다만 **stash pop 이 충돌하면 거기서 멈추고 재빌드를 건너뛴다.** 워킹트리가 업스트림보다 여러 세대 낡았으면 pop 은 거의 확실히 충돌하므로, **돌리기 전에 내가 먼저 stash 해서 트리를 비우는 편이 낫다.** 그러면 업데이터는 stash 단계를 아예 건너뛴다.

**알림이 아예 안 뜨는 더 조용한 고장이 하나 더 있다.** `rubato-pi.sh` 는 업데이트 체크를 `[ -x ... ]` 로 가드한다. `rubato-update.sh` 가 `100644` 로 커밋되면(업스트림 `d227889a0`, 2026-08-26) 그 가드가 거짓이라 `--check` 가 통째로 건너뛰어지고, `rubato update` 서브커맨드는 "Permission denied" 로 끝난다. **뒤처져 있다는 신호 자체가 사라진다.** 2026-08-29 에 그렇게 28 커밋 밀린 채로 발견했다. 확인은 `ls -l harness/scripts/rubato-update.sh`, 복구는 `chmod +x` 와 `git update-index --chmod=+x` 를 함께.

**업데이트해도 돌고 있는 세션은 옛 코드다.** `node_modules` 는 프로세스 기동 때 메모리로 올라간다. 벤더 패치를 받으려면 세션을 한 번 재시작해야 한다.

관련: [[rubato-direct-provider-cutover]], [[shared-rubato-clone-hazard]], [[codex-meight-global-setup]]
