---
name: codexbar-keychain-popup-fix
description: "CodexBar가 \"Claude Code-credentials\" 키체인 접근 팝업을 반복적으로 띄울 때의 영구 해결법"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 49e0796a-a3e2-4ca6-80ce-64c4b961b886
  modified: 2026-08-06T06:10:39.269Z
---

CodexBar(steipete, teamid Y5PE65HELJ)가 Claude 사용량을 보려고 macOS 키체인의 "Claude Code-credentials" 항목을 읽는데, Claude Code가 토큰 갱신할 때마다 그 항목을 다시 써서 ACL을 자기만 신뢰하게 리셋 → CodexBar 접근 시 "로그인 키체인 암호 입력" 팝업이 반복적으로 뜬다. "항상 허용"이나 `security set-generic-password-partition-list`로 teamid를 파티션 목록에 넣어도 Claude의 다음 갱신 때 되돌려져서 소용없다.

**함정 — `claudeOAuthKeychainPromptMode = never`만으로는 안 막힌다.** CodexBar는 토큰 읽기 경로가 2개다: (1) 앱 내부 Security.framework 읽기 → promptMode가 통제함, (2) `security` CLI를 자식 프로세스로 직접 실행 → promptMode 무시하고 OS 팝업이 뜬다. 팝업 아이콘이 CodexBar가 아니라 **터미널 `>_` 아이콘**이면 (2)번 CLI 경로가 범인이다.

**확실한 영구 해결:** 앱 완전 종료 후 아래를 메인 도메인과 앱그룹 컨테이너(`Y5PE65HELJ.com.steipete.codexbar`) plist 양쪽에 쓰고 재실행.
- `defaults write com.steipete.codexbar debugDisableKeychainAccess -bool true`  ← 마스터 킬스위치, 모든 경로 차단
- `defaults write com.steipete.codexbar claudeOAuthKeychainReadStrategy -string securityFramework`  (CLI 경로 제거)
- `defaults write com.steipete.codexbar claudeOAuthKeychainPromptMode -string never`
검증: 재실행 후 `pgrep -lf "SecurityAgent|/usr/bin/security"` 로 몇 초 감시해 팝업/`security` 호출이 안 뜨는지 확인. 본체+위젯이 각각 읽어 팝업이 2개씩 뜨므로 앱그룹 plist에도 반드시 같이 쓸 것.

**트레이드오프:** never면 CodexBar가 키체인을 안 읽어서 Claude 구독 사용량 %·리셋 타이머 실시간 갱신은 끊긴다. 단, 로컬 로그(`~/.claude/projects/*.jsonl`)로 토큰/비용 사용량은 계속 표시됨. 구독 %를 다시 보려면 정책을 `onUserAction`/`always`로 되돌리면 된다.

**대체 경로와 그 함정(2026-08-06 확정):** 구독 % 는 키체인 대신 `~/.codexbar/config.json`의 `tokenAccounts`(bare access token) 로 살린다 — `~/.claude/shell/codexbar-claude-sync.py` + launchd `com.wooojin.codexbar-claude-sync`가 5분마다 프로필별 토큰을 복사한다. **함정: CodexBar.app은 config.json을 실행 시 한 번만 읽고 파일 감시를 안 한다**(바이너리에 FSEvents/kqueue 없음, 앱 내 "새로 고침"·⌘R도 캐시된 토큰 재사용). 그래서 토큰이 ~8시간마다 회전하면 실행 중인 앱은 죽은 토큰에 고정돼 "Claude OAuth request unauthorized"만 띄우고, 같은 config를 매번 새로 읽는 `codexbar` CLI는 멀쩡한 비대칭이 생긴다. 해결: 동기화 스크립트가 토큰이 실제로 바뀐 회전 때만 앱을 graceful quit → config 기록 → `open -g` 재실행 한다. quit을 먼저 해야 한다 — 앱이 종료하면서 config.json을 자기 값으로 덮어쓴다. 진단 지표는 `~/Library/Application Support/com.steipete.codexbar/history/claude.json`의 마지막 `capturedAt`(계정 키는 토큰이 바뀔 때마다 새로 생겨서 구간이 ~8h로 끊긴다).

미사용 프로필(cswap sub 등)은 access token이 만료돼도 갱신할 수단이 없어서 계속 401이다. 그 프로필로 `claude`를 한 번 돌리는 것 말고는 방법이 없다(스크립트는 refresh token 소각 위험 때문에 의도적으로 갱신을 안 한다).
