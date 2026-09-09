---
name: moonlight-remote-control-limits
description: 문라이트 스트림 안으로는 computer-use 타이핑이 깨짐, 파일은 LAN HTTP로 넘길 것
metadata:
  type: feedback
---

문라이트로 윈도우 PC를 조작할 때 computer-use의 **키보드 입력은 쓸 수 없다** (2026-08-21, 4회 이상 실패 확인). 영문 문장은 전부 □로 렌더되고, `abc123`은 키업이 유실돼 `a`가 수백 개 찍혔다. 숫자 키 하나는 통과하지만 문자는 안 된다. IME 문제가 아니다(트레이가 영문 A 상태였음). 마우스는 정상.

**Why:** 여기서 시간을 많이 버렸다. 타이핑으로 뚫으려는 재시도가 가장 비싼 실패였다.

**How to apply:**
- 파일 전달은 맥에서 `python3 -m http.server 8000 --bind 0.0.0.0` 띄우고 윈도우에서 `iwr http://<맥IP>:8000/파일 -o 파일`. 끝나면 서버 반드시 종료.
- 긴 명령은 내가 치지 말고 우진님께 드려서 직접 치시게 한다 (우진님 키보드는 정상 동작).
- 마우스 좌표가 어긋나면 문라이트 설정 "게임 대신 원격 데스크톱에 맞게 마우스 최적화"(`absmouse`) 를 켠다. **원래 값은 키 자체가 없음(꺼짐)** 이므로 되돌릴 때는 `defaults delete com.moonlight-stream.Moonlight absmouse`. 반드시 문라이트를 완전히 종료한 뒤에 해야 반영된다(cfprefsd 캐시). 스트림 중이면 SIGTERM을 무시하므로 `kill -9`가 필요할 수 있다.
- 잘못 입력된 텍스트 지우기: `ctrl+shift+end` → `backspace`. (`ctrl+a`·`delete`는 안 먹음)

[[preserve-working-environment]] [[afk-macro-windows]]
