---
name: claude-phone-remote-control
description: "클로드 폰 연동은 텔레그램 고정 슬롯(클롱이=상담, maplog_bot=maplog 세션), claude-cmux가 세션ID(--resume) 기준 매핑+슬롯 take-over (2026-07-12 surface→세션ID 전환)"
metadata: 
  node_type: memory
  type: project
  originSessionId: b0cab1aa-eaaa-4d77-bd38-5b5be5d15829
  modified: 2026-08-12T08:41:56.526Z
---

2026-07-04 확정: 폰 연동은 **텔레그램 고정 매핑** — cmux pane(surface) ID 기준으로 봇을 핀 고정. Remote Control(`/rc`)도 요건 충족 상태(2.1.200, OAuth)지만 우진님이 텔레그램 UX 선호로 이 방식 채택.

**구현 상태 (`~/.local/bin/claude-cmux`, 백업 `claude-cmux.bak-20260704`):**
- cmux가 모든 탭을 이 래퍼로 실행하며, 래퍼가 `CMUX_SURFACE_ID`로 고정 매핑:
  - `997709B9-8F4C-40CC-86C9-68C80721F577` → `~/.claude/channels/telegram-2` = **@maplog_bot** (봇명 "어플개발", maplog 작업 세션)
  - `63E689FB-F7F3-440B-B81C-0E524C6ADB55` → `~/.claude/channels/telegram` = **클롱이** (상담 세션, pane 제목 "클롱이")
- 매핑된 pane만 `--channels` 부착 + 폰으로 "🔗 연결됨" 알림(끄기: `CMUX_TELEGRAM_NO_HELLO=1`). 그 외 pane·비 cmux 실행은 텔레그램 없이 실행.
- 슬롯2 토큰 저장·getMe 검증 완료, access.json은 allowlist(7389033218) 시딩 완료 — 페어링 불필요.
- **2026-07-04 적용 완료**: maplog_bot 개통(Telegram.app에서 Start 클릭), 두 pane 모두 cmux CLI(`send`/`send-key`/`read-screen`)로 `/exit` 후 셸의 `"$CMUX_CLAUDE_WRAPPER_SHIM" --resume <id>`로 재시작(대화 유지, 셸에 CMUX_SURFACE_ID 있어 매핑 작동). 두 폴러 동시 가동 검증됨. 교훈: pane에 send 하기 전 read-screen으로 입력창 초안 여부 확인할 것(초안 위에 enter 보내면 그대로 전송됨).
- 구 브릿지 launchd `com.wooojin.claude-telegram-bridge`: bootout + plist `.disabled` rename + 로그 90MB truncate 완료.

**우진님 방침 (2026-07-04):** 폰/노트북을 채널별로 따로 대응하지 말 것 — 한 대화로 통합. 노트북(터미널) 세션이 본체, 텔레그램은 동일 내용의 미러. 어시스턴트 답변은 양쪽에 같은 내용 하나만 (미러 훅이 자동 처리, 수동 reply 턴은 훅이 스킵하므로 중복 없음).

**양방향 미러링 (2026-07-04 추가):** `~/.claude/hooks/telegram-mirror.py`가 user 전역 settings.json의 UserPromptSubmit/Stop 훅(async)으로 등록됨. 노트북에서 친 프롬프트는 **HTML 인용구(blockquote) 스타일**(우진님이 샘플 A/B/C 중 확정, 이모지 없음·html.escape 필수), 턴 마지막 어시스턴트 텍스트는 🤖 접두어 평문으로 그 세션의 봇에 전송. `TELEGRAM_STATE_DIR` 없는 세션은 무동작(매핑된 pane만 미러). 가드: 슬래시 커맨드 스킵, 텔레그램발 에코 스킵(`<channel ` + `source=` 포함 여부로 판정 — `source="plugin:telegram:telegram"`이라 좁은 매칭은 실패했었음), reply 툴 쓴 턴 스킵, `mirror.last` 해시로 resume 직후 Stop 재발화 중복 방지. 훅이 매 실행마다 스크립트를 새로 읽으므로 수정 시 세션 재시작 불필요. 하네스 주입 텍스트 필터(2026-07-04): `<task-notification>`은 XML 원문 대신 "⚙️ 요약 한 줄 + `<blockquote expandable>` 접힌 result 본문"으로 변환 전송, `<system-reminder>`/`<command-name>`/`<local-command*>`/`<teammate-message>`로 시작하는 프롬프트는 스킵 (우진님: 근거·중간과정은 좋지만 `<status>` 같은 태그 노이즈는 보이지 말 것). **Stop 레이스 픽스(2026-07-04 밤):** 툴 쓰는 턴에서 마지막 어시스턴트 텍스트가 아직 플러시 안 된 시점에 훅이 읽어 직전 텍스트를 오발송하던 버그 → 두 번 연속 동일하게 읽힐 때까지 0.5s 폴링(최대 ~3s) 안정화 대기 추가로 해결.

**Amphetamine 자동 깨움 (2026-07-04):** 로그인 시 무기한 세션 자동 시작 — `~/Library/LaunchAgents/com.wooojin.amphetamine-autostart.plist` + `~/.local/bin/amphetamine-autostart`. 앱 내장 "Start Session At Launch"는 MAS 버전에서 미작동(설정값은 정상 저장되나 무시됨)이라 AppleScript `start new session with options {duration:0, interval:0, displaySleepAllowed:true}`로 직접 시작. CDM(뚜껑 닫아도 깨움)·배터리 30% 미만 자동 종료는 기존 설정 그대로. 일시중지 = 알약 메뉴 → End Current Session. **맥이 잠들면 폰(텔레그램)으로 깨울 수 없음** — 연동은 맥이 깨어 있을 때만 동작, 잠든 사이 메시지는 텔레그램 서버에 보관됐다가 깨어나면 도착.

**매핑 방식 전환 = 세션 ID 고정 (2026-07-12, 백업 `claude-cmux.bak-20260712`):** surface ID 매핑이 cmux 재시작마다 ID가 바뀌어 뒤엉키던 문제 해결. 이제 래퍼가 **1순위로 `--resume <세션ID>` 기준 매핑**, surface는 2순위 폴백. 클롱이(상담)는 세션 ID `3f5bf72f-3f81-4c31-8446-0b23e0a5b58e`에 **영구 고정** → surface가 뭐로 바뀌든(예: 이날 A4424C2E로 드리프트) 텔레그램은 이 세션에만 붙고 다른 세션은 절대 못 가로챔. 추가로 **슬롯 take-over**: `--channels` 붙기 직전 `$dir/bot.pid`의 살아있는 폴러를 `kill -9`로 정리 → 재시작·중복 pane으로 폴러 2개 공존하던 409 뒤엉킴 방지(새 세션이 단독 소유). maplog(telegram-2)는 아직 surface 매핑(997709B9) 유지 — 필요시 그 세션ID도 `SLOT_BY_SESSION`에 추가하면 됨. **클롱이 세션 ID가 바뀌면**(새 대화로 갈아타면) 래퍼의 `SLOT_BY_SESSION` 값 갱신 필요.

**핵심 제약:** 봇 토큰 1개 = 폴러 1세션. 채널은 세션 시작 시에만 바인딩(실행 중 attach 불가, 공식 문서 확인) → 매핑/래퍼 변경 적용하려면 해당 pane 재시작 필요(cmux autoResume가 대화 유지).

**플러그인 전환 이후 실태 (2026-08-12 확인):** 이제 텔레그램은 공식 플러그인 `telegram@claude-plugins-official` 0.0.6이 담당. 핵심 함정: 플러그인 server.ts가 `TELEGRAM_STATE_DIR` env 없으면 **기본값 `~/.claude/channels/telegram`(=클롱이 슬롯)을 뭄** → 이 스왑 프로필(dalisalvador1231)로 새 세션이 뜰 때마다 최신 세션이 봇을 뺏어감(자체 stale-pid kill 로직으로 take-over). cswap 런치 경로는 claude-cmux 래퍼를 안 타서 SLOT_BY_SESSION도 env도 안 붙음. 대응:
- **미러 훅 폴백 (2026-08-12 패치)**: `telegram-mirror.py`가 env 없으면 `~/.claude/channels/mirror-map.json`에서 hook payload의 session_id로 state dir을 찾음. 미러(노트북→폰)는 훅이 직접 HTTP로 쏘므로 폴러와 무관하게 동작.

**근본 픽스 = mood 세션 자동 라우팅 (2026-08-12 저녁 구축):** "클롱이는 /mood 쓰는 세션이 자동 소유" 구조.
- **owner gate**: 플러그인 server.ts(0.0.6 캐시, 스왑 프로필 경로) 로컬 패치 — `~/.claude/channels/telegram/owner-session`에 적힌 **Claude 프로세스 PID**의 세션만 폴링 시작. 주인 아니면 대기(툴은 제공), 파일 삭제 시 stock 동작 복귀(=원라인 off 스위치). 주인이 바뀌면 5초 내 슬롯 양도. 세션 식별은 조상 프로세스 체인에서 claude PID 추출(ps 기반) — env에 세션 ID가 없어서 PID 방식 채택. **⚠️ 플러그인 업데이트(0.0.6→) 시 패치 유실 — 재적용 필요.**
- **자동 핀 훅**: `~/.claude/hooks/telegram-owner-pin.py` — PreToolUse(matcher=Skill, `~/.claude/settings.json` 등록, 스왑 프로필은 자동 동기화됨: 두 settings.json은 별개 파일인데 ~/.claude 편집이 스왑에 복제돼 중복 등록됐던 것 dedupe로 정리). Skill(mood) 호출 순간 그 세션의 claude PID를 owner-session에, session_id를 mirror-map.json에 기록 → 폴링·미러 모두 자동 승계. 새 상담 세션은 /mood 한 번이면 폰 연동이 따라옴(별도 /mcp 불필요 — 그 세션의 server.ts가 대기 중이다가 5초 내 시작).
- 백업: settings.json은 `.bak-ownerpin-20260812`, 플러그인 원본은 캐시 재설치로 복원 가능.

관련: [[codex-meight-global-setup]] (Amphetamine 상시 깨움은 코덱스 세팅 공용)
