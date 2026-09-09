---
description: 이 Mac 고유의 CLI·도구 설정과 알려진 함정.
---
이 Mac 고유의 개발 환경 사실. `~/.codex/memories`에서 옮겨왔다. 도구 업데이트로 재발할 수 있어 재확인이 필요하다.

## 홈 디렉토리 배치

- 포트폴리오 폴더 정본은 `~/포트폴리오` (한글 이름 — `portfolio`/`resume` 영문 검색에 안 걸린다). 대회·프로젝트별 하위 폴더(Cofathon-2026, openaigame-2026)에 결과 보고서를 넣는다. `~/portfolio`를 새로 만들지 않는다.
- 포트폴리오·이력서·지원서·과거 프로젝트 성과가 필요한 작업에서는 `msearch`로 이 위치를 찾은 뒤 `/Users/wooojin/포트폴리오/INDEX.md`부터 읽는다. 관련 프로젝트의 `요약.md`, 필요한 근거 파일 순서로만 좁혀 들어가고 폴더 전체를 한꺼번에 읽지 않는다. 이미지와 PDF도 요청에 직접 필요할 때만 연다.

## Claude / Codex

- Claude Code를 Google·claude.ai 로그인 전용 상태로 만들려면 `~/.claude/anthropic.env`의 `ANTHROPIC_API_KEY` 주입과 `~/.claude.json`의 `customApiKeyResponses`를 **둘 다** 제거해야 한다.
- Codex↔Claude 스킬 이식 시 도구명이 다르다. Claude의 위임은 `Agent`(Codex의 `Task`가 아님), `meight`는 Codex worker 라우팅, `consult`는 외부 고품질 검토.
- `~/.claude/skills` 직접 쓰기가 보안 경계로 차단될 수 있다. 허용된 staging(`Downloads/...`)에 먼저 쓰고 옮긴다.

## GitHub 계정

- 이 노트북의 GitHub 계정은 `rainstorm0907`이며 `keepitmello/Rubato` 권한은 READ다. `keepitmello/Rubato` 관리자 계정은 mello가 있는 다른 노트북에 있으므로, 이 노트북에서 그 계정으로 인증을 바꾸거나 `origin/rubato/base` 직접 push를 시도하지 않는다.

## Aside / 브라우저

- macOS Aside 내장 `rg`가 quarantine 때문에 반복 보안 경고를 내면, 원본을 백업하고 해당 경로를 Homebrew `rg`로 심볼릭 링크 교체하면 해결된다. Aside 업데이트 시 재발 가능. `spctl`은 `/usr/sbin/spctl` 경로를 쓴다.

## Karabiner

- Varmilo 규칙 충돌로 한영·Rectangle·`⌘⇧3`이 동시에 깨지면, 새 규칙을 얹지 말고 가장 가까운 정상 자동 백업으로 롤백한다. 설정은 `~/.config/karabiner/karabiner.json`, 백업은 `automatic_backups/`.
- 2026-09-01, `TFG24F14V`는 Mac DisplayPort·Windows HDMI 1로 연결했다. DDC 밝기 쓰기는 동작하지만 입력 선택 VCP `0x60`은 표준 HDMI 1 코드 `17`, 대체 코드 `4`, 자체 후보 `1·2·3`을 모두 무시하고 현재값 `7`을 유지했다. BetterDisplay·m1ddc 양쪽에서 재현돼 소프트웨어 DDC 입력 전환은 이 모니터에서 불가로 판정했고, 실패한 Karabiner 단축키는 제거했다. `hardwarePowerOff`로 DP를 끊으면 HDMI로 자동 전환되지 않고 모니터가 꺼지며, BetterDisplay Pro가 없어 소프트웨어 재연결도 불가했다.
- DP로 돌아올 때 어두워진 원인은 BetterDisplay가 `TFG24F14V`에 저장한 combined brightness 15%·software brightness 30%를 재적용했기 때문이다. 2026-09-01 두 값을 100%로 저장해 재연결 디밍을 제거했다. 이 모니터 자체 OSD에는 입력 소스 단축 버튼이 없으므로 한 번에 전환하려면 외장 DP 스위치/KVM이 필요하다.

## 리서치 라우팅

- Sol이 최종 비교·판단, Consult(Aside 기반 ChatGPT)는 좁은 공개 판단, Grok+Aside 네이티브 실행기는 넓은 공개·로그인 브라우저 탐색과 정확한 클릭까지 수행한다.
- Grok provider는 `xai-grok-oauth`/`grok-4.6`. `xai/grok-4.6`은 실패한다.
- 별도 중복 스킬이나 자동 체이닝은 만들지 않기로 확정했다.
