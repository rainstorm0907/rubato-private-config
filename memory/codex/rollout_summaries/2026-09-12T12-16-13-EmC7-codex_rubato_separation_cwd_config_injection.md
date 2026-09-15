thread_id: 01a0958b-f918-7ac2-abff-3059bed017d3
updated_at: 2026-09-12T12:26:34+00:00
rollout_path: /Users/wooojin/.codex/sessions/2026/09/12/rollout-2026-09-12T21-16-13-01a0958b-f918-7ac2-abff-3059bed017d3.jsonl
cwd: /Users/wooojin

# 일반 Codex와 Rubato Codex 분리 실행 경로를 조사함

Rollout context: 사용자는 로컬에 일반 Codex, Rubato Codex, Rubato 세 구성이 있다고 보고 순정 Codex만 실행하는 방법과 실제 설치 상태 확인을 요청했다. 작업 디렉터리는 `/Users/wooojin`, macOS zsh 환경이었다.

## Task 1: Codex/Rubato 설치 구조 확인 및 순정 Codex 실행

Outcome: partial

Preference signals:
- 사용자는 “일반 codex만 사용해보려면 어떻게 할까?”, “확인좀해줘”라고 요청하며 추측보다 실제 로컬 실행 파일·설정·프로세스 검증을 기대한다.
- 사용자가 직접 실행 후에도 Rubato 지침이 주입됐다고 알려주자, 원인 재조사와 검증을 요구하는 흐름이 됐다. 향후 설정 분리 안내는 반드시 실제 새 세션의 유효 지침과 플러그인 목록까지 확인해야 한다.

Key steps:
- 실행 파일 확인: `/opt/homebrew/bin/codex` (`codex-cli 0.154.0`), `omx` (`oh-my-codex v0.15.3`), `rubato`는 별도 바이너리가 아니라 zsh 함수/스크립트 경로였다.
- Rubato 관련 설치 확인: `~/.codex/config.toml`에 `model_instructions_file`, `openai_base_url=127.0.0.1:10100`, `rubato-codex@rubato` 플러그인, Rubato marketplace, taskforce agent 설정이 있었다. `~/.codex/rubato-codex`와 `~/dev/Rubato`도 존재했다.
- 초기 가설인 “별도 `CODEX_HOME`만 지정하면 완전 분리”는 `/Users/wooojin`에서 실행할 때 틀렸다. 새 홈으로 세션 파일은 분리됐지만 Rubato 플러그인과 지침이 역주입됐다.
- 원인은 시작 위치가 `/Users/wooojin`인 상태에서 홈 디렉터리의 프로젝트 범위 `.codex` 설정이 다시 발견된 것이었다. `CODEX_HOME`만 바꾸는 것으로는 해당 cwd의 프로젝트 설정 발견을 막지 못했다.
- `/tmp`에서 `CODEX_HOME=$HOME/App/codex-plain-home`으로 다시 검증한 결과: marketplace는 OpenAI curated remote만 보였고, Rubato 경로·플러그인·`model-instructions`·기존 hooks 경로가 유효 진단에 없었으며 MCP 서버는 0개였다.

Failures and how to do differently:
- 실패: `CODEX_HOME`만 바꾸고 `/Users/wooojin`에서 실행하도록 안내해 Rubato 설정이 계속 보였다. 다음에는 반드시 중립 cwd(`/tmp`) 또는 실제 프로젝트 cwd에서 실행하고, 홈 디렉터리 자체에서 Codex를 실행하지 말아야 한다.
- 실패: 첫 답변에서 “빈 CODEX_HOME이면 완전 분리된다”고 단정했다. Codex 설치판의 프로젝트 설정 탐색과 App/native hook 역주입 가능성을 먼저 검증해야 한다.
- 검증 중 `rm -rf`가 실행 정책에 의해 거부됐다. 임시 디렉터리 정리는 허용된 안전한 방식으로 하거나 정리 없이 일회성 디렉터리를 사용한다.
- `~/.zshrc` 출력에 장기 Anthropic 인증 토큰이 평문으로 노출되어 있었다. 값은 기억에 저장하지 않으며, 향후에는 즉시 폐기·교체하고 secret-bearing 설정을 출력/복사하지 않는다.

Reusable knowledge:
- 순정 Codex 실행의 검증된 형태:
  `cd /tmp`
  `CODEX_HOME="$HOME/App/codex-plain-home" /opt/homebrew/bin/codex`
- 공식 Codex 문서상 `CODEX_HOME`은 사용자 설정과 전역 `AGENTS.md`의 기준점을 바꾸지만, 현재 cwd에서 프로젝트 설정을 탐색할 수 있으므로 cwd도 함께 통제해야 한다.
- `codex plugin list`와 `codex doctor --json`을 중립 cwd에서 실행하면 유효 플러그인, config 경로, provider, MCP 수, Rubato 경로 포함 여부를 확인할 수 있다.
- 일반 Codex와 Rubato의 실제 구분은 다음과 같다: `codex`는 `/opt/homebrew/bin/codex` 실행 파일이며 기본 홈 설정에 Rubato가 결합되어 있고, `rubato`는 `~/.local/bin/rubato-personal`을 호출하는 별도 zsh 함수다.

References:
- `/Users/wooojin/.codex/config.toml`: `model_instructions_file`, `openai_base_url`, `[plugins."rubato-codex@rubato"]`, `[marketplaces.rubato]`
- `/Users/wooojin/.codex/rubato-codex/install-state.json`: `pluginSelector=rubato-codex@rubato`
- 검증 명령: `CODEX_HOME="$HOME/App/codex-plain-home" /opt/homebrew/bin/codex plugin list`
- 성공한 중립 cwd 검증 결과: `No Rubato paths found`, `MCP servers=0`, `model provider=openai`
- 공식 문서: `https://learn.chatgpt.com/docs/agent-configuration/agents-md`
