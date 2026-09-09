---
name: codex-meight-global-setup
description: 코덱스 쓰라고 하면 무조건 keepitmello/claude-codex-meight 전역세팅 + meight로 위임
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ac1da58d-53e4-48d3-8e3f-4b031718d118
---

우진님이 "코덱스 사용/상의/위임" 류로 지시하면, 무조건 `https://github.com/keepitmello/claude-codex-meight`(meight) 방식으로 전역세팅하고 그걸 통해 코덱스를 구동한다.

**Why:** 우진님이 명시적·항구적으로 "무조건"이라고 지정한 코덱스 사용 방식. 기존 [[browser-automation-policy]]처럼 매번 묻지 말고 이 세팅을 기본값으로 적용한다.

**How to apply:**
- 전역세팅 구성요소(2026-06-16 설치, 2026-07-03 upstream 0743e6b로 갱신): ① `~/.local/share/claude-codex-meight` 클론 + `install.sh` → `~/.local/bin/meight` CLI(+`.venv`, SDK `openai-codex==0.1.0b3`), ② `skills/meight` → `~/.claude/skills/meight` + 신규 `skills/meight-worker` → `~/.codex/skills/meight-worker`(워커측 계약), ③ 전역 gitignore(`~/.gitignore`)에 `.meight/`, ④ 오케스트레이터 정책을 `~/.claude/CLAUDE.md` "Codex Orchestration (meight)" 섹션으로 통합, ⑤ LaunchAgent `com.keepitmello.meight` 설치·로드(데몬 상시 유지 — `start`는 dispatch와 달리 데몬 자동기동 없음).
- 전제: codex CLI + python3≥3.10 (둘 다 충족). 미설치 머신에서 다시 트리거되면 위 5단계를 재실행.
- 구동(2026-07-14 v3 계약, upstream ac411d2): `start`/`dispatch`에 `--mode collab|delegate`와 **`--role mate|worker` 둘 다 필수**(기본값 없음, teaching error). mate=도전·리뷰·컨설트(plan 리뷰·적대 리뷰), worker=구현·검증, 역할과 모델은 직교. 위임 구현/리뷰 = `--role worker --mode delegate --report decision`, 상의/설계/진단 = `--role mate --mode collab --sandbox ro`. 사소·단발 = `dispatch`, 그 외 = `start`+`wait --timeout` + `status`/`steer`. `wait` exit: 0완료·1체크포인트·2실패/중단·3질문(reply 가능)·4데몬사망.
- v3 추가(2026-07-14): 모델 별칭 sol/terra/luna 자동 정규화(gpt-5.6-*), effort에 ultra/max 추가(SDK enum 런타임 완화), 데몬 capabilities=["role"] 핸드셰이크(구 데몬이면 "daemon predates --role; restart required"), 워커에 computer-use 승인 자동수락 브리지 상시 설치(⚠️ 워커가 사람 승인 없이 데스크톱 앱 접근 — 민감 작업 브리프에 화면 사용 금지를 명시할 것), SDK 내장 런타임 대신 시스템 codex CLI 사용(MEIGHT_CODEX_BIN 재정의 가능). 스킬 3분할: skills/meight(디스패처)→`~/.claude/skills/meight`, mate/worker/common 계약은 레포 SSOT 경로가 프리앰블에 직접 주입(`~/.codex/skills` 사본은 참고용). 라우팅: [[fable-token-routing-policy]] — Maplog=Terra 유지, 타 프로젝트 Luna xhigh 시험(우진님 확정), sol effort 기본 high.
- 로컬 커밋 984cb36은 `backup/pre-v3` 브랜치+fork 원격에 보존(내용은 upstream e65173a로 흡수). 우진님 git 훅이 내 Bash의 checkout/switch/reset --hard를 차단 — 이 레포의 브랜치 이동은 우진님이 `!`로 직접 실행해야 함.
- 리뷰 독트린(구버전과 다름 주의): 구현자 셀프리뷰 금지가 원칙, 기본은 신규 코덱스 리뷰 워커. 교차모델(Claude reviewer 에이전트)은 중요 작업의 추가 관점. 워커는 브리프가 허용하면 검증된 결과를 커밋/푸시 가능(최종 통합·승인은 Claude).
- `meight.py` 변경 후엔 데몬 재시작 필수(런타임이 데몬 프로세스에 상주). 워커 질문은 `QUESTION:`+`TARGET: dispatcher|user` 구조 — user 소유 종류(scope/ux/priority/risk/irreversible/acceptance)는 우진님께 그대로 에스컬레이션.
- 단발 가벼운 상의/리뷰는 기존 [[codex-discusser]]/codex-reviewer 스킬로도 가능하나, "위임/감독/병렬"은 meight.
- 함정 ①(2026-07-04): codex 자격증명이 서버에서 revoke되면 워커가 시작 5~7초 만에 "refresh token was revoked"로 죽는데, `codex login status`는 stale auth.json을 읽어 "Logged in"으로 **거짓 표시**한다. 진단은 워커 events.log, 복구는 `codex logout` → `codex login`(브라우저, 우진님만 가능).
- 함정 ②(2026-07-04): ro 워커에서 코덱스측 OMX ultrawork 상태(active/planning)가 stop hook을 반복 유발 — 집중 verify도 15분+/입력 수백만 토큰으로 부풂. 워커가 .omx 상태를 못 고치면 needs_input(QUESTION)으로 끝나는데, 이건 코드가 아니라 하니스 정리 질문이므로 결론(VERDICT)이 이미 나왔으면 `meight interrupt`로 닫는 게 맞다. reply로 턴을 더 돌리면 같은 루프에 다시 빠진다.
- **함정 ② 근본 해결(2026-07-04 적용)**: `~/.codex/hooks.json`의 OMX(oh-my-codex) 훅 5개 엔트리에 `[ -n "$MEIGHT_HOME" ] && echo '{}' || node <omx-hook>` 가드 — meight 워커에만 OMX 훅 전체 스킵. 원리: launchd plist가 데몬에 `MEIGHT_HOME` 주입 → SDK가 `os.environ.copy()`로 워커에 상속 → 일반 셸/코덱스 세션엔 이 변수 없음(검증됨). 백업 `hooks.json.bak-20260704`. 주의: 데몬을 launchd 없이 수동 실행하면 MEIGHT_HOME이 없어 가드 미작동. OMX를 npm 업데이트해도 hooks.json 가드는 유지되나, OMX 재설치가 hooks.json을 다시 쓰면 가드 재적용 필요.
- 데몬 재시작(`launchctl kickstart -k`)은 활성 워커(codex 자식)까지 죽인다 — 재시작 전 `pgrep -P <데몬pid>` + `meight status`로 실행중 워커 확인·정리 먼저 (2026-07-04 recap-verify를 실수로 끊은 교훈; 결론은 result.md에 남아 있었음).
