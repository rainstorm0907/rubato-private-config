---
name: afk-macro-windows
description: 자리비움 방지 매크로가 게임에 먹히려면 관리자 터미널 필수, 입력 방식 6종 --backend/--probe
metadata:
  type: project
---

`~/Downloads/woojin_codex_test_windows.py` (윈도우 PC에서는 `m.py`). 2026-08-21 기준 동작 확인됨.

게임이 키를 안 받던 원인은 **입력 방식이 아니라 권한**이었다. 게임이 관리자 권한으로 돌고 있어서, 일반 권한 프로세스가 보낸 SendInput을 윈도우(UIPI)가 조용히 버렸다. SendInput 공식 문서에 "반환값도 GetLastError도 UIPI 차단을 알려주지 않는다"고 명시돼 있어 스크립트 쪽에서는 성공으로 보인다. 파워셸이 키를 받은 건 파워셸이 같은 권한 수준이라 벽을 안 탔을 뿐.

**How to apply:** 실행은 반드시 시작 버튼 우클릭 → 터미널(관리자) → `python m.py`. 기본 입력 방식은 `scan`(가상키+스캔코드). 다른 방식이 필요하면 `--backend {scan,scancode,vk,keybd,post,send}`, 어느 게 먹는지 모를 때는 `--probe`(관리자 터미널에서, 기존 실행 중인 복사본 먼저 Ctrl+C — 단일 실행 잠금이 있어 두 번째는 바로 종료됨). 단축키는 왼쪽Ctrl+왼쪽Alt+F8 일시정지 / F9 종료.

합성 입력임을 숨기는 방향(Raw Input hDevice 위장 등)은 구현하지 않기로 선을 그었다. [[verify-before-done]]
