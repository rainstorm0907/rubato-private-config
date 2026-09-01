# Rubato private config

우진의 전역 에이전트 설정과 개인 스킬을 보관하는 비공개 저장소다.

## 포함 범위

- `skills/`: `~/.agents/skills/`
- `global/claude/CLAUDE.md`: `~/.claude/CLAUDE.md`
- `global/claude/settings.json`: `~/.claude/settings.json`
- `global/claude/agents/`: `~/.claude/agents/`
- `global/claude/hooks/`: `~/.claude/hooks/`
- `global/codex/AGENTS.md`: `~/.codex/AGENTS.md`
- `global/codex/config.toml`: `~/.codex/config.toml`
- `global/codex/agents/`: `~/.codex/agents/`
- `global/codex/rules/`: `~/.codex/rules/`

`skills/checkup`은 원래 심볼릭 링크지만, 다른 Mac에서도 복원할 수 있도록
현재 대상 파일을 일반 디렉터리로 보관한다.

## 제외 범위

다음 항목은 의도적으로 저장하지 않는다.

- API 키, 토큰, 쿠키, 로그인 정보, `.env`
- `~/.claude/anthropic.env`
- `~/.config/consult/consult.env`와 Consult 세션·응답
- Codex·Claude 대화 기록, 세션 DB, 메모리 저장소
- 캐시, 로그, `__pycache__`, `.consult`, `.omx`, 백업 사본
- 설치된 앱, 모델 카탈로그, 브라우저 프로필

GitHub 비공개 저장소도 비밀 저장소는 아니다. 인증값은 macOS Keychain이나
로컬 환경 파일에서 따로 관리한다.

## 현재 Mac에서 갱신

```bash
./scripts/sync-from-home.sh
git diff
```

`git diff`로 민감정보와 불필요한 생성물이 들어오지 않았는지 확인한 뒤
커밋한다.

## 새 Mac에 복원

기본 실행은 변경 예정 내용만 출력한다.

```bash
./scripts/restore-to-home.sh
```

확인 후 실제로 복원한다.

```bash
./scripts/restore-to-home.sh --apply
```

복원 스크립트는 기존 파일을 삭제하지 않지만 같은 경로의 파일은 덮어쓴다.
`/Users/wooojin/...` 절대경로가 들어간 설정은 사용자명과 설치 위치가 다른
Mac에서 별도로 고쳐야 한다. 외부 도구와 앱은 이 저장소가 설치하지 않는다.
