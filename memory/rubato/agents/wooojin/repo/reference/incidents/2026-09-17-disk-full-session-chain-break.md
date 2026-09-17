---
description: 2026-09-17 디스크 100% → Rubato 세션 "Disk I/O error" → 기록 사슬 끊김까지 3겹 사고의 원인·복구 절차·재발 방지.
---
---
description: 2026-09-17 디스크 100% → Rubato 세션 "Disk I/O error" → 기록 사슬 끊김까지 3겹 사고의 원인·복구 절차·재발 방지.
---
# 디스크가 차면 세션 기록 사슬이 끊긴다 (2026-09-17)

상태: 원인 확정·복구 진행. 맵로그 리드 세션 `01a0a908-083f-708f-b820-7437cf1b6e39`(앱 스레드 `a62e4f8a-cfbe-4c03-8c10-de13734280d3`, gpt-6-astra xhigh).

## 증상과 오진

앱에 "Worked for 1.0s" 뒤 `Disk I/O error` 3줄이 반복. 9시간 반 작업 중인 줄 알았지만 실제로는 매 턴 350ms 만에 `stopReason: aborted`, 토큰 0.

## 3겹 원인

1. **디스크 100%** — 남은 공간 430MB. 범인은 `~/Downloads/maplog-qa` 20GB, 그중 `2026-09-16-recap-connected-motion/runs/` 7.6GB. QA 스크립트(`capture_runs.py:61`)가 시도마다 122초짜리 `full.mov` 320MB를 남겨 하룻밤 23바퀴에 7GB.
2. **SQLite 연결이 굳음** — 공간을 비워도 20시간 떠 있던 pi-server가 poisoned connection을 유지. 앱 재시작으로 해소.
3. **세션 기록 사슬 끊김(진짜 원인)** — ENOSPC로 엔트리 `3e0bec63` 한 줄이 안 써졌고, 다음 줄 `a57b85b8`가 없는 부모를 가리킴. 리프에서 조상을 따라가면 24줄 만에 끊겨 압축·문맥창 기록에 도달 못 함 → context-notes 확장 초기화 실패 → `새 문맥 관리 확장이 준비되지 않았어요. 요약 방식으로 전환하지 않고 요청을 중단했어요.`

세 번째가 핵심이다. 요약 모드로 몰래 갈아타지 않고 중단하는 건 설계대로 맞는 동작이다(넘어갔으면 9시간 문맥이 조용히 날아감).

## 진단 방법

- 세션 jsonl은 `id`/`parentId` 링크드 트리. 전체를 읽어 `parentId not in ids`를 세면 끊긴 곳이 바로 나온다. 리프에서 뿌리까지 사슬 길이와 전체 엔트리 수를 비교하는 것도 같은 판정.
- 고장 지점 특정은 `lsof -p <pi-server>`로 연 DB 확인 → 각 sqlite `pragma quick_check` → 세션 jsonl 말미의 `errorMessage` 순서로 좁혔다.
- 에러 문구 원문을 `~/.rubato-pi/stock-engine`에서 grep하면 발생 조건 코드(`context-notes/engine-gate.mjs`, `extensions/context-notes.mjs`)까지 바로 간다.

## 복구

끊긴 줄의 `parentId`를 마지막으로 성한 엔트리 id로 되돌린다. 두 id 모두 8글자라 **바이트 길이가 같아** in-place 덮어쓰기가 가능하다(서버가 파일을 열고 append 중이므로 temp+rename은 위험). 원본은 `.bak-<날짜>-chainfix`로 보존.

```python
with open(p,'r+b') as f:
    f.seek(off); assert f.read(8)==b'3e0bec63'
    f.seek(off); f.write(b'09c6ee14')
```

**파일을 고친 뒤 반드시 앱/pi-server를 재시작한다.** 서버는 세션 트리를 메모리에 캐시하므로 파일만 고치면 계속 같은 에러가 난다. 이번에 순서를 거꾸로 해서(재시작 → 파일 수정) 한 번 헛돌았다.

## 재발 방지 (미결)

- QA 스크립트가 판정 끝난 `full.mov`를 지우게 고치기. 안 하면 9.7GB는 30바퀴치라 하루 반이면 또 바닥.
- 남은 정리 후보: `maplog-qa`의 지난 세션 영상(09-14 2.7G, 09-16-evidence-loop 2.0G, 09-16-reactive 1.5G), `.codex` 오래된 세션·로그 DB.
