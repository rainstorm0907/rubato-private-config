---
name: ai-smell-setup
description: "2026-08-12 \"AI 냄새\" 제거 세팅의 정본 파일 위치 — CLAUDE.md/AGENTS.md 커뮤니케이션 규칙, frontend-design 게이트, voice 샘플"
metadata: 
  node_type: memory
  type: project
  originSessionId: b4d77991-f286-47e6-a77a-d0078e636fda
  modified: 2026-08-13T16:10:24.074Z
---

2026-08-12 코딩애플 "AI 냄새" 영상 기반 환경 정비. 수정 요청 시 아래 정본 파일을 직접 편집:

- `~/.claude/CLAUDE.md` — Voice Samples(리듬만 모방, 사실·고유명사 복사 금지) + User Communication(내부 용어 노출 금지) 섹션
- `~/.codex/AGENTS.md` — Communication 섹션에 같은 규칙 + 의례적 칭찬·장식 이모지·불필요한 리스트 금지 (백업: AGENTS.md.bak-20260812)
- `~/.claude/skills/frontend-design/` — SKILL.md에 New-Screen Direction Gate(새 화면 단위면 구조 다른 시안 2~3개 먼저 제안), ui-polish.md에 안티슬롭 기본값 경고 + 검증루프 2라운드 상한
- `~/App/woojin/voice/` — 글 샘플 13편 + INDEX.md(장르별 특징 가이드). 명의 글 작성 시 참조. [[woojin-writing-voice]]

2026-08-14 추가 — **Stance Triggers**: 우진이 이미 쓰는 문장 9개("간보기", "나도 이끌어봐", "열어둬/답정너 금지", "그대로 해석하지마", "한차원 뒤에서 보면?/매몰되지 말고", "읽어만 봐", "토큰 박살내지 말고", "각자 보고 비교해봐", "이해되게 말해봐")를 트리거로 등록. 짧은 문장이 정본 의미로 펼쳐지고, 조합 가능, 적용 시 답 첫머리에 확인 한 마디. `~/.claude/CLAUDE.md`와 `~/.codex/AGENTS.md`에 동일 섹션 중복 — **한쪽 고치면 반드시 같이 고칠 것**.

관련: [[codex-claude-global-sync]] (코덱스가 업스트림이므로 AGENTS.md 쪽 변경은 동기화 흐름 주의)
