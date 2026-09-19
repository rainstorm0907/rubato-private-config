---
name: checkup
description: "우진이 필요할 때 원문 세션을 싸게 찾아 읽는 수동 도구. /checkup, '정기점검', 또는 특정 세션·기간 분석 요청으로만 실행. 환경 점검·교훈 저장은 그 요청이 있을 때만."
disable-model-invocation: true
---

# Checkup — 세션을 싸게 읽는다

원본 transcript를 통째로 LLM에 읽히지 않는다. 압축은 로컬 스크립트(토큰 0), 대량
읽기는 저비용 모델, 판단은 이 세션이 한다. 결론을 바꿀 발화·승인·실패 원인은 요약이
아니라 원문의 해당 구간(앞뒤 포함)으로 돌아가 확인한다. 요약에 없다고 원문에 없던
사실로 취급하지 않는다.

## 0. 범위

우진이 지정한 세션·기간·질문이 범위다. 지정이 없는 정기점검만
`~/dev/claude-ops/state/checkup.json`의 `last_run` 이후를 대상으로 한다.
현재 세션·서브에이전트 로그·상담 자료(`~/mood`)는 요청 없이 넣지 않는다.

세션 원문 위치:
- Rubato: `~/.rubato-pi/agent/sessions/*.jsonl` (`*-artifacts/`는 도구 출력)
- Claude Code: `~/.claude/projects/**/*.jsonl` (`subagents/` 제외)
- Codex: `~/.codex/sessions/`

## 1. 다이제스트 (토큰 0)

```bash
python3 ~/dev/claude-ops/bin/digest.py <transcript.jsonl> <out.md>            # 사용자 발화 + 답변 꼬리 + 툴 에러
python3 ~/dev/claude-ops/bin/digest.py --mode workflow <transcript.jsonl> <out.md>  # 지시별 반응·대상 파일까지
```

출력은 `~/dev/claude-ops/state/digests/checkup/YYYYMMDD/<세션ID 앞8자>.md`. 두 형식(Rubato·Claude Code)
모두 읽힌다(2026-09-19 확인). 짧고 범위가 분명한 세션은 다이제스트 없이 직접 읽는 게 더 싸면 그렇게 한다.
지정한 세션은 짧아도 읽고, 발화 수 필터는 지정 없는 정기점검의 대량 선별에만 적용한다.

## 2. 대량 추출 (필요할 때만)

다이제스트가 많을 때만 저비용 모델(현재 `meight ... --model luna --effort xhigh`)에
15~20개씩 묶어 넘긴다. 돌려받을 것은 질문에 필요한 사건·발화·근거 원문·세션 파일명과
위치다. 매 발화에서 교훈을 짜내거나 후보 수·기각 비율을 채우게 하지 않는다.

## 3. 답한다. 기록은 요청 범위에서만

읽은 목적에 맞춰 답한다. 교훈 회수·기억 갱신까지 요청받았을 때만 승격을 판단한다:
화자·상황·이후 정정·현재 상위 지침을 확인하고, 원문을 확인 못 한 것은 확정 규칙으로
올리지 않는다. 기각 기준은 기존과 같다 — 이미 있는 항목(→ 기존 파일 갱신), 헌장이 이미
커버, 일회성 사건, 레포 문서가 정본인 제품 규칙.

환경 점검(`python3 ~/dev/claude-ops/bin/doctor.py`)은 요청했거나 도구가 고장 났을 때만.
doctor는 수리하지 않는다.

`last_run`은 지정 없는 정기점검을 끝까지 돌렸을 때만 실행 시작 시각으로 갱신한다.
특정 세션 읽기나 중간에 막힌 실행은 갱신하지 않는다.

홈의 `checkup`은 `~/dev/claude-ops/skills/checkup`으로 가는 심볼릭 링크다. 링크를
디렉터리로 덮지 말고 정본을 고친다.
