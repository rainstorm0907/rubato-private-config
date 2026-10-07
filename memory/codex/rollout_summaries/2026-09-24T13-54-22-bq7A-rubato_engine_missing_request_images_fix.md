thread_id: 01a0d3b2-2599-7122-8d6c-c4c0b2124586
updated_at: 2026-09-24T14:00:42+00:00
rollout_path: /Users/wooojin/.codex/sessions/2026/09/24/rollout-2026-09-24T22-54-22-01a0d3b2-2599-7122-8d6c-c4c0b2124586.jsonl
cwd: /Users/wooojin/App/maplog
git_branch: main

# Rubato 최신 엔진 누락 수정 및 개인 설정 보존 검증

Rollout context: `/Users/wooojin/dev/Rubato`에서 Rubato가 시작 단계 `ERR_MODULE_NOT_FOUND`로 망가진 상태를 조사하고, 최신 소스에 맞추되 개인 설정·확장·GUI 오버레이를 보존하는 작업을 수행했다.

## Task 1: Rubato 엔진 및 GUI 복구

Outcome: success

Preference signals:
- 사용자는 “최신 업뎃대로 맞추면서 개인 오버레이는 냅두고”라고 요청했다 -> 업데이트 시 개인 설정, 확장, 오버레이, 세션을 명시적으로 보존하고 전후 상태를 검증해야 한다.
- 설치 성공을 프로세스 실행만으로 간주하지 않고 실제 Rubato 창과 기존 프로젝트·세션·모델 목록으로 확인하는 흐름이 적합하다.

Key steps:
- 저장소는 `rubato/base`와 `origin/rubato/base`가 동일한 최신 커밋 `41ab706d49c7`였고, GUI 번들은 T3 upstream `c14f6015...`에 맞아 있었다.
- 시작 실패 원인은 최신 커밋에서 `request-images.mjs`가 추가됐지만 패키징 목록 `harness/pi-runtime/features/context-notes/patches.mjs`에 빠져 설치 엔진에서 모듈이 누락된 것이었다.
- `contextNoteSources`에 `request-images.mjs`를 한 줄 추가했다.
- 관련 테스트 9개 통과, 엔진 재빌드 후 설치본에서 파일 존재 및 `controller.mjs` 실제 import 성공.
- `rubato restart`로 프로필 엔진·remote hub·GUI를 재기동했고, GUI가 자동으로 닫힌 뒤 `open /Applications/Rubato.app`으로 다시 열어 실제 창을 확인했다.
- 브리지 `connected`, 모델 카탈로그 22개 로드, Rubato 창에서 기존 프로젝트·세션과 Opus 5.5 표시를 확인했다.
- 개인 설정·모델 저장소·확장 등 19개 파일의 전후 SHA-256 manifest가 동일했다.
- `/Applications/Rubato.app` codesign 검증 통과.

Failures and how to do differently:
- 최초 `rubato --help`도 엔진의 누락 모듈 때문에 실패했다. 소스가 최신인지보다 설치된 실행 엔진의 source fingerprint와 패키징 closure를 먼저 확인해야 한다.
- `rubato restart` 자체는 성공했지만 GUI 창은 재시작 직후 닫힌 상태였다. 재시작 성공 문구만 믿지 말고 프로세스, bridge catalogue, 실제 GUI accessibility tree를 확인한 뒤 필요하면 앱을 명시적으로 다시 열어야 한다.
- 최종 작업 트리에는 `harness/pi-runtime/features/context-notes/patches.mjs`의 한 줄 수정이 커밋되지 않은 채 남았다. 자동 업데이트는 dirty tree에서 멈출 수 있으므로 후속 커밋 또는 별도 정리가 필요하다.

Reusable knowledge:
- Rubato CLI는 `/Users/wooojin/.local/bin/rubato`를 통해 `harness/scripts/rubato-pi.sh`를 실행하고, 실제 엔진은 `~/.rubato-pi/stock-engine`에 설치된다.
- 개인 확장은 `harness/scripts/install-extensions.sh`가 기본적으로 기존 파일을 유지한다. 개인 보존 검증은 `~/.zshrc`, `~/.rubato/agent`, `~/.rubato-pi/agent`, `~/.rubato/t3-home/userdata/settings.json` 및 확장 파일의 전후 해시로 수행한다.
- GUI 앱은 `/Applications/Rubato.app` 링크가 `~/.rubato/t3-source/apps/desktop/.electron-runtime/Rubato.app`을 가리키며, GUI 전용 데이터는 `~/.rubato/t3-home`, GUI Pi 프로필은 `~/.rubato-pi/agent`, 기존 CLI 프로필은 `~/.rubato/agent`에 분리된다.

References:
- 수정 파일: `/Users/wooojin/dev/Rubato/harness/pi-runtime/features/context-notes/patches.mjs`
- 오류: `Cannot find module .../dist/rubato-features/context-notes/src/context-notes/request-images.mjs`
- 검증 명령: `node --test harness/rubato-pi/test/unit/context-notes-request-images.test.mjs harness/pi-runtime/features/context-notes/context-notes.test.mjs`
- 엔진 재빌드: `node harness/scripts/build-active-engine.mjs --force`
- 재기동: `rubato restart`
- GUI 검증: `codesign --verify --deep --strict /Applications/Rubato.app`
