---
name: home-reorg-plan
description: "홈(~) 정리 — 새 규칙(2026-08-13): 프로젝트는 ~/App/, 홈 루트 생성 금지"
metadata: 
  node_type: memory
  type: project
  originSessionId: ac1da58d-53e4-48d3-8e3f-4b031718d118
  modified: 2026-08-13T10:00:13.717Z
---

**생성 규칙 (2026-08-13 확정, 재발 방지의 본체):**
- 새 프로젝트·실험·앱은 전부 **`~/App/<이름>/`** 에 만든다 (dev 아님 — 우진님 선택).
- 일회성 산출물은 `~/outputs/`, 사용자에게 줄 파일은 `~/Downloads/`.
- **홈 루트(~)에 새 폴더 생성 금지.** 코덱스 AGENTS.md에도 같은 규칙 있음([[codex-memory-bridge]]).

**2026-08-13 정리 실행:**
- `~/App/`으로 이동: ai-companion-board, chat(웹앱), less-stupid-opus-gpt55-with-fable, mood-for-mom, moodtest, wan22-colab-tools, work(사용량 기록·발표자료), woojin(개인 아카이브 — **voice 샘플 경로가 `~/App/woojin/voice/`로 변경됨**, [[woojin-writing-voice]] 갱신 완료).
- **`~/App/repo/` = git 레포 모음** (우진님 지시): less-stupid-opus-gpt55-with-fable, swot(←projects) 이동.
- 휴지통: orca·Games(빈 폴더), `_quarantine/finance/pipeline-legacy-20260616`(6/30 기한 경과), hama-singleify-backup(아래).
- 유지: maplog(Xcode 활성 — 이동 금지), outputs, tmp, hama(루트 본체 — 우진님이 "본체 빼고" 정리 지시), projects/{aitop100,src}(비-git 잔여).

**Hama 정리 (2026-08-13):** 본체 clean·고유커밋 0·라이브 200 확인 후 `git pull --ff-only`로 origin/main(cfbe323) 동기화. **백업에만 있던 .env 회수**: 프론트 `.env`·`.env.local`, 파이썬 백엔드 `.env` → 본체 제자리에 복원(전부 chmod 600), opensearch 변형 2종은 `~/hama/_env-archive/opensearch/`(.git/info/exclude로 로컬 무시). 그 후 160M 백업 휴지통.

**과거 라운드 요약 (6/16~17 완료):** 26-1학기 통합, ~/dev/finance 통합(stock은 `~/stock` 심링크로 호환 유지 — run_*.py 절대경로 하드코딩 때문, 경로수정 전까지 심링크 제거 금지), Hama worktree 단일화(deps 삭제됨 — 실행 전 npm install/venv 재설치 필요), Downloads 문서통합.

**⚠ 가드 훅:** `~/.zshrc`의 `git()` 래퍼가 destructive git을 차단(return 42). 정식 우회 = 사용자 명시 승인 후 `GIT_OK=1`. 일반 rm/mv/cp·read-only git은 통과.

**원위치 유지 (우진님 지시):** 25-2학기, eclipse, eclipse-workspace, mood, project-journal, reports, 루트 문서 파일들.
