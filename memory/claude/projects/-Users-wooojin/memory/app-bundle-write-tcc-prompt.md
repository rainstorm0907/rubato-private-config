---
name: app-bundle-write-tcc-prompt
description: "앱 번들(/Applications/*.app) 안에서 파일을 만들면 macOS '앱 관리' 권한 팝업이 뜬다 — asar 추출은 스크래치패드에서 (2026-08-12)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 032b5d4e-00a4-41c3-be85-bfa5326dd0f5
  modified: 2026-08-12T04:19:10.991Z
---

`/Applications/*.app` 번들 **안쪽을 CWD로 잡고 파일을 쓰면** macOS가 "앱 관리"(Privacy & Security → App Management) 권한을 요구하는 팝업을 띄운다. 우진님이 이걸 싫어하심 — 갑자기 뜨면 원인 추적을 시켜야 해서.

**실제 사례 (2026-08-12):** Paseo 내부 동작 확인하려고
`cd /Applications/Paseo.app/Contents/Resources && npx @electron/asar extract-file app.asar <경로>` 실행.
`extract-file`이 CWD에 쓰기 때문에 번들을 수정하는 동작이 되어 팝업 발생.

**How to apply:** asar·zip·앱 리소스 추출은 **반드시 스크래치패드를 CWD로** 두고, 소스는 절대경로로 지정할 것.
```
cd "$SCRATCHPAD" && npx --yes @electron/asar extract-file /Applications/X.app/Contents/Resources/app.asar <내부경로>
```

**Why:** 권한을 켜서 해결하면 안 된다 — 켜는 순간 클로드가 `/Applications` 안을 수정할 수 있게 되어 앱 오염 위험이 생긴다. 꺼둔 채로도 읽기 작업은 전부 정상 동작한다.

**곁다리 사실:** 앱 관리 목록의 `2.1.xxx` 항목은 Claude Code 버전별 바이너리(`~/.local/share/claude/versions/`). macOS TCC가 코드 서명 identity 기준이라 버전마다 새 항목이 생기며 **하나로 통합 불가**. 옛 버전 항목은 죽은 값이라 `−`로 지워도 무방.

관련: [[preserve-working-environment]], [[paseo-mobile-setup]]
