---
name: paseo-mobile-setup
description: "Paseo(폰 원격 코딩) 2026-08-07 설치 완료 — launchd 데몬 소유, 앱 종료해도 터미널 생존, cmux는 자리용/Paseo는 외출용"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4903e825-512d-4695-a848-b6ceb434fcd1
  modified: 2026-08-06T15:53:14.532Z
---

2026-08-07 설치 완료. `brew install --cask paseo` (0.2.5) + `~/Downloads/paseo-setup-kit.zip` 킷 실행.

**구조:** 데몬 소유자가 앱이 아니라 launchd(`~/Library/LaunchAgents/sh.paseo.daemon.plist`).
앱 설정 `manageBuiltInDaemon: false`로 앱을 순수 클라이언트화 → Cmd+Q 해도 데몬 PID 유지되고 돌던 터미널·claude가 살아남는다(실측 검증). 앱(약 680MB) 안 띄워도 폰 연결 유지, 데몬만 약 160MB.

**설치 시 밟은 함정:** 킷 `install.sh`가 `command -v claude`로 경로를 찾는데, 우진님 zsh에는 `alias claude='claude --dangerously-skip-permissions'`가 있어서 alias 정의 문자열이 그대로 잡힌다. `unalias claude 2>/dev/null; command -v claude`로 고쳐서 실행함(실제 경로 `~/.local/bin/claude`). 킷을 다시 풀어 쓸 일이 있으면 같은 수정 필요.

**보안상 알아둘 것:** Paseo **에이전트** 모드는 provider command로 절대경로를 직접 실행해서 alias 미적용(권한 확인 정상 작동). 하지만 Paseo **터미널**은 로그인 zsh라 alias가 살아 있어서, 폰에서 `claude` 치면 `--dangerously-skip-permissions`로 뜬다.

**주요 경로/명령:**
- 설정 `~/.paseo/config.json` (webUi 켬, listen 127.0.0.1:6767 — 외부 노출 포트 없음)
- 웹 UI `http://127.0.0.1:6767/`, 폰 페어링 `paseo daemon pair` (QR은 비밀번호 취급)
- 데몬 정지 `launchctl bootout gui/$(id -u)/sh.paseo.daemon` — `paseo daemon stop`은 launchd가 되살림
- 롤백: 킷의 `uninstall.sh`, 백업 `~/.setup-backups/paseo-kit-20260807-005137`
- cmux에 명령 2개 병합됨(`Paseo Workspace`, `Paseo: List Agents`) — cmux.json의 `paseo-kit managed block`

**역할 분담:** 자리에선 cmux, 외출하면 폰 Paseo. 세션은 자동 공유가 아니라 `paseo import <session-id>`(일반→Paseo, 메시지 방식이 됨) 또는 `claude --resume [--fork-session]`(Paseo→일반)으로 옮겨 탄다. 길게 돌 작업은 처음부터 Paseo 터미널에서 시작하는 게 전환 비용이 없다.

릴레이(`relay.paseo.sh`)는 제3자 서버 경유. 맥이 잠들면 폰에서 안 보이는데, [[claude-phone-remote-control]]의 Amphetamine 상시 깨움 설정이 이미 그 조건을 만족시켜 준다.

관련: [[claude-phone-remote-control]] (텔레그램 고정 매핑 — 알림·짧은 지시용으로 여전히 유효), [[codex-meight-global-setup]]
