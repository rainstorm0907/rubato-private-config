---
name: rubato-direct-provider-cutover
description: "2026-08-29 rubato가 FX bridge/OpenCodex를 버리고 6 provider 직결로 갈아탔다, :8788 데몬·plist·SENPI_AUTH_PATH 전부 폐기, 토큰은 broker sentinel이라 /login 재실행 필요"
metadata:
  type: project
---

2026-08-29 에 `~/dev/Rubato` 를 origin 과 맞추면서 **아키텍처가 통째로 바뀌었다** (업스트림 커밋 `fa50898f5`).

**사라진 것.** `harness/bridge/` 전체, `harness/scripts/{start.sh,install-supervisor.sh,rubato-restart.sh}`, `:8788` FX bridge, OpenCodex `:10100`, `rbr`/`rubato-restart` alias, launchd `dev.rubato.bridge`. 여섯 provider 전부 senpi 프로세스 안에서 vendor 를 직접 부른다. 남은 로컬 의존은 Kiro 사이드카 `:8990` 하나뿐이고, 그 ensure 는 첫 `kiro/*` 호출에만 돈다.

**따라서 `SENPI_AUTH_PATH` · plist supervisor 가드 이야기는 전부 죽은 지식이다.** 그때 남긴 교훈 중 하나만 살아남는다 — **`/health` 의 `ok:true` 와 모델 목록은 인증이 산다는 근거가 못 된다.** 목록은 정적 카탈로그에서 나온다. 확인하려면 그 provider 로 실제 한 턴을 돌려야 한다.

**전환 뒤 사람 손이 필요한 단 한 단계**: `~/.rubato-pi/agent/auth.json` 의 토큰이 broker sentinel 이다(`access` 길이 5, `refresh: "rubato-broker"`). bridge 로 보내라는 표지였을 뿐이라 지금은 무의미하다. `rubato` 세션에서 provider 마다 `/login` 을 다시 해야 한다. **파일 사이로 토큰을 복사하면 안 된다** — OpenAI 는 refresh token 을 회전시켜서, 같은 토큰을 두 저장소가 들면 먼저 갱신한 쪽이 다른 쪽을 영구히 죽인다. 실 토큰은 `~/.omo/agent/auth.json` 에 있지만 그건 bridge 시절 저장소다.

절차서가 레포 안에 있다: `harness/docs/provider-direct-apply-runbook.md`.

관련: [[rubato-update-tty-gated]], [[shared-rubato-clone-hazard]], [[rubato-memory-store-setup]]
