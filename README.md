# Rubato private config

우진의 전역 에이전트 설정과 개인 스킬을 보관하는 비공개 저장소다.

## 포함 범위

- `skills/`: `~/.agents/skills/`
- `overlays/skills/`: 공개 Rubato 업데이트 뒤에도 유지할 개인 스킬 덮어쓰기
- `shell/rubato.zsh`: setup-token을 Rubato에만 넘기지 않는 개인 실행 진입점
- `runtime/`: 공개 수정이 합쳐지기 전 적용하는 검증된 임시 런타임 변환
- `global/claude/CLAUDE.md`: `~/.claude/CLAUDE.md`
- `global/claude/settings.json`: `~/.claude/settings.json`
- `global/claude/agents/`: `~/.claude/agents/`
- `global/claude/hooks/`: `~/.claude/hooks/`
- `global/codex/AGENTS.md`: `~/.codex/AGENTS.md`
- `global/codex/config.toml`: `~/.codex/config.toml`
- `global/codex/agents/`: `~/.codex/agents/`
- `global/codex/rules/`: `~/.codex/rules/`

`skills/checkup`은 원래 심볼릭 링크지만, 다른 Mac에서도 복원할 수 있도록
현재 대상 파일을 일반 디렉터리로 보관한다. 새 Mac에서는 일반 디렉터리로
복원된다. 이미 `~/.agents/skills/checkup`이 심볼릭 링크인 Mac에서는 링크와
링크 대상 모두 건드리지 않고 건너뛴다.

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
커밋한다. 동기화는 저장소 쪽에서 사라진 원본 파일과 제외 대상을 삭제하지만,
목적지가 이 저장소 내부가 아니면 실행을 거부한다. 홈 디렉터리 원본은
삭제하지 않는다.

## Rubato 업데이트

공개 저장소의 `rubato/base`는 `origin/rubato/base`와 같게 유지한다. 개인 스킬은
별도 오버레이에서 다시 설치한다.

```bash
rubato update --yes
```

에이전트나 비대화형 셸에서는 alias에 기대지 않고 아래 절대경로를 쓴다.

```bash
/Users/wooojin/App/rubato-private-config/scripts/update-rubato.sh --yes
```

업데이트가 개인 오버레이와 같은 스킬을 바꿨다면 명령이 경고한다. 업데이트 자체는
충돌 없이 끝나고 기존 개인 동작도 유지되지만, 경고된 스킬은 새 공식판의 변경을
오버레이에 반영할지 별도로 검토해야 한다.

`apply-rubato-overlays.sh --apply`는 브라우저 스킬 링크와
`~/.local/bin/rubato-personal`도 복구하고, `~/.zshrc`에 `shell/rubato.zsh`를
한 번만 연결한다. Claude Code에 필요한 setup-token은 셸에 그대로 두되 Rubato를
실행하는 자식 프로세스에서만 제거한다. 공개 인증 수정이 합쳐지면 이 실행 래퍼는
제거할 수 있다.

큰 기존 세션이 모델 예산 검사를 넘지 못해 `/compact` 화면에도 들어가지 못하는
경우에는 `runtime/resume-recovery-register.mjs`가 빈 대화에서도 모델이 성립하는지만
검사하고 복구 모드로 연다. 세션이 열리면 메시지를 보내기 전에 `/compact`를 실행한다.
공개 수정이 합쳐지면 이 임시 변환을 제거한다.

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
