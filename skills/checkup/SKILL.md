---
name: checkup
description: 정기점검 — doctor로 환경 검사 후, 지난 실행 이후 새 세션 transcript를 digest→luna 추출→승격 판단 3단계로 교훈을 회수한다. 우진님이 /checkup 또는 "정기점검"으로 직접 부를 때만 실행.
disable-model-invocation: true
---

# Checkup

환경 점검과 세션 교훈 회수를 한 번에 도는 정기점검. 원칙 하나가 전체를 지배한다:
**원본 transcript를 LLM에게 직접 읽히지 않는다.** 압축은 로컬 스크립트(토큰 0),
대량 읽기는 luna(코덱스 쿼터), 판단만 Claude가 한다.

## 0. 상태 읽기

```bash
cat ~/dev/claude-ops/state/checkup.json   # {"last_run": "<ISO8601>"}
```

파일이 없으면 비정상(최초 구축 시 생성됨) — 사용자에게 분석 시작 시점을 확인한다.

## 1. 환경 점검

```bash
python3 ~/dev/claude-ops/bin/doctor.py
```

DRIFT 항목은 그대로 보고한다. doctor는 수리하지 않으며, 수리는 사용자 승인 후 별도로.
한 달 넘게 stocktake를 안 돌렸으면 `python3 ~/dev/claude-ops/bin/stocktake.py`도 같이 돌려 보고.

## 2. 새 세션 수집 + 다이제스트 (토큰 0)

last_run 이후 수정된 대화 transcript만 고른다. 서브에이전트 로그와 현재 세션은 제외.

```bash
find ~/.claude/projects -name '*.jsonl' -not -path '*/subagents/*' \
  -newermt "<last_run>" | grep -v "<현재 세션 ID>"
```

각각을 다이제스트로 압축한다 (출력: `state/digests/checkup/YYYYMMDD/<세션ID 앞8자>.md`):

```bash
python3 ~/dev/claude-ops/bin/digest.py <transcript.jsonl> <출력.md>
```

사용자 발화가 2개 미만인 다이제스트는 버린다. 남은 게 0개면 여기서 종료하고 그렇게 보고.
resume된 세션은 파일이 이어 쓰여 지난 실행 발화가 다시 나올 수 있다 — 중복은 4단계에서 걸러진다.

## 3. 교훈 후보 추출 — meight luna xhigh

다이제스트를 워커당 15~20개로 묶어 병렬 디스패치한다. 모델 고정: luna xhigh (terra 이상 금지 — 잔바리 작업).

```bash
meight start checkup-b<N> --role worker --mode delegate --report decision \
  --sandbox ws --model luna --effort xhigh --cwd ~/dev/claude-ops --brief-file - <<'EOF'
## Goal
아래 다이제스트 파일들에서 "Claude가 다음 세션부터 다르게 행동해야 할 교훈 후보"를 추출한다.
후보 = 사용자의 교정·반복 마찰·선호 표현·좌절 신호. 사실 나열이 아니라 행동 교정 재료만.

## Scope
읽기: <다이제스트 경로 목록>. 쓰기: state/digests/checkup/YYYYMMDD/candidates-b<N>.md 하나만.

## Constraints
- **각 다이제스트의 사용자 발화 전수를 하나씩 후보 여부 판정할 것.** 짧은 발화("좀 이해되게 말해봐" 류)가 최고 가치 후보다 — 길이로 거르지 말 것.
- 후보마다: 한 줄 요약 + 근거 발화 원문 인용 + 세션 파일명.
- 판정 원장(발화 수 / 후보 수 / 기각 사유 분포)을 파일 끝에 첨부.

## Report
candidates 파일 경로와 후보 수만. 후보 본문을 decision에 중복 붙여넣지 말 것.
EOF
```

## 4. 승격 판단 — Claude 본인, 자동화 금지

**candidates 파일만 읽는다.** 원본 transcript·다이제스트 재독 금지.

기각 기준: ① MEMORY.md 기존 항목과 중복(→ 새 파일 대신 기존 파일 갱신) ② 헌장·CLAUDE.md가
이미 커버 ③ 일회성 사건 ④ 레포 문서가 SSOT인 제품 규칙. 승격은 메모리 규칙(파일 + MEMORY.md
인덱스 한 줄)대로.

마무리: `checkup.json`의 last_run을 실행 시작 시각으로 갱신하고, 결과를 보고한다 —
doctor 상태, 분석 세션 수, 후보 수, 신규/갱신/기각 수와 대표 기각 사유.
