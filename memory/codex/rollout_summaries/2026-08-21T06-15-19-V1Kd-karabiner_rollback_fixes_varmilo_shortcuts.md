thread_id: 01a022f5-a89b-7671-978c-f79906f9abdd
updated_at: 2026-08-21T06:22:00+00:00
rollout_path: /Users/wooojin/.codex/sessions/2026/08/21/rollout-2026-08-21T15-15-19-01a022f5-a89b-7671-978c-f79906f9abdd.jsonl
cwd: /Users/wooojin

# Karabiner 설정을 8월 16일 정상 상태로 복구해 단축키 문제를 해결한 롤아웃

Rollout context: 사용자는 Varmilo 키보드에서 한영 전환, Rectangle 단축키, ⌘⇧3 캡처 등 여러 단축키가 동시에 망가졌다고 보고했다. Karabiner EventViewer에서 `apple_vendor_top_case_key_code: keyboard_fn`이 내장 키보드에만 보이는 점을 언급했고, 최근 Varmilo용 규칙 수정 이후 문제가 생긴 것으로 추정했다.

## Task 1: Karabiner 설정 롤백 및 단축키 복구

Outcome: success

Preference signals:

- 사용자는 “며칠 전으로 돌릴 수 없나?”라고 요청했고, 설정을 바로 새로 설계하기보다 정상 시점 백업으로 복구하는 방식을 원했다.
- 사용자는 문제가 생긴 상태에서 전체 단축키가 정상인지 확인하고 싶어 했으며, 최종적으로 한영 전환, `⌘⇧3`, Rectangle 단축키가 모두 동작한다고 확인했다. 향후에도 수정 후 이 세 가지를 우선 검증하면 된다.
- 물리 키 입력은 에이전트가 직접 검증할 수 없으므로, 복구 후 사용자가 실제 Varmilo에서 테스트하고 문제가 남을 때만 EventViewer의 실제 키값 기준으로 최소 수정하는 흐름이 적절하다.

Key steps:

- `~/.config/karabiner`와 Rectangle 설정 및 자동 백업을 조사했다.
- 8월 20~21일 백업들과 현재 설정을 비교해, 최근 추가된 Varmilo 전용 Ctrl/Windows/Caps 다중 변환 규칙이 문제의 주요 원인으로 추정됐다.
- 현재 설정 해시를 확인한 뒤, 현재 파일을 `karabiner_20260821-152022-before-rollback-to-20260816.json`으로 안전 백업했다.
- `karabiner_20260820-161923-before-moonlight-except.json`을 현재 `karabiner.json`으로 복원했다.
- 복원 파일의 SHA-256 일치, JSON 유효성, `Default profile` 선택 상태, Karabiner 프로세스 실행 상태를 확인했다.
- 사용자가 “다 된다”라고 명시적으로 확인했다.

Failures and how to do differently:

- 최근 설정에는 Varmilo용 키 변환이 여러 단계로 겹쳐 있었고, 키보드가 실제로 내보내는 이벤트와 어긋나면 Command 조합·한영·Rectangle·캡처가 연쇄적으로 깨질 수 있었다. 향후 복잡한 규칙을 추가하기 전에 현재 파일을 백업하고, 장치별 최소 규칙만 추가해야 한다.
- 캡처 단축키 자체가 macOS 설정에서 비활성화된 흔적은 발견되지 않았다. 비슷한 증상에서는 먼저 Command 변환 규칙과 장치 식별자를 확인하고, macOS symbolic hotkey를 불필요하게 수정하지 않는 것이 좋다.

Reusable knowledge:

- Karabiner 설정 경로: `/Users/wooojin/.config/karabiner/karabiner.json`
- 자동 백업 경로: `/Users/wooojin/.config/karabiner/automatic_backups/`
- 복구 기준 백업: `karabiner_20260820-161923-before-moonlight-except.json` (내용상 8월 16일 정상 상태, SHA-256 `c59ca005...`)
- 롤백 전 안전 백업: `karabiner_20260821-152022-before-rollback-to-20260816.json`
- 복구 후 설정은 `Default profile`, 복합 규칙 4개, 장치 6개였고 Karabiner CLI는 `Default profile`을 반환했다.
- 현재 실행 중인 Karabiner 서비스는 복구 후에도 정상적으로 유지됐으며, 복구 파일이 다시 덮어써지지 않았다.

References:

- 현재 설정: `/Users/wooojin/.config/karabiner/karabiner.json`
- 롤백 명령은 현재 파일 SHA-256이 예상값과 일치할 때만 실행하도록 충돌 검사를 포함했다.
- 최종 사용자 확인: “넌 천재야!!!!!!!!!!!!!!!!! 다 된다 ㅠ 고마워”
