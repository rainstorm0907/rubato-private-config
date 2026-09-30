thread_id: 01a0a396-c7a2-7420-8aef-d722947e4ea6
updated_at: 2026-09-15T08:40:08+00:00
rollout_path: /Users/wooojin/.codex/sessions/2026/09/15/rollout-2026-09-15T14-42-42-01a0a396-c7a2-7420-8aef-d722947e4ea6.jsonl
cwd: /Users/wooojin

# Rubato 데스크톱 GUI 설치 및 stale queue 복구 PR

Rollout context: `/Users/wooojin/dev/Rubato`에서 기존 CLI 설정을 보존하면서 T3 기반 Rubato GUI를 설치하고 검증한 뒤, Maplog 세션의 stale queue 문제를 복구하는 PR을 만들고 CI 상태를 확인했다.

## Task 1: Rubato 데스크톱 GUI 설치

Outcome: success

Preference signals:
- 사용자는 “우리 세팅 그대로인지 확인”을 요청했고, 설치 전후 설정·인증·모델 저장소 해시를 비교하는 검증이 수행됐다. 비슷한 설치에서는 기존 개인 설정과 인증을 건드리지 않았음을 파일 기준으로 확인해야 한다.
- 설치 후 단순 프로세스 실행이 아니라 실제 앱 화면에서 기존 프로젝트·세션·모델 목록이 보이는지 확인했다. 사용자는 설치 성공을 실제 UI 상태로 확인하는 흐름을 선호한다.

Key steps:
- `/Users/wooojin/dev/Rubato`에서 `./install.sh --gui` dry-run으로 현재 경로가 구형 ChatGPT 런처가 아니라 핀된 T3 + Rubato overlay임을 확인했다.
- `bash harness/t3-integration/install-gui.sh --apply` 실행.
- T3 commit `3138f5716098a331f9a7d4cfc1bcd07118967a83` checkout, overlay·Rubato 아이콘·GUI 설정 적용, Electron 데스크톱 빌드 완료.
- `/Applications/Rubato.app`은 `/Users/wooojin/.rubato/t3-source/apps/desktop/.electron-runtime/Rubato.app`을 가리키며, `codesign --verify --deep --strict` 통과.
- GUI 전용 설정은 `~/.rubato/t3-home/userdata/settings.json`, Pi 프로필은 `~/.rubato-pi/agent`를 사용했다. 기존 CLI 설정 `~/.rubato/agent/*`와 `.zshrc` SHA-256은 설치 전후 동일했다.
- CUA로 실제 Rubato 창을 확인: 기존 `wooojin`, `maplog`, `keepitmello/rubato`, `maple` 프로젝트와 세션이 표시됐고 Rubato provider 및 모델 목록이 노출됐다.
- 관련 테스트는 12 pass / 3 skipped. 실제 모델 호출은 비용과 새 세션 생성을 피하기 위해 수행하지 않았다.

Failures and how to do differently:
- `cua.getApp("Rubato")` 첫 호출은 timeout이었지만 `cua.getState()`에서 `app.rubato.t3`가 실행 중임을 확인한 뒤 bundle ID로 재바인딩해 검증했다.
- `peekaboo`는 설치되어 있지 않아 사용할 수 없었다. CUA가 다시 실패하면 먼저 `cua.getState()`와 bundle ID를 확인하고, Peekaboo는 `--no-remote` fallback으로만 사용한다.
- GUI 기본 모델(`xai/grok-4.6`)과 CLI 기본 모델(`openai-codex/gpt-5.6-sol`)은 의도적으로 분리되어 있다. 이를 동일 설정으로 오해하지 않는다.

Reusable knowledge:
- 현재 GUI 설치 경로는 `harness/t3-integration/install-gui.sh --apply`이며, GUI 홈은 `~/.rubato/t3-home`, GUI Pi agent는 `~/.rubato-pi/agent`다.
- `write-gui-settings.mjs`는 GUI provider instance를 `rubato`로 만들고 기본 선택을 `xai/grok-4.6`으로 설정하며 내장 provider들은 비활성화한다.
- 기존 CLI 설정/인증을 보존했는지는 설치 전후 해시와 실제 UI의 프로젝트·세션 목록을 함께 확인해야 한다.

References:
- `/Users/wooojin/dev/Rubato/harness/t3-integration/install-gui.sh`
- `/Users/wooojin/dev/Rubato/harness/t3-integration/write-gui-settings.mjs`
- `/Users/wooojin/.rubato/t3-home/userdata/settings.json`
- `/Applications/Rubato.app`
- `codesign --verify --deep --strict /Applications/Rubato.app`

## Task 2: Maplog stale queue 복구 및 PR

Outcome: partial

Preference signals:
- 사용자는 개인 커밋·`v0.4+r2` 같은 기존 작업 보존 여부를 중요하게 봤고, 실제 작업에서도 기존 `Opus Selection Review` 세션과 사용자 변경을 삭제·덮어쓰지 않는 방향을 택했다.
- PR 상태가 불완전할 때 사용자는 “PR 쪽 확인 후 머지해도 되는지”를 구분해 묻는다. CI가 빨간 상태면 기술적으로 mergeable이어도 바로 머지하지 말고 외부 확인과 실패 원인을 분리해 제시해야 한다.

Key steps:
- 원래 Maplog 세션은 `database or disk is full` 이후 재개 시 `새 문맥 관리 확장이 준비되지 않았어요`로 반복 중단됐다.
- 기존 세션 `01a0993f-d6f1-799f-8e7a-f0defac63083`은 보존하고 새 `Maplog Movement Recovery` 세션 `01a0a42b-c9f9-7117-85c1-c9feca2e6b4b`을 생성했다.
- T3 stale queue 복구 변경을 `/Users/wooojin/dev/Rubato-pr-t3-queue`에서 커밋 `cbb13a29a578b25c73c4e44c41e22941f0e1dd7c`로 만들고 PR #12에 push했다.
- PR URL: `https://github.com/keepitmello/Rubato/pull/12`
- 변경 내용: pinned T3 source를 `cc839c42`로 올리고, `isStreaming=false && pendingMessageCount>0` 상태를 자동 삭제하지 않으며 Resume/Discard 선택을 제공하고, replay 실패 시 unsent queue를 유지한다.
- 로컬 검증: bridge test 27 pass, 전체 T3 integration 34 pass / 5 skipped, exact-source apply/idempotence/remove/dirty-guard 통과, typecheck·build·Codex audit 통과.
- 실제 Maplog 복구 세션에서 queue가 3개에서 0개로 정리되고 도구 실행이 계속되는 것을 확인했다. 원래 세션은 idle 상태로 보존됐다.
- PR의 `t3-integration`과 `codex-audit`는 통과했지만 `checkpoint`는 `harness/pi-server/test/restart-profile.test.mjs`의 기존 `reason: "no-pid"` 실패가 자동 재실행에서도 반복됐다. `stock-pi`는 마지막 확인 시 아직 pending/in_progress였다.

Failures and how to do differently:
- PR 본문에 CI note를 추가할 때 shell heredoc 안의 backtick이 명령 치환되어 문구가 손상됐다. 이후 quoted heredoc(`<<'EOF'`)로 본문을 다시 작성했다.
- CI checkpoint 실패는 PR 변경 파일과 무관한 `harness/pi-server` 재시작 테스트였지만, 빨간 체크를 임의로 무시하지 않고 PR 본문에 명시했다.
- 사용자의 마지막 질문 시점에는 PR이 `MERGEABLE`이지만 `mergeStateStatus=UNSTABLE`, checkpoint failure, stock-pi pending 상태였다. 따라서 “권한상 머지 가능”과 “지금 머지 권장”을 분리하고, stock-pi 완료·공식 확인·실패 허용 판단 후 머지하도록 안내했다.

Reusable knowledge:
- 기존 세션 파일과 개인 변경을 보존한 채 새 복구 세션을 만드는 방식이 문맥 확장 결함과 stale queue를 분리하는 안전한 우회였다.
- PR 검증 시 `gh pr view 12 --json ...`, `gh pr checks 12`, 실패 job 로그를 확인하고, 변경 파일 범위와 실패 job의 소유 영역이 겹치는지 판단해야 한다.
- 최종 rollout 시점에는 PR이 아직 merge되지 않았고, Maplog 복구 세션도 `running` 상태였다. PR을 merge하거나 앱을 재설치하면 실행 중 세션을 끊을 수 있으므로 작업 완료 후 처리해야 한다.

References:
- PR #12: `https://github.com/keepitmello/Rubato/pull/12`
- Commit: `cbb13a29a578b25c73c4e44c41e22941f0e1dd7c`
- Branch: `fix/t3-client-queued-messages`
- Original session: `01a0993f-d6f1-799f-8e7a-f0defac63083`
- Recovery session: `01a0a42b-c9f9-7117-85c1-c9feca2e6b4b`
- CI failure: `restart-profile.test.mjs`, `{"restarted":false,"reason":"no-pid"}`
