---
name: rubato-memory-store-setup
description: Rubato 기억 저장소는 wooojin 하나로 통합됨, msearch 백엔드 redis-stack 6380 + 전용 venv + API키까지 완료해 검색 작동 중
metadata:
  type: project
---

2026-08-25 마이그레이션. Rubato 기억 저장소를 `~/.omo/memory/agents/wooojin` **하나로 통합**했다. `~/.omo/omo.jsonc` 에 `memory.agent: "wooojin"` 을 박아서 어느 cwd 에서 띄우든 같은 저장소로 간다(유저 스코프 설정이 먼저 로드되고 프로젝트 `.omo/omo.jsonc` 가 덮는 구조).

**decisions/ 와 reference/ 는 msearch 로만 읽힌다.** `harness/prompts/base.pi.md:21` — memory 툴은 쓰기 전용이고 읽지 않는다. 즉 msearch 가 안 돌면 그 기억들은 존재하지 않는 것과 같다. 프롬프트에 실리는 건 `system/` 뿐이다.

msearch 백엔드 세팅:
- Redis Stack 7.4.0 (cask, `brew trust` 필요한 Redis 공식 tap) — **homebrew-core 의 redis 8.10 은 안 된다**(vectorset 만 있고 RediSearch 없음)
- launchd `~/Library/LaunchAgents/dev.msearch.redis.plist`, 포트 6380. 끄기: `launchctl bootout gui/501/dev.msearch.redis`
- 파이썬은 `~/.omo/memory/msearch-venv` (brew python 은 EXTERNALLY-MANAGED). `~/.local/bin/msearch` 는 MSEARCH_PYTHON 을 지정하는 **일반 파일 래퍼** — 레포로 가는 심링크로 만들면 안 된다(덮어쓰면 레포 원본이 파괴된다)
- OPENAI_API_KEY 는 `~/.omo/memory/msearch-state/.env` (권한 600). **오직 임베딩용이다** — 모델 호출은 코덱스 OAuth 로 따로 간다. `~/.codex/auth.json` 은 ChatGPT OAuth 라 키가 null 이어서 못 쓴다. 2026-08-25 발급해서 넣었고 색인 완료(10파일 57조각)
- **셸 alias 가 래퍼를 가로챈다.** `~/.zshrc:304` 의 `alias msearch=` 는 레포 스크립트로 직행해서 venv 를 안 쓴다 → 대화형 셸에서 `msearch --doctor` 는 "python 패키지 없음" 으로 뜬다. 에이전트가 쓰는 **비대화형 bash 는 .zshrc 를 안 읽어서 PATH → 래퍼 → venv 로 제대로 간다.** 손으로 확인할 때는 `~/.local/bin/msearch` 를 전체 경로로 부른다

`install.sh --apply` 는 `~/.local/bin/msearch` 를 심링크로 되돌린다 — 그때 래퍼를 다시 만들어야 한다.
**이 구멍은 업스트림 PR 로 올렸다: keepitmello/Rubato#2** (`fix(harness): msearch 설치를 절반에서 끝까지 옮긴다`).
머지되면 설치기가 `harness/msearch/.venv` 를 세우고 스크립트가 그걸 자동으로 집으므로 래퍼가 필요 없어진다 —
그때 venv 를 그 자리로 옮기고 `~/.local/bin/msearch` 를 공식 심링크로 되돌린다.

**redis-py 8 호환 버그를 직접 고쳤다** (로컬 커밋 `6122313aa`, 아직 PR 아님). FT.SEARCH 응답이 redis-py 8 부터 map 으로 와서 파서가 `KeyError: 1` 로 죽었다 — 색인은 되는데 모든 질의가 터진다. 버전 핀이 없어서 새로 까는 사람은 전부 겪는다. 응답을 옛 배열 모양으로 되돌리는 자리를 하나 넣어 해결. 덤으로 FT.HYBRID(Redis Stack 7.4 에 없는 명령)의 거절이 vector 검색까지 죽이던 것도 막았다.

관련: [[codex-memory-bridge]], [[session-analysis-pipeline]], [[automation-adoption-criteria]]
