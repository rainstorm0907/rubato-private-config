# Task Group: OpenAI Game aerial-world comparison-lab implementation and verification
scope: `/Users/wooojin/App/openaigame`의 승인된 공중 월드 비교 브리프를 baseline·문서에 손대지 않는 격리 lab으로 구현하고, preset 전환·공유 충돌 데이터·telemetry를 실제 브라우저 상호작용까지 검증할 때 쓴다. 이는 최종 월드 선택이나 사용자 체험 판정이 아니다.
applies_to: cwd=/Users/wooojin/App/openaigame (rollout executed from cwd=/); reuse_rule=동일한 `experiments/aerial-world-lab/**` 범위와 docs/31 승인 브리프에만 직접 재사용한다. baseline/brief hash, browser state, and final user comparison are time-specific and must be rechecked.

## Task 1: Build and verify isolated three-world aerial comparison lab, partial

### rollout_summary_files

- rollout_summaries/2026-08-21T14-11-41-Xjho-aerial_world_lab_comparison_build.md (cwd=/, rollout_path=/Users/wooojin/.codex/sessions/2026/08/21/rollout-2026-08-21T23-11-41-01a024a9-c89d-7ef3-84eb-d0ecf22a31ca.jsonl, updated_at=2026-08-21T16:55:15+00:00, thread_id=01a024a9-c89d-7ef3-84eb-d0ecf22a31ca, browser-verified build; final player comparison unverified)
- rollout_summaries/2026-08-21T17-03-13-D4yU-aerial_world_lab_implementation_verification.md (cwd=/Users/wooojin/App/openaigame, rollout_path=/Users/wooojin/.codex/sessions/2026/08/22/rollout-2026-08-22T02-03-13-01a02546-d269-77a2-b0f7-2e3d866d61cc.jsonl, updated_at=2026-08-21T17:50:14+00:00, thread_id=01a02546-d269-77a2-b0f7-2e3d866d61cc, current-code/browser verification; first-impression flights remain user work)

### keywords

- aerial-world-lab, experiments/aerial-world-lab, docs/31-aerial-world-playable-comparison-implementation-brief.md, WORLD_PRESETS, world-presets.js, presetId, sceneId, world_first_impression, aerial-world-lab-flight-telemetry-v1, V-key, collisionShapes, headless Chrome, CDP

## User preferences

- when the approved build scope said “단독 쓰기 범위는 ... `experiments/aerial-world-lab/**` 뿐”, the user prohibited baseline/docs edits, commits, and cleanup -> keep implementation strictly inside the named artifact boundary and report a conflict rather than widening it. [Task 1]
- when implementation was requested, the user required actual browser interaction and separate changed files, checks, browser-confirmed items, and unverified items -> do not substitute static checks for interaction evidence or report the final comparison decision as complete. [Task 1]
- when validating an inherited implementation, the user said “실제 코드·실행 결과만 기준” -> inspect current files and run evidence rather than trust prior session reports. [Task 1]
- for adjacent comparison builds, preserve the brief’s blind-ish `세계 A/B/C` labels, bench-only `V` switching, equipment preservation, and isolated telemetry as acceptance criteria. [Task 1]

## Reusable knowledge

- Lab files are `README.md`, `game.js`, `index.html`, `telemetry.js`, and `world-presets.js` under `experiments/aerial-world-lab/`. It copied the `speed-feedback-v1` physical/equipment baseline and replaced only world data. The original approved docs/31 hash was `2a8a82fc1454213f54bd88a881a6974dc1e1a133f2dd81ef61488c02624cb0cf`; it changed externally during work, so rehash before continuation. [Task 1]
- `WORLD_PRESETS[*].forms` is the shared visual/collision source: forms carry `layer`, `collide`, material, `assetKey`, parts, and optional deterministic motion, and collision shapes are generated from those same parts. [Task 1]
- `V` cycles A→B→C→A only from the bench; `R` resets the current world/equipment. Telemetry key `aerial-world-lab-flight-telemetry-v1` records `presetId`, `sceneId`, per-flight environment, and `world_first_impression`. [Task 1]
- Verified evidence: `node --check` passed for all three JS files. Browser checks loaded `http://127.0.0.1:8654/`, exercised `3`, `V`, `R`, `J`, and `F1`, and found no page/console errors. The baseline and lab’s 67 `P` parameters matched in `verify/params-identity.json`; `WORLD`, `R=13`, and start `(190,886)` also matched. B’s `rocking-horse` motion is derived only from `flightTime`, and visual/collision x/y agreed at `flightTime=2.125`. [Task 1]

## Failures and how to do differently

- Symptom: large inline patch commands fail around template strings/backticks. Cause: nested quoting/tool syntax. Fix: use small `apply_patch` edits or file-based scripts and run syntax checks after each logical patch. [Task 1]
- Symptom: CDP checks see stale JavaScript or a disappeared Chrome target. Fix: start a fresh target, cache-bust script URLs, and assert `typeof window.game.getPreset === 'function'` before interaction. [Task 1]
- Symptom: a screenshot looks like a stale/start frame after camera mutation. Cause: camera state changed without rendering. Fix: expose a lab-only controlled render/camera hook and force render. [Task 1]
- Symptom: report says old telemetry is absent. Browser evidence only proved the new key is isolated; old storage existed. Fix: distinguish “new lab key is used” from “old key does not exist.” User first-impression flights, A→B→C/reverse comparison, and final selection remain unperformed. [Task 1]
- Symptom: `J` inspection lands at a zone start rather than the representative form. Cause: the inspection coordinate does not encode the visual target. Fix: add per-zone `inspectX` and make `jumpToZone()` use it. Do not call parameter identity a same-input position/velocity replay. [Task 1]

# Task Group: OpenAI Game A-world structure exploration
scope: `/Users/wooojin/App/openaigame`에서 지정 브리프만 읽고 A안 공중 월드의 단일 비전·비행 분기·폐기 기준을 문서 산출물 하나에 작성하는 질적 설계 작업이다. 구현 또는 구조 유형 분류 작업이 아니다.
applies_to: cwd=/Users/wooojin/App/openaigame; reuse_rule=docs/29와 같은 범위 제한된 독립 세계 설계에 재사용한다. 이 비전은 구현 승인이나 최종 비교 승자가 아니며, 실제 flight evidence로 다시 판정한다.

## Task 1: Write the A-world structure proposal, success

### rollout_summary_files

- rollout_summaries/2026-08-21T14-11-42-qFpV-independent_aerial_world_sol_medium_structure_exploration.md (cwd=/Users/wooojin/App/openaigame, rollout_path=/Users/wooojin/.codex/sessions/2026/08/21/rollout-2026-08-21T23-11-42-01a024a9-cb4b-7851-bf7d-6b80ef0f140b.jsonl, updated_at=2026-08-21T14:15:36+00:00, thread_id=01a024a9-cb4b-7851-bf7d-6b80ef0f140b, designated document verified)

### keywords

- aerial-world, world-structure, aerial-world-sol-medium, docs/29-aerial-world-structure-exploration-brief.md, speed-wing, glide-wing, open-air, blockout, collision-outline, 창가로 항해하는 미완성 하늘배

## User preferences

- when creating a world proposal, the user said “구조 유형을 미리 분류하지 말고”, “안전한 평균안 대신 하나의 응집된 월드 비전에 베팅하세요” -> present one strong world vision with tradeoffs and discard criteria, not a parallel menu of safe options. [Task 1]
- when scope said “지정된 산출물 파일 하나만 작성” and “그 파일 경로만 짧게 보고”, do not modify code/other documents or pad the completion report. [Task 1]
- the brief fixed `압도적이지만 자유로운 거대한 놀이방 70 / 근접 비행 긴장 30` -> preserve open air between large forms; do not turn it into a continuous course or dense obstacle maze. [Task 1]

## Reusable knowledge

- The proposed A world is “창가로 항해하는 미완성 하늘배”: a huge ceiling airship of hull, ribs, sail, ballast, and prow, with flight through the open air between parts rather than along surfaces. [Task 1]
- Speedwing takes a low/deep inner-hull entry and late climb; glider preserves forward speed for a long outer climb and high glide. They split before the main sail and rejoin in a wide mast-knot space. [Task 1]
- Preserve separate blockout fields for `공간 기준점`, `비행층`, `충돌 외곽`, `시각 자산`, `움직임 역할`, `소리 역할`, and `랜드마크 가림/노출` so art replacement does not require structural rewrite. [Task 1]
- Discard the vision if both wings choose the same side/height/ascent timing, the glider upper route becomes a cost-free safe line, players memorize tiny gaps instead of distant goals, or Speed II collides before the player can see. [Task 1]

## Failures and how to do differently

- Symptom: `git status --short` returns `fatal: not a git repository`. Cause: Git metadata was assumed. Fix: verify the target file and required content directly; Git status was irrelevant to this document-only task. [Task 1]

# Task Group: macOS Karabiner Varmilo shortcut rollback and minimal-rule recovery
scope: `/Users/wooojin`의 Varmilo 키보드에서 한영, Rectangle, `⌘⇧3`처럼 여러 단축키가 함께 깨졌을 때, 최근 Karabiner 변경을 새 규칙으로 덮지 않고 마지막 정상 자동 백업으로 안전하게 복원하는 로컬 macOS 복구 절차다.
applies_to: cwd=/Users/wooojin; reuse_rule=이 Mac의 Karabiner/Varmilo 설정 복구에 재사용 가능하다. 특정 백업 파일·장치 ID·키값은 checkout/time-specific이므로 실제 현재 설정과 EventViewer를 다시 확인한다.

## Task 1: Roll back Varmilo Karabiner rules and restore shortcuts, success

### rollout_summary_files

- rollout_summaries/2026-08-21T06-15-19-V1Kd-karabiner_rollback_fixes_varmilo_shortcuts.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/08/21/rollout-2026-08-21T15-15-19-01a022f5-a89b-7671-978c-f79906f9abdd.jsonl, updated_at=2026-08-21T06:22:00+00:00, thread_id=01a022f5-a89b-7671-978c-f79906f9abdd, user-confirmed recovery)

### keywords

- Karabiner, Varmilo, Rectangle, 한영, keyboard_fn, apple_vendor_top_case_key_code, ⌘⇧3, automatic_backups, rollback, vendor_id 1241, product_id 41169

## User preferences

- when several Varmilo shortcuts broke, the user asked “며칠 전으로 돌릴 수 없나?” -> before designing another mapping, locate the nearest known-good backup and use a reversible rollback path. [Task 1]
- after recovery, the user directly tested 한영 전환, `⌘⇧3`, and Rectangle and said “다 된다” -> use these three real-device checks as the minimum acceptance list for similar keyboard recovery. [Task 1]
- when a remaining key needs correction, use the actual Varmilo EventViewer value and add the smallest device-specific rule; do not infer physical-key output. [Task 1]

## Reusable knowledge

- Karabiner state is `/Users/wooojin/.config/karabiner/karabiner.json`; automatic backups are in `/Users/wooojin/.config/karabiner/automatic_backups/`. First hash and preserve the current file, then restore a known-good backup and compare its SHA-256 with the active file. [Task 1]
- In this incident, `karabiner_20260820-161923-before-moonlight-except.json` represented the pre-Varmilo-change normal state; the pre-rollback current file was preserved as `karabiner_20260821-152022-before-rollback-to-20260816.json`. These filenames are incident evidence, not a universal restore target. [Task 1]
- Verify JSON validity, active `Default profile`, and Karabiner process/CLI state before asking for physical-key tests. The rollback survived service operation and the user confirmed all three affected shortcuts. [Task 1]

## Failures and how to do differently

- Symptom: Command combinations, 한영, Rectangle, and capture fail together after Varmilo edits. Likely cause: overlapping Ctrl/left_command/Caps transformations for the same device (here `vendor_id: 1241`, `product_id: 41169`) remap one physical key multiple times. Fix: back up first, remove the overlapping design by restoring the last good state, then reintroduce only one EventViewer-confirmed transformation if needed. [Task 1]
- Symptom: `⌘⇧3` fails and macOS capture settings look suspect. Cause in this case was Command/Fn conversion, not a disabled symbolic hotkey. Fix: inspect Karabiner device rules before changing macOS capture settings. [Task 1]

# Task Group: macOS Aside bundled-rg security-warning troubleshooting
scope: `/Users/wooojin`의 Aside가 반복적으로 macOS 보안 경고를 띄우거나 검색을 멈출 때, 실제 실행 바이너리의 quarantine/rejection을 확인하고 검증된 대체 경로를 복구하는 로컬 데스크톱 장애 대응이다.
applies_to: cwd=/Users/wooojin; reuse_rule=이 Mac의 Aside runtime과 Homebrew ripgrep에는 재사용 가능하다. Aside 업데이트가 내장 바이너리를 복원할 수 있으므로 재발 시 경로·링크·업데이트 여부를 다시 확인하고, 다른 앱에는 원인을 먼저 검증한다.

## Task 1: Replace Aside's quarantined bundled rg, success

### rollout_summary_files

- rollout_summaries/2026-08-20T13-29-37-oMyf-fix_aside_rg_macos_security_warning.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/08/20/rollout-2026-08-20T22-29-37-01a01f5c-e998-7b62-96fb-5484a42b5beb.jsonl, updated_at=2026-08-20T13:32:41+00:00, thread_id=01a01f5c-e998-7b62-96fb-5484a42b5beb, verified root-cause replacement; recheck after Aside updates)

### keywords

- macOS, Aside, rg, ripgrep, quarantine, com.apple.quarantine, spctl, syspolicyd, CoreServicesUIAgent, xattr, /Users/wooojin/.aside/runtime/native/bin/rg, /opt/homebrew/bin/rg

## User preferences

- when the repeated warning persisted, the user said: "이것좀 그만 뜨게해봐!!!!!!!!!!" -> remove the recurring root cause instead of merely dismissing the current dialog; report the cause, applied change, recurrence condition, and actual re-run verification concisely. [Task 1]

## Reusable knowledge

- Aside invoked `/Users/wooojin/.aside/runtime/native/bin/rg`; the bundled executable had `com.apple.quarantine`/provenance metadata and `/usr/sbin/spctl --assess --type execute --verbose=4 <path>` reported it as rejected. [Task 1]
- The working repair preserved the original as `/Users/wooojin/.aside/runtime/native/bin/rg.blocked-original-20260820` and made the original path a symlink to `/opt/homebrew/bin/rg`. The replacement reported `ripgrep 15.1.0`; an actual search completed, no new security warning was logged, and `CoreServicesUIAgent` had zero windows. [Task 1]
- To diagnose a recurrence, inspect `xattr -l <path>`, assess the actual executable with `/usr/sbin/spctl`, then inspect `syspolicyd`, `CoreServicesUIAgent`, and `XProtectService` through `log show`; confirm behavior by rerunning a search, not only by checking the link. [Task 1]

## Failures and how to do differently

- Symptom: `spctl` validation fails before assessing the file. Cause: this macOS environment's tool is `/usr/sbin/spctl`, not `/usr/bin/spctl`. Fix: invoke `/usr/sbin/spctl` explicitly. [Task 1]
- Symptom: removing xattrs appears to help but the warning returns. Cause: the quarantined Aside-bundled binary remains the executable or can be restored by an update. Fix: preserve it for rollback, link the known-good Homebrew binary at the invoked path, verify with a real search, and recheck the same path after Aside updates. [Task 1]

# Task Group: Research-browser routing with Consult, Grok, and Aside
scope: `/Users/wooojin` 및 `/Users/wooojin/dev/maple`에서 최신·공개·로그인 브라우저 조사가 필요할 때 Sol의 최종 비교 역할과 Consult/Grok+Aside의 실행 역할을 가볍게 분리하는 workflow다. 읽기·reversible browser work와 consequential mutation의 경계를 포함한다.
applies_to: cwd=/Users/wooojin (secondary=/Users/wooojin/dev/maple); reuse_rule=현재 로컬 skill/runtime 설정에 재사용 가능하다. provider/catalog, login state, UI selectors, and model availability are time-specific; local evidence alone로 충분하면 외부 호출을 생략한다.

## Task 1: Replace Consult with the Aside-based ChatGPT executor, success

### rollout_summary_files

- rollout_summaries/2026-08-20T10-16-26-Z7ls-aside_grok_research_routing.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/08/20/rollout-2026-08-20T19-16-26-01a01eac-0c17-76a0-80b8-cba135b66726.jsonl, updated_at=2026-08-20T12:32:54+00:00, thread_id=01a01eac-0c17-76a0-80b8-cba135b66726, quick/deep pilot verified)

### keywords

- consult, run_aside_consult.py, Aside, ChatGPT Pro, GPT-5.6 Sol, contenteditable, keyboard.insertText, fail-closed, /c/ URL, fresh snapshot, detached ref

## Task 2: Build the implicit research router and native Grok+Aside runner, success

### rollout_summary_files

- rollout_summaries/2026-08-20T10-16-26-Z7ls-aside_grok_research_routing.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/08/20/rollout-2026-08-20T19-16-26-01a01eac-0c17-76a0-80b8-cba135b66726.jsonl, updated_at=2026-08-20T12:32:54+00:00, thread_id=01a01eac-0c17-76a0-80b8-cba135b66726, native browser-click pilot verified)

### keywords

- research-browser-router, run_grok_research.py, xai-grok-oauth, grok-4.6, effort=high, Grok+Aside, grok-report.md, grok-run.json, orphanCheck=gone, WebSearch, WebFetch, login auction

## Task 3: Apply the routing update to an already-running Maple session, partial

### rollout_summary_files

- rollout_summaries/2026-08-20T10-16-26-Z7ls-aside_grok_research_routing.md (cwd=/Users/wooojin/dev/maple, rollout_path=/Users/wooojin/.codex/sessions/2026/08/20/rollout-2026-08-20T19-16-26-01a01eac-0c17-76a0-80b8-cba135b66726.jsonl, updated_at=2026-08-20T12:32:54+00:00, thread_id=01a01eac-0c17-76a0-80b8-cba135b66726, follow-up required; do not repeat completed auction work)

### keywords

- Maple Auction, follow-up, routing update, existing session, web search, computer-use fallback, latest research, login listings

## User preferences

- when assigning research, the user specified “Sol이 작업 및 비교, 에이전트로 Grok이 경매장 Aside 브라우저에서 탐색” -> Sol receives the compact result and makes the final comparison; do not make Sol trail browser actions. [Task 1][Task 2]
- the user asked that “정확한 클릭같은 것도 알아서 에이전트가 끝내게” -> route focused public judgment to Consult and broad public/login browsing plus reversible clicks, filters, and downloads to Grok+Aside. [Task 1][Task 2]
- the user repeatedly requested “최대한 경량화” and said “별도 grok-aside-research 스킬은 없는 게 낫다”, “그록 실행기까지만” -> retain one router plus two runners; do not add duplicate skills, shared libraries, or automatic chaining. [Task 1][Task 2]
- when asking for research in another session, the user wanted automatic judgment and invocation -> keep the router implicit, but skip external calls when local evidence is sufficient. [Task 2]

## Reusable knowledge

- `run_aside_consult.py` verifies the logged-in personal ChatGPT Pro account and chosen model before submitting; quick is `GPT-5.6 Sol + 매우 높음`, deep is `GPT-5.6 Sol + Pro`. Work/Free/unlogged state stops the run. [Task 1]
- For Aside ChatGPT UI, use a fresh snapshot; if a ref detaches, re-find it once. `contenteditable` requires click then `keyboard.insertText()` rather than `fill()`, followed by input-content validation. Model-selection verification is fail-closed. Successful runs preserve existing tabs, record the exact `/c/...` URL, then close the task tab. [Task 1]
- Native Grok configuration is `provider=xai-grok-oauth`, `model=grok-4.6`, `effort=high`; `xai/grok-4.6` is not the Aside provider ID. `run_grok_research.py` bounds pages/actions/wall time and saves `grok-brief.md`, `grok-report.md`, `grok-run.json`, stdout, and stderr. [Task 2]
- Grok reports distinguish `직접 관찰`, `공식 확인`, `해석`, `미확인`, `브라우저 작업`, `상태 변경`, and `승인 필요`. On success, read only compact `grok-report.md` and `grok-run.json`; inspect raw logs only for failure or contradiction. [Task 2]
- Grok can finish reading, search, filtering, detail opening, precise clicking, and read-only downloads. Purchases, submissions, messages, deletions, and account/security changes require explicit user approval. The native pilot opened a new Wikipedia tab, clicked English, verified `en.wikipedia.org`, preserved existing Maple tabs, closed the task tab, and ended with `orphanCheck=gone`. [Task 2]

## Failures and how to do differently

- Symptom: login auction research cannot proceed despite Grok. Cause: the first contract only granted WebSearch/WebFetch, not browser authority. Fix: send broad login-web exploration to the native Grok+Aside agent rather than assuming a model limitation. [Task 2]
- Symptom: Aside says `Requested model ... not available`. Cause: wrong provider ID. Fix: check the Aside model catalog and use `xai-grok-oauth/grok-4.6`, not `xai/grok-4.6`. [Task 2]
- Symptom: a short timeout exits code 1 without a useful report. Fix: preserve partial material as code 3 when present and ensure process-group and task-tab cleanup; do not retry blindly. [Task 2]
- Symptom: a routing upgrade does not affect a live session. Cause: environment/skill changes are not retroactive. Fix: send a brief follow-up telling that thread to use the new runner for remaining research and do not redo already-complete work. [Task 3]

# Task Group: OpenAI Game execution gates, document routing, and scene-comparison boundary
scope: `/Users/wooojin/App/openaigame`에서 구현·위임 전 단계/근거/허용 범위를 판정하고, 새 세션의 최소 문서 입구와 공중 맵 장면 비교 상태를 유지하는 현재 운영 관문이다. 실제 플레이 근거 없는 억지 보상/시스템과 승인 전 맵 구현을 막는다.
applies_to: cwd=/Users/wooojin/App/openaigame; reuse_rule=OpenAI Game의 다음 구현·위임·단계 전환에 적용한다. 기준 문서와 현재 버전은 작업 시작 전에 다시 확인하며, 이 규칙을 Maplog 등 다른 프로젝트의 기본 gate로 일반화하지 않는다.

## Task 1: Add persistent pre-implementation anti-forcing gates for OpenAI Game, adopted

### rollout_summary_files

- extensions/ad_hoc/notes/20260815T101212-openaigame-anti-forcing-gates.md (cwd=/Users/wooojin/App/openaigame, rollout_path=none, updated_at=2026-08-15T10:12:12+09:00, thread_id=none, authoritative current execution-gate and Fable-connection note) [ad-hoc note]

### keywords

- OpenAI Game, docs/14-execution-gates.md, REFERENCE, DRAFT, v4, anti-forcing, current stage, one hypothesis, Fable medium, plan mode, Telegram, TELEGRAM_STATE_DIR, telegram-2, @maplog_bot, mirror.last

## Task 2: Consolidate representative document routing and A/B scene-comparison status, success

### rollout_summary_files

- rollout_summaries/2026-08-17T23-40-17-o5At-openaigame_doc_routing_and_dumbfire_research.md (cwd=/Users/wooojin/App/openaigame, rollout_path=/Users/wooojin/.codex/sessions/2026/08/18/rollout-2026-08-18T08-40-17-01a01218-e960-74f1-bdc9-b2aca428d6c9.jsonl, updated_at=2026-08-20T10:14:19+00:00, thread_id=01a01218-e960-74f1-bdc9-b2aca428d6c9, canonical reading path; recheck current comparison status)

### keywords

- START_HERE.md, AGENTS.md, CLAUDE.md, HANDOFF.md, DECISIONS.md, docs/14-execution-gates.md, docs/28-scene-comparison-protocol.md, A안 거대한 매달린 형태, B안 듬성듬성한 스카이라인, IN PROGRESS

## Task 3: Preserve follow-up map-redesign input without authorizing implementation, pending

### rollout_summary_files

- extensions/ad_hoc/notes/20260815T193700-openaigame-map-density-height-reveal.md (cwd=/Users/wooojin/App/openaigame, rollout_path=none, updated_at=2026-08-15T19:37:00+09:00, thread_id=none, authoritative follow-up map-redesign input; not implementation authorization) [ad-hoc note]

### keywords

- OpenAI Game, 맵 재설계, 넓어진 거리, 빠른 속도, 배경·전경 사물, 글 없이 안내, 실제 비행선, 상승과 하강, 3단계 바람 구역, 높이와 구조, 음향 비교

## Task 4: Run or continue an isolated aerial A/B analysis, success/partial

### rollout_summary_files

- rollout_summaries/2026-08-17T17-25-51-AJQ3-independent_aerial_scene_comparison_grok_4_6.md (cwd=/Users/wooojin/App/openaigame, rollout_path=/Users/wooojin/.codex/sessions/2026/08/18/rollout-2026-08-18T02-25-51-01a010c2-1a1d-7b41-a3f8-3f38339acecf.jsonl, updated_at=2026-08-17T17:35:41+00:00, thread_id=01a010c2-1a1d-7b41-a3f8-3f38339acecf, Grok independent artifact completed)
- rollout_summaries/2026-08-17T17-25-52-x82e-independent_airborne_scene_comparison_incomplete.md (cwd=/Users/wooojin/App/openaigame, rollout_path=/Users/wooojin/.codex/archived_sessions/rollout-2026-08-18T02-25-52-01a010c2-1fc1-7060-82f6-5f8df8d6bc42.jsonl, updated_at=2026-08-17T17:26:23+00:00, thread_id=01a010c2-1fc1-7060-82f6-5f8df8d6bc42, Opus task stopped after protocol read; do not treat as completed)

### keywords

- docs/28-scene-comparison-protocol.md, scene-comparison-grok-4.6-high.md, scene-comparison-opus-5-high.md, 공통 입력 패킷, 교차 오염, 단일 산출물, [예상], [검증], A안 거대한 매달린 형태, B안 듬성듬성한 스카이라인, 급강하→속도→상승→활공

## User preferences

- when OpenAI Game implementation or delegation is proposed, the user explicitly requires the current stage and permitted scope to be checked first; `REFERENCE` and `DRAFT` are not implementation authorization. [Task 1] [ad-hoc note]
- when a version is scoped, require exactly `현재 단계 / 판정할 가설 하나 / 근거 문서와 절`; if one is absent or conflicts, reject the implementation brief rather than filling it in. One version judges one hypothesis, not several new systems at once. [Task 1] [ad-hoc note]
- when considering a hidden discovery or reward, explicitly judge `억지가 아닌가`; do not assign meaning merely because an event is already detectable. [Task 1] [ad-hoc note]
- Fable review is input only: the main session must compare it with documents and actual-play evidence, then obtain Woojin's scope approval before implementation. [Task 1] [ad-hoc note]
- when optimizing the representative docs, the user wanted only the representative entrance optimized, not every document reread -> keep `START_HERE.md` to current stage and minimal routing, while preserving detailed plans, feeling references, and early implementation thinking as library documents. [Task 2]
- when requesting Claude/Codex shared rules, the user did not want duplicated rules or a new shared-memory folder -> keep `CLAUDE.md` as an `AGENTS.md` pointer and the rule body in one place. [Task 2]
- when making an important document-structure decision, the user asked to discuss it with `cs sub` Opus 5 High first -> use independent high-quality review as input, but let the main session make the final integration. [Task 2]
- map-redesign input is not implementation approval while sound comparison is in progress -> do not start map implementation from this note; retain it as a later design input. [Task 3] [ad-hoc note]
- when requesting independent scene comparison, the user required “공통 입력 패킷만 지정 순서로 읽으세요”, “찾거나 읽거나 언급하지 마세요”, and one specified output file -> keep the input order and session isolation, edit only the named artifact, and do not add coordinates, pixel measurements, block maps, structure diagrams, or code. [Task 4]

## Reusable knowledge

- The canonical project gate is `/Users/wooojin/App/openaigame/docs/14-execution-gates.md`. Current baseline is v4: do not stack the next version on v5; map and core play come first. [Task 1] [ad-hoc note]
- A hidden discovery/reward is eligible only when all are present: naturally observed real-play behavior, temptation from a pre-existing map/object, an afterward-understandable cause, a verified source of play technique, and a reward that expands behavior. [Task 1] [ad-hoc note]
- Request an independent Fable check at a phase transition, first introduction of a new system, or boundary that turns `REFERENCE`/`DRAFT` into implementation. Do not overuse it for numeric tuning, one-variable experiments within the same stage, or bug fixes. Keep the judgment session Fable medium in plan mode and non-writing; implementation goes to a separately approved, brief-gated session. [Task 1] [ad-hoc note]
- The Fable check uses the existing `@maplog_bot` (`어플개발`) slot at `~/.claude/channels/telegram-2`. Do not enable the global Telegram plugin; configure only that session with `TELEGRAM_STATE_DIR=~/.claude/channels/telegram-2` and the Telegram channel plugin so another session does not capture the bot. [Task 1] [ad-hoc note]
- Verify the bridge by `mirror.last` updating or by successful Telegram delivery, not merely by a live Claude process. Codex desktop chat is not automatically mirrored by the Claude channel hook; send stage decision, task start, and completion updates directly through the same bot. [Task 1] [ad-hoc note]
- Minimum new-session reading path: `START_HERE.md` → `AGENTS.md` → `DECISIONS.md` → `docs/14` §0·§4 → `docs/28-scene-comparison-protocol.md`. `HANDOFF.md` is `CLOSED` historical handoff, not the entrypoint; `DECISIONS.md` is append-only one-line decisions. [Task 2]
- `docs/28` is the A/B definition, comparison criteria, and independent-analysis SSOT. The available Grok artifact chose A, while the listed Opus task is incomplete; do not promote a cross-session consensus or descend to structure diagrams, block maps, coordinates, or map implementation from that evidence. [Task 2][Task 4]
- Keep `docs/08`, `10`, `11`, `19`, `20`, `21`, `docs/02`, and `docs/frame/raw-brief-rocket-plan.md` as preserved library context rather than deleting/moving them for entrypoint simplification. [Task 2]
- For later map redesign, use small background/foreground objects to guide the next airship and wind through direction, spacing, and motion rather than text; reduce big rectangular assemblies in favor of curved, overlapping, asymmetric airships. From stage 3 introduce ascent/descent and make later equipment reveal previously unseen heights/structures; redesign the stage-3 wind approach line and force direction. [Task 3] [ad-hoc note]
- The completed Grok artifact chose A안 because large suspended forms may make speedwing and glider routes qualitatively different. Treat that as one independent conclusion, not final adoption; `docs/23` measurements can be cited, but post-patch climb/camera feel remains `[예상]` until flight-verified. [Task 4]

## Failures and how to do differently

- Symptom: a `REFERENCE`/`DRAFT` document or easy-to-detect event becomes a new system by implementation convenience. Cause: stage authorization and the anti-forcing judgment were skipped. Fix: stop on a missing/conflicting three-part brief and require the real-play eligibility criteria before coding. [Task 1] [ad-hoc note]
- Symptom: Fable is treated as implementation approval, or its judgment session changes files. Cause: independent review and production authority were blurred. Fix: keep Fable medium/plan/non-writing, then have the main session compare evidence and obtain scope approval before a separate implementation session. [Task 1] [ad-hoc note]
- Symptom: Telegram appears connected because Claude is running, but key stage updates never arrive. Cause: process liveness was mistaken for channel delivery, or the global plugin captured the shared bot. Fix: use the scoped `telegram-2` state directory and confirm `mirror.last` or a real send. [Task 1] [ad-hoc note]
- Symptom: long `cs sub` stdout appears empty and triggers duplicate external-model calls. Cause: result may still be in a live process or response file. Fix: inspect PID and output file before retrying; run one managed call. [Task 2]
- Symptom: a compact entrypoint deletes the project's early large plan. Cause: current routing was conflated with archival value. Fix: make the entrypoint a pointer layer and retain the library documents. [Task 2]
- Symptom: an independent review leaks parallel conclusions or becomes a map design. Cause: protocol isolation, single-artifact scope, or qualitative boundary was ignored. Fix: read only the ordered common packet; label unverified physics `[예상]`; keep the fixed A/B template and separate verdict from implementation. [Task 4]
- Symptom: an initiated analysis is reported as finished. Cause: protocol read was mistaken for completion. Fix: require the ordered inputs, required A/B headings, verdict, reversal conditions, and designated output-file check before marking success. [Task 4]

# Task Group: OpenAI Game Dumbfire reference research and physics-clip hook analysis
scope: `/Users/wooojin/App/openaigame`에서 Dumbfire처럼 이목을 끈 로켓 게임 사례를 조사하고, 표면 장르 복제 없이 짧은 물리 클립의 조작·성공 훅을 검증할 때 쓴다. Instagram 관찰 수치와 외부 모델 해석은 구분한다.
applies_to: cwd=/Users/wooojin/App/openaigame; reuse_rule=OpenAI Game의 레퍼런스 조사와 클립/훅 판단에 재사용 가능하다. Instagram 수치·댓글·공개 페이지 상태는 time-specific이며, 제품 기능 요청은 자동 백로그가 아니다.

## Task 1: Research Dumbfire as an attention-getting rocket-game case, partial

### rollout_summary_files

- rollout_summaries/2026-08-17T23-40-17-o5At-openaigame_doc_routing_and_dumbfire_research.md (cwd=/Users/wooojin/App/openaigame, rollout_path=/Users/wooojin/.codex/sessions/2026/08/18/rollout-2026-08-18T08-40-17-01a01218-e960-74f1-bdc9-b2aca428d6c9.jsonl, updated_at=2026-08-20T10:14:19+00:00, thread_id=01a01218-e960-74f1-bdc9-b2aca428d6c9, partial evidence collection; recovered Grok findings remain incomplete)

### keywords

- Dumbfire, Instagram, Steam 4944600, DcJ3LTtJ7rs, DbdcYQYJUYQ, DbQy_Bgpi6b, DboFffGp8Z6, grappling hook, TAS, time trial, Workshop, page.waitForTimeout is not a function, adapter_eof, Grok High

## User preferences

- when researching Dumbfire, the user asked not to force it into “our same genre,” but to treat it as “이목을 끈 로켓 게임 사례” -> separate the attention-making principle from surface genre and from applicability to this game. [Task 1]
- when reading comments, the user wanted the reason for reactions rather than raw counts -> keep original comment evidence, category, and interpretation separate; do not promote feature requests straight to the backlog. [Task 1]
- when researching public posts, the user chose read-only evidence collection -> do not like, follow, comment, message, save, or otherwise change external state. [Task 1]

## Reusable knowledge

- Representative reels: `DcJ3LTtJ7rs` (grappling hook), `DbdcYQYJUYQ` (accuracy flight), `DbQy_Bgpi6b` (multi-target), `DboFffGp8Z6` (update playtest). Directly observed signals were about 3.5k–13k likes and 129–235 comments per reel at the time; values change. [Task 1]
- Repeating reactions: controls/physics admiration, TAS/time-trial interest, demo/release requests, Mac/mobile/Xbox requests, and sandbox/custom-map/level-editor/Workshop requests. Treat the latter as possible expansion desire after the core hook, not product requirements. [Task 1]
- Provisional testable principle: before copying features, ask whether the first seconds show speed, route, and success/failure; whether one scene suggests skilled alternative routes; and whether failure creates immediate retry desire plus a next strategy. The partial Grok conclusion was that one visible flight accomplishment hooks better than feature lists; mark unplayed-video claims as inference. [Task 1]

## Failures and how to do differently

- Symptom: Instagram automation breaks on login popups, unsupported `page.waitForTimeout`, `:has-text` selector/REPL errors, snapshot truncation, or `adapter_eof`. Fix: use Aside `sleep()` plus a fresh snapshot, collect a small set of representative reels in short independent sessions, and save each result immediately. [Task 1]
- Symptom: Grok High keeps browsing and ends without a final report. Fix: set a web-search cap and explicit stop condition; when no result returns, close as partial using only acquired evidence and label direct observation, official confirmation, interpretation, and unknown separately. Do not run broad `rg` over `.codex`/sessions; search the project path and explicit file globs. [Task 1]

# Task Group: Career eligibility, student internships, Baekseok contests, and context-transfer format
scope: `/Users/wooojin`에서 채용 자격을 공식 원문과 학점 자료로 판단하고, 재학생 인턴/백석대 대회를 현황·조건별로 조사하며, 다른 AI용 사용자 컨텍스트를 지정 형식으로 옮길 때 쓴다.
applies_to: cwd=/Users/wooojin; reuse_rule=채용 공고·대회 일정·토큰 가격은 확인 시점 의존이므로 매번 공식 원문을 다시 검증한다. 지원/제출 행위는 명시 승인 없이는 범위 밖이다.

## Task 1: Verify KakaoBank internship eligibility and leave-of-absence premise, success

### rollout_summary_files

- rollout_summaries/2026-08-18T00-23-26-kfik-career_research_internships_baekseok_contests_context_transf.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/08/18/rollout-2026-08-18T09-23-26-01a01240-6ac7-7db1-8c62-4dcdf522026c.jsonl, updated_at=2026-08-18T01:32:38+00:00, thread_id=01a01240-6ac7-7db1-8c62-4dcdf522026c, official eligibility plus local credit-file check)

### keywords

- 카카오뱅크, AI Native 서비스 기획자, recruit.kakaobank.com/jobs/263159, 기졸업자, 졸업 요건, 수료자, 휴학, 120학점, 84.5학점, 35.5학점

## Task 2: Research currently open student-eligible internship alternatives, partial

### rollout_summary_files

- rollout_summaries/2026-08-18T00-23-26-kfik-career_research_internships_baekseok_contests_context_transf.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/08/18/rollout-2026-08-18T09-23-26-01a01240-6ac7-7db1-8c62-4dcdf522026c.jsonl, updated_at=2026-08-18T01:32:38+00:00, thread_id=01a01240-6ac7-7db1-8c62-4dcdf522026c, time-specific jobs; candidate list partly revalidated)

### keywords

- 재학생 인턴, 현재 열림, 마감, 시즌 추정, 딥오토 AI Engineer, 피치에이아이 AI/ML Engineer, 카카오뱅크 AI 운영 어시스턴트, 6개월 풀타임, Wanted 379363, Wanted 376376

## Task 3: Compare Baekseok Smart IT, Hacking Festival, and JAVA contests, partial

### rollout_summary_files

- rollout_summaries/2026-08-18T00-23-26-kfik-career_research_internships_baekseok_contests_context_transf.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/08/18/rollout-2026-08-18T09-23-26-01a01240-6ac7-7db1-8c62-4dcdf522026c.jsonl, updated_at=2026-08-18T01:32:38+00:00, thread_id=01a01240-6ac7-7db1-8c62-4dcdf522026c, official past notices; 2026-2 timing is inference)

### keywords

- 백석대, Smart IT, Hacking Festival, JAVA 경진대회, 개인 참가, 2인, 5인 이내, 상금, 2026-2, 70%, 20%, 10%

## Task 4: Explain Codex research-token cost with uncertainty, success

### rollout_summary_files

- rollout_summaries/2026-08-18T00-23-26-kfik-career_research_internships_baekseok_contests_context_transf.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/08/18/rollout-2026-08-18T09-23-26-01a01240-6ac7-7db1-8c62-4dcdf522026c.jsonl, updated_at=2026-08-18T01:32:38+00:00, thread_id=01a01240-6ac7-7db1-8c62-4dcdf522026c, official pricing distinction; session total estimated, not measured)

### keywords

- Codex 토큰, GPT-5.4 API, input 1M, cache input, output 1M, 정액제, usage limits, credits, 현재 열린 것만 10개

## Task 5: Transfer user context to another AI in a specified format, success

### rollout_summary_files

- rollout_summaries/2026-08-18T00-23-26-kfik-career_research_internships_baekseok_contests_context_transf.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/08/18/rollout-2026-08-18T09-23-26-01a01240-6ac7-7db1-8c62-4dcdf522026c.jsonl, updated_at=2026-08-18T01:32:38+00:00, thread_id=01a01240-6ac7-7db1-8c62-4dcdf522026c, migration-output preference and privacy boundary)

### keywords

- 컨텍스트 이전, 1인칭, 2인칭, 사용자, 원문 유지, 저장된 메모리, 가져온 위치, 한국어 존댓말, 결과 먼저, 검증 증거

## User preferences

- when researching jobs, the user repeatedly said “지원 버튼은 절대 누르지 마” -> read and verify only; do not apply or submit. [Task 1]
- when deciding eligibility, the user asked for “원문 근거로만 판정” -> separate official job wording from local credit/academic evidence. [Task 1]
- after “많이많이 찾아줘,” the user accepted rechecking only actually open postings -> collect broadly, then label `현재 열림 / 마감 / 시즌 추정` before giving candidates. [Task 2]
- when comparing Baekseok contests, “가능하면 1인이 좋은데 안되면 친구 한명까진 ㄱㅊ” and “현실적으로 내가 그렇게 3개정도 한다면” -> prioritize solo participation, use a two-person fallback, and compare prize, format, likely timing, and effort allocation together. [Task 3]
- for context transfer, the user asked “1인칭 대명사와 2인칭 대명사는 사용하지 말아 줘,” preserve user wording especially for requests/preferences, use only stored-memory rules, and end with `가져온 위치: <name>`. [Task 5]

## Reusable knowledge

- At the 2026-08-18 check, KakaoBank AI Native service-planner internship allowed only graduates or people who had completed graduation requirements, and prohibited academic commitments during the internship. The local degree file showed 84.5/120 credits earned, 35.5 short, and 33/54 major credits, so leave of absence did not create the required completion status. [Task 1]
- Time-specific examples: DeepAuto explicitly allowed enrolled/on-leave/graduated applicants; Peach AI allowed vacation-period students/on-leave/future or completed graduates but required no semester classes and 5×40-hour work. KakaoBank assistant roles centered on six-month full-time availability. Recheck each original page before acting. [Task 2]
- From official past notices, Smart IT allowed individual or teams up to five (₩1m grand prize); Hacking Festival was for Baekseok students with team-based awards but no stated one-person ban/size limit; JAVA was individual online problem solving. 2026-2 months were past-pattern estimates only. The proposed fit was Smart IT 70%, Hacking Festival 20%, JAVA 10%; solo JAVA, solo/2-person Smart IT, and a one-friend Hacking Festival. [Task 3]
- Do not present estimated session token counts as measured usage. Official API prices and Codex subscription usage/credits are different; reduce large research by bounding it upfront, e.g. `현재 열린 것만 10개` or `백석대 교내만`. [Task 4]

## Failures and how to do differently

- Symptom: LinkedIn URL is `페이지 없음`, or Aside has stale refs/redeclared `const`. Fix: find the `kr.linkedin.com`/official source again; take a new snapshot after each action, use new variable names, and stay within supported APIs. [Task 1]
- Symptom: a candidate list mixes open roles, closed roles, season patterns, and inferred eligibility. Fix: enforce the three status buckets from the outset and do not call an unverified role student-eligible. [Task 2]
- Symptom: a past contest notice becomes a confirmed 2026 date. Fix: explicitly mark month estimates as inference and re-open the exact board post/2026 notice. [Task 3]
- Symptom: context transfer leaks sensitive personal information or adds current-chat inference as a permanent rule. Fix: include only requested, needed stored-memory facts; exclude contact data, addresses, tokens, and unsupported inference. [Task 5]

# Task Group: 백석대 2026-2 수강계획의 보류된 기독교세계관 분반 선택
scope: 소프트웨어학전공 3학년 2학기 시간표의 확정 과목과, 여자친구 시간표를 대조한 뒤 결정할 기독교세계관 공용 분반 선택을 보존한다. 현재 성적 위험 판단은 당시 강의평 근거이며 최종 수강신청 확정은 아니다.
applies_to: cwd=/Users/wooojin; reuse_rule=2026-2 시간표 대화·재확인에만 사용한다. 강의 시간·분반·성적 위험은 변경될 수 있으므로 실제 수강신청 전 최신 정보와 두 사람의 확정 시간표를 다시 대조한다.

## Task 1: 백석대 2026-2 시간표 방향과 기독교세계관 결정을 보류, pending

### rollout_summary_files

- extensions/ad_hoc/notes/2026-08-09T00-58-44-baekseok-course-plan.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-08-09T00:58:44+09:00, thread_id=none, authoritative current course-plan note) [ad-hoc note]

### keywords

- 백석대, 2026-2, 소프트웨어학전공, 3학년 2학기, 월·수·목 등교, 화·금 공강, 프런티어십, 컴퓨터공학부 채플, 소프트웨어공학, 빅데이터, 다함께 파이썬, 창의융합 Leading Class, 기독교세계관, 서현덕, 김은득, 기독교탐사

## Reusable knowledge

- Current target pattern is 월·수·목 등교 with 화·금 공강. Confirmed courses are 프런티어십(한정수 월1), 컴퓨터공학부 채플(월3), 소프트웨어공학(이승화 월4,5), 빅데이터(이시은 사이버), 다함께 파이썬(손은영 목5,6), 창의융합 Leading Class(박지연 수7,8). [Task 1] [ad-hoc note]
- Do not finalize 기독교세계관 until the girlfriend's Monday 기독교탐사 time is known; then compare both timetables and choose a shared Monday or Wednesday section. The current grade-first candidate is 서현덕 월2; the existing-attendance-day candidate is 김은득 수4, with higher A-grade risk in lecture evaluations. [Task 1] [ad-hoc note]

## Failures and how to do differently

- Symptom: a single-person timetable optimization prematurely fixes 기독교세계관. Cause: the girlfriend's Monday 기독교탐사 constraint is still unknown. Fix: preserve both 월2 and 수4 candidates, then make the joint-timetable comparison before registering. [Task 1] [ad-hoc note]

# Task Group: Hackathon proof-spine, worktree integration, and final-submission verification
scope: 열린 문제의 해커톤에서 제품 선택부터 구현·협업·제출 검증까지, 대표 주장마다 최종 제출 아카이브에서 재실행 가능한 증거를 연결하는 운영 방식이다. 특정 대회의 제품 판단이나 구현 계획 자체는 이 범위에 포함하지 않는다.
applies_to: cwd=/Users/wooojin; reuse_rule=다음 Cofathon·KB AI Challenge 등 contest workflow에 재사용 가능하다. 대회 원문, 제품 선택, 제출 규격, 정확한 검증 명령은 매 대회마다 새 프로젝트 문서에서 다시 확정한다.

## Task 1: Consolidate Cofathon reproducibility discipline and KB AI Challenge product narrative into a proof-spine workflow, adopted

### rollout_summary_files

- extensions/ad_hoc/notes/2026-08-04T13-23-55+0900-hackathon-proof-spine-workflow.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-08-04T13:23:55+09:00, thread_id=none, authoritative future-contest operating decision) [ad-hoc note]

### keywords

- Cofathon, KB AI Challenge, hackathon, proof spine, 한 줄 → 한 사용자 경로 → 한 코드 경로 → 한 검증 명령 → 한 제출 주장, START_HERE.md, DECISIONS.md, CONTRACT.md, RELEASE.md, AGENTS.md, clean release worktree, claim-evidence, final ZIP

## Task 2: Locate and verify the KB AI Challenge final GitHub ZIP, success

### rollout_summary_files

- rollout_summaries/2026-08-04T02-48-42-CVQC-kb_ai_submission_check_and_claude_skill_port.md (cwd=/Users/wooojin/App/maplog, rollout_path=/Users/wooojin/.codex/sessions/2026/08/04/rollout-2026-08-04T11-48-42-019fcaac-6218-7d51-9588-26b61af9a752.jsonl, updated_at=2026-08-04T14:50:45+00:00, thread_id=019fcaac-6218-7d51-9588-26b61af9a752, exact final archive confirmed in a private collaborator repository)

### keywords

- KB-hackaton, keepitmello/KB-hackaton, KB이음케어_우브라더스_제출_최종.zip, 587c9dec032e8043c303829e29ce0636dad633c7, GitHub API, affiliation=owner,collaborator,organization_member, final ZIP

## User preferences

- when preparing the next contest, the user has decided to combine “Cofathon의 동결·재현 규율” with “KB AI Challenge의 제품 서사·다역할 UX” -> use one operating system rather than treating reproducibility and product narrative as separate tracks. [Task 1] [ad-hoc note]
- when an open-ended contest starts, do not lock a detailed implementation plan at the start -> freeze the contest original text, allow independent exploration and the human product choice, then lock one representative path before parallel expansion. [Task 1] [ad-hoc note]

## Reusable knowledge

- The proof spine is `한 줄 → 한 사용자 경로 → 한 코드 경로 → 한 검증 명령 → 한 제출 주장`: every representative sentence needs evidence that can be rerun from the final submission archive. Build the input-one-item through result-return path before parallel UI, runtime, docs, and additional scenarios. [Task 1] [ad-hoc note]
- Use three layers with distinct authority: a personal Codex skill for contest initialization, phase transitions, worktrees/task packets, integration, claim-evidence checks, and final-ZIP re-verification; project `START_HERE.md`, `DECISIONS.md`, `CONTRACT.md`, `RELEASE.md` for current facts/contracts; project `AGENTS.md` only for durable safety rules such as dirty-tree preservation, owner scope, verification integrity, release authority, and no secrets. Keep product value, current work, and long status history out of `AGENTS.md`. Related skill: skills/hackathon-proof-spine/SKILL.md. [Task 1] [ad-hoc note]
- Keep private judgment notes separate from shared meeting notes: `지금 믿는 것 / 찜찜한 것 / 상대에게 전달할 것 / 지금 끝낼 하나 / 나중에 볼 것`; promote only human-confirmed material into the shared decision record. [Task 1] [ad-hoc note]
- Default collaboration topology: shared development host plus independent worktrees per person/agent, one integration owner, and a separate clean release worktree. GitHub is milestone backup/final publication, not the real-time handoff channel. Integrate every 60–90 minutes; check contract changes immediately; if two people must edit the same file, pause parallel work for a short pair session. [Task 1] [ad-hoc note]
- Freeze new features early in release. Extract the exact submission ZIP into a fresh directory and run install, build, test, hero smoke, PDF render, and claim-evidence comparison there; only that archive-level result can be final PASS. [Task 1] [ad-hoc note]
- The KB AI Challenge final repository was private `keepitmello/KB-hackaton`; at the 2026-08-04 check, `main` contained `KB이음케어_우브라더스_제출_최종.zip` (about 6.78 MB) in commit `587c9dec032e8043c303829e29ce0636dad633c7`, alongside the technical PDF, participation documents, prototype code, and screenshots. This identifies the archival target, but does not replace fresh-archive verification for a future submission claim. [Task 2]

## Failures and how to do differently

- Symptom: documents grow but SSOT keeps moving, fixture UI is disconnected from runtime, or the last integration is rushed. Cause: document authority/lifetime, people/agent ownership, and phase-transition conditions were not narrow and explicit. Fix: use the three-layer structure and lock the proof spine before broad parallelism. [Task 1] [ad-hoc note]
- Symptom: parallel `main` push/pull is used as live coordination, or the same file is edited concurrently. Cause: GitHub and worktree boundaries were treated as collaboration protocol. Fix: keep worktrees independent under one integration owner; use milestone GitHub sync and pair briefly for shared-file edits. [Task 1] [ad-hoc note]
- Symptom: the working repository passes but the submitted artifact cannot substantiate the claims. Cause: final submission archive was not revalidated. Fix: re-extract the exact ZIP into a clean directory and run the complete release checklist before calling it PASS. [Task 1] [ad-hoc note]
- Symptom: a GitHub search finds only personal repositories and misses the submitted archive. Cause: collaborator/organization repositories were excluded. Fix: query the GitHub API with `affiliation=owner,collaborator,organization_member`, then inspect the named archive and its commit/tree. [Task 2]

# Task Group: Keyboard buying research: 80Retros GB65, switch choice, and long-term modding
scope: 30만 원대 키보드 구매에서 공식 사양과 실제 커뮤니티 사용 사례를 함께 확인하고, 독거미 대비 가치·통울림·핫스왑 기판·스위치 선택을 짧게 판단할 때 쓴다.
applies_to: cwd=/Users/wooojin; reuse_rule=GB65의 가격·사양·후기 결론은 2026-07-29 조사 시점의 근거다. 다른 키보드 구매에는 조사 순서와 판단 기준만 재사용하고, 현재 가격·재고·후기는 다시 확인한다.

## Task 1: Judge GB65 against 독거미 for price, build quality, resonance, and switch swapping, success

### rollout_summary_files

- rollout_summaries/2026-07-29T08-42-53-ff0V-gb65_80retros.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/07/29/rollout-2026-07-29T17-42-53-019fad0a-7db3-78d1-b1ad-f53f87d9a79d.jsonl, updated_at=2026-07-29T08:42:53+00:00, thread_id=019fad0a-7db3-78d1-b1ad-f53f87d9a79d, official specifications plus limited community-use evidence)

### keywords

- 80Retros GB65, GAME1989, 독거미, 67키, CNC 풀알루미늄, hot-swap, VIA, 통울림, gasket, 1.6mm 논플렉스컷 PCB, MX 3핀 5핀

## Task 2: Explain HMX V0-T versus XMAS for a non-specialist, success

### rollout_summary_files

- rollout_summaries/2026-07-29T08-42-53-ff0V-gb65_80retros.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/07/29/rollout-2026-07-29T17-42-53-019fad0a-7db3-78d1-b1ad-f53f87d9a79d.jsonl, updated_at=2026-07-29T08:42:53+00:00, thread_id=019fad0a-7db3-78d1-b1ad-f53f87d9a79d, practical switch-selection comparison)

### keywords

- HMX V0-T, HMX XMAS, 저소음 택타일, 리니어, 40gf, 2.0mm, 3.8mm, 5핀, 스템 흔들림, 오타

## User preferences

- when assessing a purchase, the user asked “독거미 이런거보다 확실히 좋은거 맞나?”, “키보드갤러리나 그런거 검색해봐”, then “짧게 얘기해봐” -> check both official specifications and real community use, then lead with a short, decisive conclusion rather than a spec dump. [Task 1]
- when choosing hardware for continued use, the user asked “통울림같은 문제는 없나?”, “앞으로 스위치 바꿔가며 사용할 기판으로 퀄 좋은 편이야?” -> answer long-term upgradeability and likely defects before price comparisons; state limited evidence briefly instead of claiming certainty. [Task 1]
- when the user said “둘다 hmx 키알못이야” -> explain switches through linear/tactile feel, noise, weight, and accidental-press risk rather than material jargon. [Task 2]

## Reusable knowledge

- At the 2026-07-29 check, Korean GB65 was a wired 67-key 65% keyboard with CNC full-aluminum case, about 1.8 kg, hot swap, VIA, dampening, one-year warranty, and about ₩298,000. Its 1.6 mm non-flex-cut hot-swap PCB plus aluminum/POM plate options make it a good platform for ordinary MX 3/5-pin switch swaps, but not for Hall-effect or optical-switch expansion. [Task 1]
- GB65 is not objectively better than 독거미 in every dimension: it charges for a heavy aluminum build, Game Boy-retro design, and custom-build enjoyment, while 독거미 remains stronger on wireless convenience and value. The decisive question is whether the user will value the wired 65% layout/design long-term. [Task 1]
- No repeating GB65 통울림 defect was found, but the community sample was limited. The heavy case and dampening make severe resonance less likely; actual sound still depends heavily on foam, plate, and switch combination. [Task 1]
- HMX V0-T is a quiet tactile with an early, clear bump: quieter than typical tactile switches but not silent, with some reported ping/residual noise. HMX XMAS is a light 40 gf linear (2.0 mm actuation, about 3.8 mm travel, 5-pin): smooth and fast but more prone to accidental presses. Choose V0-T for tactile feedback/quieter use and XMAS for a light linear feel. [Task 2]

## Failures and how to do differently

- Symptom: a search for `GB65` returns unrelated products such as DrunkDeer G65. Cause: the model string is ambiguous. Fix: start with `80Retros GAME1989 GB65` and a focused community query such as `site:gall.dcinside.com/mgallery/board`. [Task 1]
- Symptom: sparse 통울림 posts become “there is no issue.” Cause: absence of many reports was treated as proof. Fix: say the recurring-defect signal was not found, name the limited sample, and explain build-dependent variables. [Task 1]

# Task Group: Morrow deterministic skin-compatibility judgment calibration
scope: `/Users/wooojin/Downloads/Cofathon-Full-Mock-02`에서 내부 검증용 피부 프로필·성분·리뷰 판정 엔진을 보정하고, 사용자 승인 전 임계값 비교 산출물을 만들 때 쓴다. 실제 소비자 추천 UX나 임계값 최종 확정은 범위 밖이다.
applies_to: cwd=/Users/wooojin/Downloads/Cofathon-Full-Mock-02; reuse_rule=같은 Morrow data/work checkout의 deterministic judgment와 calibration에 재사용 가능하다. 데이터 분포·사용자 승인·현재 임계값은 실행마다 확인하며, 최종 55/60점 선택을 추정하지 않는다.

## Task 1: Calibrate the review-aware judgment engine and regression-test it, success

### rollout_summary_files

- rollout_summaries/2026-07-28T07-58-18-g2iZ-morrow_skin_judgment_calibration_and_threshold_comparison.md (cwd=/Users/wooojin/Downloads/Cofathon-Full-Mock-02, rollout_path=/Users/wooojin/.codex/sessions/2026/07/28/rollout-2026-07-28T16-58-18-019fa7bb-50b4-72f0-a119-1af5f89893c1.jsonl, updated_at=2026-07-28T09:36:02+00:00, thread_id=019fa7bb-50b4-72f0-a119-1af5f89893c1, deterministic engine correction; 16 tests passed)

### keywords

- Morrow, START_HERE.md, work/judgment.py, test_judgment.py, HELPFUL_CAP, DECISION_THRESHOLD, NEGATIVE_EVIDENCE_THRESHOLD, material_conflict, rating_weight_total, 리뷰 함정, 민감성, 인용문, 262ab43

## Task 2: Generate 55-vs-60 temporary match comparison without changing code, success

### rollout_summary_files

- rollout_summaries/2026-07-28T07-58-18-g2iZ-morrow_skin_judgment_calibration_and_threshold_comparison.md (cwd=/Users/wooojin/Downloads/Cofathon-Full-Mock-02, rollout_path=/Users/wooojin/.codex/sessions/2026/07/28/rollout-2026-07-28T16-58-18-019fa7bb-50b4-72f0-a119-1af5f89893c1.jsonl, updated_at=2026-07-28T09:36:02+00:00, thread_id=019fa7bb-50b4-72f0-a119-1af5f89893c1, comparison artifact only; final threshold pending user scan)

### keywords

- match-comparison-55-vs-60.html, matches-threshold-55.csv, matches-threshold-60.csv, 55점, 60점, MRW-Q007, MRW-P002, MRW-P052, 14건, 9건, final threshold pending

## User preferences

- when implementing a judgment system, the user said “내가 짚지 않았는데 너가 임의로 추가하지마”, “오버엔지니어링 금지” -> start from the personal memo and observed data; keep rules minimal and ask before making a value judgment such as a final threshold. [Task 1]
- when defining the surface, the user said “실제 유저가 사용하는 웹 페이지가 아니라 내부에서 사용할 로직을 검증하는 웹사이트” -> prioritize evidence, score breakdown, and comparable `맞음/안맞음/판단보류` results over consumer-recommendation polish. [Task 1]
- when explaining `안맞음`, the user wanted “상품이 나쁘다”가 아니라 “맞는 성분도 있지만 이 프로필과 어긋나는 점” -> show positive grounds separately from conflict/caution grounds. [Task 1]
- when threshold choice was still open, the user said “코드는 수정하지 말고 … 임시로 생성해봐” -> preserve code and current results; create a comparison artifact for direct scanning before changing the threshold. [Task 2]

## Reusable knowledge

- Read `START_HERE.md` before implementation; it makes `user_profiles` and `ingredient_tags` primary, reviews auxiliary evidence, and keeps recommendation criteria separate from validation criteria. Leave `.sealed/` and source `data/` untouched. [Task 1]
- In this data, `reviews.csv.author_id` is not the same ID system as `user_profiles.csv.user_id`. Filter contact/address/external-promotion reviews, but retain ordinary delivery/purchase context. Review traps also include rating/body polarity mismatch, repeated boilerplate, quoted third-party opinions, sparse-review products, an unregistered profile, and sensitivity-concentrated negative experiences. [Task 1]
- `HELPFUL_CAP = 8` followed the approximate 90th percentile and, together with purchase-verification weighting, prevents one review from dominating. The validated revision uses reviewer skin-type matching, severity and generic-negative terms, quote removal, duplicate attenuation, and stronger negative weight when the reviewer profile matches. [Task 1]
- Keep `DECISION_THRESHOLD = 50` and `NEGATIVE_EVIDENCE_THRESHOLD = 0.12` as the then-current temporary implementation values, not an approved final 55/60 match threshold. Reserve `판단보류` for unregistered profile or insufficient ingredient/review evidence; score positive/negative conflicts as match or mismatch and show a warning. [Task 1][Task 2]
- Regression evidence: P033×민감성 became `mismatch 49`, P041×건성 remained `match 72` after quote correction, P009×지성 was `mismatch 42`; across 1,740 combinations hold rate fell from 69% to 4%, with 16 tests, Python compile, CSV generation, and JS syntax checks passing. [Task 1]
- `work/output/match-comparison-55-vs-60.html` shows common matches and 55-only additions with grounds/warnings. For 21 requests, 55 had 14 matches and 60 had 9 (a subset); inspect the five 55-only cases before any final code, README, or result-CSV update. [Task 2]

## Failures and how to do differently

- Symptom: review evidence rarely changes a verdict (69% holds; zero review-only mismatches). Cause: `base 50`, `coverage × sample_support` double dilution, and a ±10 cap. Fix: model review negatives as an independent calibrated axis rather than merely increasing a small score cap. [Task 1]
- Symptom: `material_conflict` yields `판단보류` even when evidence exists. Cause: conflict was treated as absence of evidence, against the user’s final criterion. Fix: decide match/mismatch by score and expose the conflict as a warning; use hold only for missing core evidence. [Task 1]
- Symptom: empty-review product tests fail. Cause: `rating_weight_total` was uninitialized. Fix: on the empty path explicitly set `weighted_rating=None` and weight total `0.0`. [Task 1]
- Symptom: a threshold comparison is mistaken for final configuration. Cause: the temporary artifacts were generated without user approval of 55 or 60; README also lagged the temporary implementation. Fix: scan the five 55-only rows with the user, obtain the decision, then synchronize code, README, and result CSV; visual browser inspection of the HTML remains a separate optional check. [Task 2]

# Task Group: Short Korean participation-selection replies
scope: 선정·합격·행사 참석처럼 기쁜 소식에 대한 짧고 바로 보낼 수 있는 한국어 회신을 만들고, 전송 직전 자연스러움만 확인할 때 쓴다.
applies_to: cwd=/Users/wooojin/App/maplog; reuse_rule=개인 communication workflow에 재사용 가능하며, event date/name/recipient formality는 새 메시지마다 확인한다.

## Task 1: Draft and confirm a short Cofathon selection acceptance reply, success

### rollout_summary_files

- rollout_summaries/2026-07-24T02-13-15-qxJK-cofathon_selection_reply_short_korean_message.md (cwd=/Users/wooojin/App/maplog, rollout_path=/Users/wooojin/.codex/sessions/2026/07/24/rollout-2026-07-24T11-13-15-019f91e5-f75b-7720-974a-b11c1d7101d8.jsonl, updated_at=2026-07-24T02:17:29+00:00, thread_id=019f91e5-f75b-7720-974a-b11c1d7101d8, user approved concise send-ready wording)

### keywords

- Cofathon, 참가자 선정, 회신, 한국어, 짧은 메시지, 참석 의사, “길게 말고 짧게”, “그냥 이렇게 해????”

## User preferences

- when a selection/celebration reply is needed, the user said “길게 말고 짧게 말해여할거같은데” -> offer a short, send-ready message before optional variants or explanations. [Task 1]
- when the user asks “그냥 이렇게 해????” before sending -> avoid rewriting the approved message; check spacing/naturalness and give warm, immediate reassurance. [Task 1]
- when the user is excited or nervous in casual Korean -> respond warmly and casually, but make the outbound message politely formal. [Task 1]

## Reusable knowledge

- A participation-selection reply only needs thanks, attendance intent, and a short day-of greeting. Proven example: “안녕하세요. Cofathon 신청자 정우진입니다. 참가자 선정 감사드립니다! 7월 30일 행사에 참석하겠습니다. 당일 뵙겠습니다!” [Task 1]

## Failures and how to do differently

- Symptom: the first reply grows into a signature or extra formality. Cause: the default was more ceremonial than the user's requested short reply. Fix: remove signature/unneeded formality first and keep only the essential sentences. [Task 1]

# Task Group: Maplog structure-first implementation and design-stage boundary
scope: `/Users/wooojin/App/maplog`에서 기능·권한·데이터 흐름을 연결하는 구현 단계와 별도 감성/시각 디자인 단계를 혼동하지 않고, native interaction과 필수 UX를 먼저 안정시킬 때 쓴다.
applies_to: cwd=/Users/wooojin/App/maplog; reuse_rule=Maplog의 제품·개발 작업에는 재사용 가능하다. 다만 구체 UI/구현 우선순위는 메인 SSOT와 현재 task boundary를 다시 확인한다.

## Task 1: Set the Maplog pre-design implementation boundary, success

### rollout_summary_files

- extensions/ad_hoc/notes/20260722-012325-maplog-design-stage-boundary.md (cwd=/Users/wooojin/App/maplog, rollout_path=none, updated_at=2026-07-22T01:23:25+09:00, thread_id=none, user-confirmed design-stage boundary and primary product/development SSOT) [ad-hoc note]

### keywords

- Maplog, 디자인 단계 전 구현 원칙, 최소 정보 구조, native interaction, loading, empty, error, 복구, 접근성, 개인정보 경계, 2026-07-12_product_development_plan.md

## User preferences

- when Woojin confirmed the 2026-07-22 boundary for a stage that connects `기능·권한·데이터 흐름` -> 최소 정보 구조와 native interaction을 먼저 안정시키고, 감성·시각 완성도는 별도 디자인 단계에서 일관되게 입힙니다. 임시 시각안을 최종 디자인처럼 굳히거나 조각마다 과도하게 다듬지 않습니다. [Task 1] [ad-hoc note]
- when working before the visual-design stage -> 뒤로가기·주 행동·loading/empty/error·복구·접근성·개인정보 경계처럼 기능 이해와 안전에 필수인 UX는 생략하지 않습니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- Maplog의 메인 제품·개발 SSOT는 `/Users/wooojin/App/maplog/record/plans/2026-07-12_product_development_plan.md`다. 구현 단계의 scope/순서는 이 문서부터 대조한다. [Task 1] [ad-hoc note]
- pre-design implementation은 bare functionality가 아니라 최소 정보 구조, native interaction, 안전·복구·접근성 경계를 갖춘 usable slice를 뜻한다. visual polish는 functional structure가 안정된 뒤 일관된 단계로 묶는다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: 임시 시각안을 최종 디자인처럼 굳히거나 기능 조각마다 과도하게 다듬어 구조 결정을 지연시킨다. 원인: 구현 단계와 감성·시각 완성도 단계를 섞었다. 수정: 현재 작업이 기능·권한·데이터 흐름을 잇는 단계면 SSOT 기준 최소 구조/native interaction과 필수 UX만 완료하고 디자인 polish는 별도 단계로 넘긴다. [Task 1] [ad-hoc note]

# Task Group: MapleStory HEXA/VI skill delta and hexaOrder decision workflow
scope: MapleStory에서 새 VI/HEXA core를 지금 열지, `hexaOrder`를 기다릴지, 특정 burst/boss threshold 때문에 당길지를 판단할 때 기존 V/IV 대비 실제 증가분과 현재 자원을 함께 확인하는 workflow다.
applies_to: cwd=/Users/wooojin/dev/maple; reuse_rule=같은 로컬 Maple character snapshot과 HEXA 상담에는 재사용 가능하다. skill tooltip, `hexaOrder`, character resources, boss target은 live-state-specific이므로 매 질문마다 다시 확인한다.

## Task 1: Record HEXA/VI skill opening and late-hexaOrder decision workflow, success

### rollout_summary_files

- extensions/ad_hoc/notes/2026-07-21-hexa-skill-delta-workflow.md (cwd=/Users/wooojin/dev/maple, rollout_path=none, updated_at=2026-07-21T00:00:00+09:00, thread_id=none, authoritative note for VI/HEXA opening and hexaOrder decision routing) [ad-hoc note]

### keywords

- MapleStory, VI, HEXA, hexaOrder, hexa-skill-workflow.md, growth-assistant.mjs, `skill <character> <skill>`, V core, IV tooltip, VI tooltip, Maplescouter, burst threshold, boss target

## User preferences

- when Woojin asks whether a new VI/HEXA skill should be opened or why it is late in `hexaOrder` -> conclusion first: `open now`, `wait for order`, or pull forward only for a specific burst/boss threshold; personalize it with current character resources and boss target. [Task 1] [ad-hoc note]

## Reusable knowledge

- Start with `/Users/wooojin/dev/maple/kb/hexa-skill-workflow.md`, refresh the character snapshot when stale, then run `node tools/growth-assistant.mjs skill <character> <skill>` to inspect the existing V core, active HEXA core, and recorded resources. [Task 1] [ad-hoc note]
- Compare the existing V/IV tooltip with the VI tooltip and remove repeated text. Never count the full VI tooltip as incremental damage; separate reprinted effects, true numerical additions, and structural interactions. [Task 1] [ad-hoc note]
- Verify class interactions with official notes plus focused class-board experiments, then check the live Maplescouter `hexaOrder`. A later rank means cheaper competing gains exist; it does not automatically make the core bad. [Task 1] [ad-hoc note]
- Stop once existing-to-new delta, important interactions, live order, and resource constraint are known; do not continue broad research after a personalized conclusion is supported. [Task 1] [ad-hoc note]

## Failures and how to do differently

- Symptom: the full VI tooltip is reported as the new skill's damage gain. Cause: reprinted V/IV effects were not removed from the comparison. Fix: calculate only the existing-to-VI delta and label numerical additions versus structural interactions separately. [Task 1] [ad-hoc note]
- Symptom: a late `hexaOrder` is treated as proof that the core should never be opened. Cause: relative opportunity cost was flattened into a binary quality judgment. Fix: compare competing gains and current resources; pull the core forward only when its burst/boss threshold justifies it. [Task 1] [ad-hoc note]

# Task Group: Maplog completed-work reporting and provenance discipline
scope: `/Users/wooojin/App/maplog`에서 구현/QA/문서화가 끝난 뒤 Woojin에게 결과를 다시 설명하거나 project record를 남길 때, plain-language summary와 provenance/status를 섞지 않고 정리하는 기본 reporting contract로 쓴다.
applies_to: cwd=/Users/wooojin/App/maplog; reuse_rule=같은 Maplog repo의 completed-work report, wrap, handoff, project-record 업데이트에는 재사용 가능하다. 다만 실제 결정 출처와 verification evidence는 해당 run 기준으로 다시 확인해야 한다.

## Task 1: Record Maplog explanation-first reporting and provenance/status defaults, success

### rollout_summary_files

- extensions/ad_hoc/notes/20260711-224807-maplog-explanation-and-provenance.md (cwd=/Users/wooojin/App/maplog, rollout_path=none, updated_at=2026-07-11T22:48:07+09:00, thread_id=none, authoritative note for completed-work reporting, provenance labeling, and decision-status discipline) [ad-hoc note]

### keywords

- Maplog, completed-work report, plain Korean summary, provenance, decision status, user-confirmed, assistant recommendation, research inference, implemented, verified, superseded, next unresolved decision

## User preferences

- when Woojin brings back a completed-work report, first explain in plain Korean `what actually changed, how it connects to the original plan, what the user can now do, and what remains` -> 다음 구현 프롬프트로 바로 점프하지 말고 explanation-first closeout를 기본값으로 둡니다. [Task 1] [ad-hoc note]
- when recording Maplog decisions, do not write assistant recommendations, research conclusions, or implementation-agent judgments as Woojin's intent or as a user-confirmed decision -> decision source를 명시적으로 분리합니다. [Task 1] [ad-hoc note]
- when a decision came from Woojin, preserve a short verbatim quote and the date/context when available -> 사용자 판단은 paraphrase만 남기지 말고 짧은 원문 anchor를 함께 남깁니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- project record 기본 순서는 `plain-language summary first -> provenance/status -> implementation facts -> verification evidence -> next unresolved decision`이 가장 reread-friendly하면서도 future-agent handoff에 충분하다. [Task 1] [ad-hoc note]
- provenance label은 최소 `user-confirmed`, `assistant recommendation`, `research inference`, `implementation decision`, `observed QA evidence`를 구분해서 쓴다. [Task 1] [ad-hoc note]
- decision status는 `proposed`, `user-confirmed`, `implemented`, `verified`, `superseded`, `user-confirmation-pending` 같은 explicit status vocabulary로 남기는 편이 검색과 stale cleanup에 유리하다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: completed-work report가 바로 다음 구현 지시로 넘어가서 사용자가 `이번에 뭐가 바뀌었는지` 다시 물어야 한다. 원인: closeout보다 handoff를 먼저 썼다. 수정: plain Korean으로 changed/plan-link/now-possible/remaining을 먼저 설명한다. [Task 1] [ad-hoc note]
- 증상: assistant proposal이나 research conclusion이 사용자 의사결정처럼 기록된다. 원인: source label 없이 결론만 압축했다. 수정: 각 decision에 provenance label을 붙이고, Woojin 결정이면 짧은 quote/date anchor를 남긴다. [Task 1] [ad-hoc note]
- 증상: 같은 문서 안에서 현재 상태가 proposal인지 implemented인지 헷갈린다. 원인: explicit decision status를 생략했다. 수정: `proposed` / `implemented` / `verified` / `superseded` / `user-confirmation-pending` 같은 상태를 각 항목에 붙인다. [Task 1] [ad-hoc note]

# Task Group: Maplog implementation prompt model routing
scope: `/Users/wooojin/App/maplog`의 구현 프롬프트에서 작업 성격에 맞는 모델·추론 강도와 writable-repo 경계를 먼저 고정할 때 쓴다.
applies_to: cwd=/Users/wooojin/App/maplog; reuse_rule=현재 Maplog의 prototype discovery와 approved production integration routing에만 재사용한다. 모델 availability와 exact effort는 프롬프트 시작 전 다시 확인한다.

## Task 1: Route Maplog prompts between Claude Fable prototype work and GPT-5.6 Terra production integration, user-confirmed

### rollout_summary_files

- extensions/ad_hoc/notes/2026-07-12-maplog-model-routing-preference.md (cwd=/Users/wooojin/App/maplog, rollout_path=none, updated_at=2026-07-12T18:59:51+09:00, thread_id=none, authoritative note for starting Maplog implementation prompts with a concrete model and reasoning recommendation, splitting Fable prototype work from Terra integration work) [ad-hoc note]

### keywords

- Claude Fable, GPT-5.6 Terra, very high reasoning, model routing, implementation prompt, read-only prototype, writable repository isolation, motion, feel, data contracts, regression tests

## User preferences

- when Woojin explicitly requested that future implementation prompts begin with a concrete recommendation for which available model and reasoning effort should run that task -> 프롬프트 맨 위에서 `추천 모델 + reasoning effort + 왜 이 라우팅인지`를 먼저 고정합니다. [Task 1] [ad-hoc note]
- when the work is a high-ambiguity, product-defining visual interaction prototype where user intent, convenience, motion, and feel must be discovered and demonstrated -> Claude Fable first를 기본값으로 두고, real repo write는 분리합니다. [Task 1] [ad-hoc note]
- when the work is approved-interaction integration in the real Maplog repo, including persistence, data contracts, edge cases, performance, regression tests, QA evidence, and documentation -> GPT-5.6 Terra with very high reasoning을 기본값으로 둡니다. routine specified UI edits와 non-visual implementation도 Terra 쪽으로 바로 보냅니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- current routing default는 two-step이다: high-ambiguity visual interaction prototype은 Claude Fable first, approved interaction을 real Maplog repo에 integrating하는 작업은 GPT-5.6 Terra with very high reasoning으로 넘긴다. Fable은 read-only or isolated로 두고, Terra와 같은 writable repo를 동시에 잡지 않는다. [Task 1] [ad-hoc note]
- routine, already-specified UI edits와 non-visual implementation work는 Fable prototype 없이 Terra로 바로 가도 된다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: implementation prompt를 시작할 때 어떤 모델이 맡아야 하는지 다시 길게 합의해야 한다. 원인: task type별 routing default를 프롬프트 맨 앞에 고정하지 않았다. 수정: `prototype-discovery면 Fable / production integration이면 Terra very high` recommendation을 prompt header에 먼저 둔다. [Task 1] [ad-hoc note]
- 증상: Fable prototype과 Terra production integration이 같은 writable repo에서 동시에 돌아 충돌하거나 provenance가 흐려진다. 원인: prototype surface와 implementation surface를 분리하지 않았다. 수정: Fable은 read-only or isolated로 돌리고, 승인된 mechanics만 Terra가 real repo에 통합한다. [Task 1] [ad-hoc note]

# Task Group: MapleStory real-use tooling, snapshot freshness, and 레공레 EXP planning
scope: `/Users/wooojin/dev/maple`에서 실제 CLI 마찰만 최소 수정하고, 캐릭터 snapshot/최신 정찰 상태를 정직하게 판단하며, 레공레 경험치·이벤트 가치를 사용자의 단위로 결론낼 때 쓴다.
applies_to: cwd=/Users/wooojin/dev/maple; reuse_rule=동일 Maple 도구와 레공레 상담에 재사용 가능하다. snapshot은 오늘 갱신 후 약 14일 재사용할 수 있으나 경매장 매물·이벤트 일정·주간 진행 및 실제 스크린샷 값은 별도 최신 확인이 필요하다.

## Task 1: Run Maple tools and fix observed friction only, success

### rollout_summary_files

- rollout_summaries/2026-07-27T10-01-48-N8Pv-maple_tool_optimization_and_legongre_exp_event_workflow.md (cwd=/Users/wooojin/dev/maple, rollout_path=/Users/wooojin/.codex/sessions/2026/07/27/rollout-2026-07-27T19-01-48-019fa306-06b3-71f3-a29a-649ca3a279a1.jsonl, updated_at=2026-08-13T14:05:16+00:00, thread_id=019fa306-06b3-71f3-a29a-649ca3a279a1, real CLI execution, minimal fixes, and package verification)

### keywords

- AGENTS.md, kb/codex-brief.md, kb/session-handoff.md, fetch_character.sh, growth-assistant.mjs, latest_digest.sh, formatSeoulTimestamp, manual.liberation, quiet-browse, ECONNREFUSED 127.0.0.1:9223, package_share.sh, package_share PASS

## Task 2: Calculate 레공레 momentum-pass and 메카베리 value, success

### rollout_summary_files

- rollout_summaries/2026-07-27T10-01-48-N8Pv-maple_tool_optimization_and_legongre_exp_event_workflow.md (cwd=/Users/wooojin/dev/maple, rollout_path=/Users/wooojin/.codex/sessions/2026/07/27/rollout-2026-07-27T19-01-48-019fa306-06b3-71f3-a29a-649ca3a279a1.jsonl, updated_at=2026-08-13T14:05:16+00:00, thread_id=019fa306-06b3-71f3-a29a-649ca3a279a1, user-unit EXP, mesos, and post-purchase screenshot recalculation)

### keywords

- 레공레, 1소재=30분, 모멘텀 패스, 메카베리, 상급 EXP 9,000장, 0.545~0.581%, 160~171소재, 80~85시간, 49,800원, 억당 1,600원, 슈피겔버스트, 피버, Lv.284 76.386%

## Task 3: Answer 렌 창룡파천검 activation question, partial

### rollout_summary_files

- rollout_summaries/2026-07-27T10-01-48-N8Pv-maple_tool_optimization_and_legongre_exp_event_workflow.md (cwd=/Users/wooojin/dev/maple, rollout_path=/Users/wooojin/.codex/sessions/2026/07/27/rollout-2026-07-27T19-01-48-019fa306-06b3-71f3-a29a-649ca3a279a1.jsonl, updated_at=2026-08-13T14:05:16+00:00, thread_id=019fa306-06b3-71f3-a29a-649ca3a279a1, official activation sequence was not verified)

### keywords

- 렌, 창룡파천검, 승천, 망혼검 절기, 심검, OPENAPI00004, Please input valid parameter, HTTP 400, jq

## User preferences

- when snapshot freshness is discussed, the user said “오늘 한번 업뎃하고 2주정돈 괜찮” -> do not impose a 30-minute freshness gate; reuse a today-refreshed character snapshot for about 14 days, while checking auction listings, event schedules, and weekly progress separately. [Task 1]
- when improving Maple tools, the user wanted actual use -> run the relevant CLI first and make only minimal changes that remove observed friction, not document-driven speculative design. [Task 1]
- when EXP/purchase advice is requested, the user said “1소재=30분”, “시간대비 몇억까지인지 결론” -> lead with a user-unit/time/meso conversion, a purchase ceiling, and recommendation; keep the arithmetic compact. [Task 2]
- when explaining a game skill, the user said “쉽게 설명좀해줘” -> give the in-game input sequence and key condition first, and do not fill an unverified activation sequence with speculation. [Task 3]

## Reusable knowledge

- Enter the repository through `AGENTS.md` → `kb/codex-brief.md` → `kb/session-handoff.md`; refresh a selected character with `./scripts/fetch_character.sh <캐릭터명>`. Render `today` in KST via `formatSeoulTimestamp()`. Only tracked liberation status should create a blocker; a wholly empty `manual.liberation` should not. [Task 1]
- Preserve partial digest output, but `latest_digest.sh` must exit 1 when browser reconnaissance fails, even if RSS results exist. Security checks in `package_share.sh` stay strict; remove local `/Users/...` paths from shared KB text rather than weakening the scan. Validation used `npm test`, `bash -n scripts/*.sh`, `node --check tools/auction-scan.js`, and a non-empty `package_share PASS` archive/secret scan. [Task 1]
- At the measured setting, 1소재 (30 minutes) was about 0.545–0.581% EXP. The paid momentum pass’s 10 메카베리 + 9,000 상급 EXP was then about 160–171소재 / 80–85 hours; at 49,800원 and 1억=1,600원, 31.125억 meso equivalent. The evidence supported “30억까지 확실히 납득 가능, 35억까지 시간 절약 목적이면 허용,” but it is time- and setup-specific. [Task 2]
- 메카베리→상급 EXP versus reverse order differed only at rounding level; use the convenient order. 피버 is not an EXP multiplier: it enables cooldown-free `슈피겔버스트`; get 100% recovery within 30 minutes and do not exit during fever because re-entry resets the gauge. [Task 2]

## Failures and how to do differently

- Symptom: `latest_digest.sh` creates a file and is called a successful latest reconnaissance despite `ECONNREFUSED 127.0.0.1:9223`. Cause: browser failure was not propagated. Fix: preserve partial output but count failed browser sections and return exit 1. [Task 1]
- Symptom: `rg character` floods output or an API failure shows only a traceback. Cause: large JSON and HTTP error paths were not narrowed. Fix: target a file/field with `jq`; on HTTP 400 print status and `{"error":{"name":"OPENAPI00004","message":"Please input valid parameter"}}` before diagnosing. [Task 1][Task 3]
- Symptom: EXP prediction conflicts with actual use. Cause: model values overrode the current screenshot; the initial Lv.284 ~69% prediction preceded an actual `76.386%`. Fix: recalculate from the pre-use screen value and state the range/conditions; count only the increment over usual 3x, not all 4x coupon time, as saved time. [Task 2]

# Task Group: MapleStory YouTube research playback safety
scope: MapleStory YouTube 영상에서 특정 시점의 시각 증거가 필요한 리서치를 할 때 transcript/subtitle 우선, muted playback, isolated browser profile을 적용한다. 영상의 내용·시세·게임 판단 자체는 별도 리서치 workflow에서 검증한다.
applies_to: cwd=/Users/wooojin/dev/maple; reuse_rule=MapleStory YouTube research에 재사용 가능하다. 영상 재생은 특정 timestamp의 시각 증거가 필요할 때만 하며, 개인 Chrome profile은 이 workflow 범위 밖이다.

## Task 1: Record transcript-first and muted YouTube inspection rule, success

### rollout_summary_files

- extensions/ad_hoc/notes/20260723-142415-maple-youtube-muted-playback.md (cwd=/Users/wooojin/dev/maple, rollout_path=none, updated_at=2026-07-23T14:24:15+09:00, thread_id=none, authoritative playback-safety rule) [ad-hoc note]

### keywords

- MapleStory, YouTube research, transcript, subtitles, timestamp, visual evidence, --mute-audio, player mute, headless Chrome, isolated browser profile, real Chrome profile

## User preferences

- when MapleStory YouTube research is needed -> existing transcripts or subtitles come first; open a video only for visual evidence at a specific timestamp. [Task 1] [ad-hoc note]
- when browser or headless Chrome must inspect a video -> mute before playback and use an isolated profile, never Woojin's real Chrome profile. [Task 1] [ad-hoc note]

## Reusable knowledge

- Use `--mute-audio` or the player mute control before any video inspection. The isolated-profile requirement applies equally to browser and headless Chrome. [Task 1] [ad-hoc note]

## Failures and how to do differently

- Symptom: research opens videos by default or plays audio through the user's normal browser profile. Cause: transcript-first and isolated muted playback were not treated as the default. Fix: inspect transcript/subtitles first; only open a required timestamp in a muted, isolated profile. [Task 1] [ad-hoc note]

# Task Group: MapleStory challenger-server market and community research workflow
scope: MapleStory 챌섭 장비, 주문서, 보스컷, 시세, 커뮤니티 여론을 빠르게 조사해야 할 때 캐릭터 snapshot, 로컬 KB, 최소한의 커뮤니티 렌더를 병렬로 묶어 재사용할 때 쓴다.
applies_to: cwd=/Users/wooojin; reuse_rule=같은 MapleStory 챌섭 시세/커뮤 리서치 workflow에는 재사용 가능하지만, 실제 매물가와 여론은 시점 의존적이므로 character snapshot과 최신 KB를 먼저 다시 확인해야 한다.

## Task 1: Record fast challenger-server market/community research workflow, success

### rollout_summary_files

- extensions/ad_hoc/notes/2026-07-10-002003-maple-challenger-scroll-workflow.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-07-10T00:20:03+09:00, thread_id=none, authoritative note for fast MapleStory challenger-server pricing and community research routing) [ad-hoc note]

### keywords

- MapleStory, 챌섭, 챌린저, 시세, 커뮤, 주문서, 카레잠, 카헤잠, 미트라, 블랙보조, item-equipment.json, kb/branchpoints, latest_digest.sh, quiet-browse, 깡통가, 완성품가

## User preferences

- when Woojin asks about 챌섭 장비/주문서/보스컷/시세/커뮤 여론 -> 오래 헤매지 말고 current character snapshot, 로컬 KB, 최소 커뮤니티 근거를 병렬로 묶어 빠르게 결론까지 가져갑니다. [Task 1] [ad-hoc note]
- when community evidence is needed for 아카/디시 style sources -> raw fetch/curl로 길게 긁지 말고 `quiet-browse open` -> `sleep 2~3` -> `quiet-browse text` 순서로 검색 목록 1개와 핵심 글 1~3개만 읽습니다. [Task 1] [ad-hoc note]
- when giving MapleStory market advice -> 답변은 결론 먼저 `사라/기다려라/조건부`, 숫자 매수선, 근거 2~3줄 구조로 압축합니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- 먼저 `character/<캐릭>/item-equipment.json`과 관련 `kb/branchpoints/`로 현재 상태를 고정하고, 동시에 `./scripts/latest_digest.sh`와 대상 키워드 `rg`를 `kb/latest-digest.md`, `kb/branchpoints`, `kb/yt`에 돌리는 순서가 빠르다. [Task 1] [ad-hoc note]
- 제목 여론만 보면 오판하기 쉽다. 최소한 `뉴비`, `저메소`, `시즌용 교불 매몰`, `완제품 구매 가능`, `직업별 매물가`, `보스컷`, `후반 수요` 전제를 분리해서 읽는다. [Task 1] [ad-hoc note]
- 교불/카르마/시즌 전용 장비는 회수 가능 장비처럼 설명하면 안 된다. 거래 가능/회수 가능 여부를 먼저 명시한 뒤 가격/효율 판단으로 넘어간다. [Task 1] [ad-hoc note]
- `깡통가`와 `완성품가`는 분리해서 본다. 깡통가에는 강화, 잠재, 에디, 재설정 비용을 붙여 실제 매수선과 비교한다. [Task 1] [ad-hoc note]
- Related skill: `skills/maple-challenger-research/SKILL.md` [Task 1]

## Failures and how to do differently

- 증상: 챌섭 시세/커뮤 질문인데 자료 탐색이 길어지고 답이 늦어진다. 원인: 캐릭터 상태와 로컬 KB를 먼저 고정하지 않고 커뮤니티부터 헤맸다. 수정: `item-equipment.json` + `kb/branchpoints` + `latest_digest.sh`/`rg`를 먼저 병렬로 돌린다. [Task 1] [ad-hoc note]
- 증상: 제목 여론만 보고 추천이 흔들리거나 사용자 상황과 안 맞는다. 원인: 뉴비/저메소/교불 매몰/완제품 가능성 같은 전제를 분리하지 않았다. 수정: 질문마다 전제를 먼저 분리하고 맞는 줄기만 남긴다. [Task 1] [ad-hoc note]
- 증상: 깡통가가 싸 보인다는 이유로 잘못된 추천이 나온다. 원인: 강화/잠재/에디/재설정 비용을 빠뜨리고 완성품가와 같은 층위로 비교했다. 수정: `깡통가 + 추가 비용`과 완성품가를 분리해 실제 매수선을 계산한다. [Task 1] [ad-hoc note]

# Task Group: MapleStory Maplescouter API tooling and 레공레 boss-ratio refresh
scope: MapleStory `레공레` 같은 캐릭터의 환산/boss stat을 다시 재야 하는데 browser surface가 불안정하거나 noisy할 때, UI scraping 대신 direct Maplescouter API route와 measured anchor를 빠르게 재사용할 때 쓴다.
applies_to: cwd=/Users/wooojin; reuse_rule=같은 MapleStory Maplescouter 조회/보스 추정 workflow에는 재사용 가능하지만, API values와 boss ratio 결론은 캐릭터 상태와 측정 시점 의존적이므로 조회 전에 갱신 여부를 먼저 확인해야 한다.

## Task 1: Record direct Maplescouter API route and 2026-07-08 레공레 anchor, success

### rollout_summary_files

- extensions/ad_hoc/notes/2026-07-08T20-43-09+0900-maplescouter-api-tooling.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-07-08T20:43:09+09:00, thread_id=none, authoritative note for bypassing browser friction with direct Maplescouter API access and refreshing `레공레` estimates) [ad-hoc note]

### keywords

- MapleStory, Maplescouter, 레공레, 레테, 심연의 결계의 핵, Browser is not available: extension, api.maplescouter.com, /api/id, api-key, boss300_stat, boss380_stat, exchangePower, hexaUsed, Black Mage estimate

## User preferences

- when MapleStory consulting hits browser friction and the approved browser surface still fails with `Browser is not available: extension` -> visual scraping을 계속 밀기보다 direct data route를 먼저 찾아 같은 search path를 반복하지 않게 합니다. [Task 1] [ad-hoc note]
- when the user has already asked to remember character benchmarks for later boss comparison -> fresh measurement anchors도 baseline처럼 남겨 이후 ratio refresh에 바로 재사용합니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- browser/extension path가 unavailable하거나 noisy하면 `https://maplescouter.com/ko/result?name=<character>&preset=00000`의 Next.js chunk를 열어 API base와 request shape를 먼저 확인한다. 이 note 기준 durable route는 `https://api.maplescouter.com/api/id?name=<character>&preset=00000`였다. [Task 1] [ad-hoc note]
- direct request에서 필요한 header는 `api-key`, `Content-Type: application/json`였고, useful JSON paths는 `.calculatedData.boss300_stat`, `.boss380_stat`, `.boss300_hexaStat`, `.boss380_hexaStat`, `.exchangePower`, `.exchangePowerHexa`, `.hexaUsed`였다. [Task 1] [ad-hoc note]
- 2026-07-08 measured anchor는 character `레공레`, Lv280 `레테`, Challenger World 2 기준으로 `boss300_stat 39347`, `boss380_stat 38899`, `boss300_hexaStat 31624`, `boss380_hexaStat 31264`, `exchangePower 63243589.15541312`, `exchangePowerHexa 38886323.44397476`, `hexaUsed [64,1428]`였다. [Task 1] [ad-hoc note]
- `레공레`는 Nexon API/in-game combat power보다 Maplescouter 환산/헥환/boss stat을 SSOT로 우선하는 편이 맞다. prior note의 Lete/정축여축-style combat-power distortion 때문에 same-boss refresh는 comparable measurement condition일 때만 `updated boss ratio ~= previous ratio * (1 + final damage/stat gain)` 식으로 잇는다. [Task 1] [ad-hoc note]
- 2026-07-08 practical conclusion은 old Black Mage estimate `89.97%` -> after HEXA stat `~97.2%` -> after legendary abyss core and follow-up measured growth `~99-103%`, center around `~101%`였다. workspace 기록은 `/Users/wooojin/dev/maple/kb/branchpoints/2026-07-08-legongre-abyss-core-legend.md`와 `/Users/wooojin/dev/maple/kb/prediction-log.md`에 남겼다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: browser가 승인됐는데도 `Browser is not available: extension` 때문에 측정 흐름이 막힌다. 원인: UI/browser surface availability를 SSOT data path보다 우선시했다. 수정: browser surface가 불안정하면 Maplescouter page chunk -> API endpoint 확인 -> direct JSON fetch 순서로 바로 피벗한다. [Task 1] [ad-hoc note]
- 증상: in-app/browser rendering noise 때문에 visual inspection에 시간을 너무 많이 쓴다. 원인: measured values를 DOM/화면에서 읽으려 했다. 수정: boss stat/환산 확인은 direct API response를 기준으로 보고, UI는 supplementary check로만 둔다. [Task 1] [ad-hoc note]

# Task Group: MapleStory equipment efficiency calculation mode
scope: MapleStory 장비 업그레이드 효율이나 meso-per-efficiency 계산을 요청받았을 때 exact mode와 rough mode를 나눠 빠르게 재사용할 때 쓴다. 캐릭터 current snapshot, API delta, screenshot tooltip을 근거로 계산하는 MapleStory 상담용 메모다.
applies_to: cwd=/Users/wooojin; reuse_rule=같은 MapleStory 장비 상담/효율 계산 workflow에는 재사용 가능하지만, 캐릭터 스냅샷과 최근 ratio는 시점 의존적이므로 계산 전에 갱신 여부를 먼저 확인해야 한다.

## Task 1: Record MapleStory precise-vs-rough efficiency calculation mode, success

### rollout_summary_files

- extensions/ad_hoc/notes/20260705-185949-maple-efficiency-calc-mode.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-07-05T18:59:49+09:00, thread_id=none, authoritative note for exact meso-per-efficiency calculation workflow) [ad-hoc note]

### keywords

- MapleStory, efficiency calculation, meso-per-efficiency, precise mode, rough mode, API delta, screenshot tooltip, Maplescouter, spec-efficiency coefficients, cost per 100m, cost per 1b

## User preferences

- when Woojin asks for `exact meso-per-efficiency calculations` in MapleStory gear consulting -> 계산을 대충 ratio 하나로 끝내지 말고 current snapshot, API before/after delta, screenshot tooltip 증가치를 근거로 분해 계산합니다. [Task 1] [ad-hoc note]
- when Woojin explicitly asks for a `fast` or `rough` answer -> full decomposition 대신 최근 ratio를 재사용해 빠르게 buy/skip/order recommendation부터 주고, rough estimate임을 먼저 밝힙니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- precise mode에서는 current character snapshot을 refresh/use하고, changed stats는 API before/after delta와 user screenshot을 concrete evidence로 둔다. [Task 1] [ad-hoc note]
- upgrade는 가능하면 `attack/magic attack`, `boss damage`, `main stat`, `all stat %`, `potential`, `starforce`, `set effect`, `symbol effect` 같은 stat component로 나눠 본다. [Task 1] [ad-hoc note]
- 각 component는 character의 current `Maplescouter/spec-efficiency coefficients`가 있으면 main-stat-equivalent로 변환하고, 결과는 total combat power increase, approximate damage/final-damage increase, total cost, efficiency per `100m`/`1b` mesos까지 함께 보고한다. [Task 1] [ad-hoc note]
- Maplescouter 내부 식을 직접 알 수 없을 때는 decomposition만 approximate로 낮추고, API delta와 screenshot tooltip increase는 hard evidence로 취급한다. [Task 1] [ad-hoc note]
- rough mode에서는 full decomposition을 생략하고, 해당 캐릭터의 most recent calculation ratio, prior combat power/damage ratio, screenshot tooltip increase, known recent upgrade efficiency를 재사용해 빠르게 추정한다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: exact efficiency 질문인데 단순 비율 답변만 줘서 사용자가 원하는 meso-per-efficiency 근거가 약해진다. 원인: current snapshot/API delta/screenshot evidence를 수집하지 않고 rough mode로 답했다. 수정: exact 요청이면 먼저 precise mode로 전환하고 stat component 분해와 cost per `100m`/`1b`까지 같이 낸다. [Task 1] [ad-hoc note]
- 증상: rough answer인데 과도하게 분해 계산하느라 답이 느려진다. 원인: fast/rough cue를 놓치고 precise mode 절차를 그대로 탔다. 수정: rough 요청이면 최근 ratio 재사용, rough label, recommendation-first를 기본값으로 둔다. [Task 1] [ad-hoc note]

# Task Group: MapleStory 레공레 레테 benchmark and boss-practice correction
scope: MapleStory 보스 추천이나 현재 스펙 맥락을 판단할 때 `레공레` `레테` 캐릭터의 2026-06-26 baseline과 practice clear 시간을 빠르게 재사용할 때 쓴다. 이 캐릭터 전용 기준이며, 챌린저/버프 상태와 post-clear timer 해석을 함께 봐야 한다.
applies_to: cwd=/Users/wooojin; reuse_rule=같은 캐릭터 `레공레` `레테`의 보스 비교/추천에는 재사용 가능하지만, 레벨·챌린저 버프·장비가 바뀌면 baseline을 다시 갱신해야 한다.

## Task 1: Record 2026-06-26 MapleStory 레공레 레테 spec/context baseline, success

### rollout_summary_files

- extensions/ad_hoc/notes/2026-06-26-maple-legongre-lete-benchmark.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-06-26T00:00:00+09:00, thread_id=none, user explicitly asked to remember this as the 2026-06-26 baseline) [ad-hoc note]

### keywords

- MapleStory, 레공레, 레테, Lv276, Challenger World, EMERALD 30000, Item Burning Plus, 카오스 더스크, 하드 윌, actual-control benchmark

## Task 2: Correct Chaos Gloom clear-time interpretation for the 2026-06-26 레공레 benchmark, success

### rollout_summary_files

- extensions/ad_hoc/notes/2026-06-26-maple-legongre-cgloom-time-correction.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-06-26T00:00:00+09:00, thread_id=none, correction note that supersedes the earlier Chaos Gloom time read) [ad-hoc note]
- extensions/ad_hoc/notes/2026-06-26-maple-legongre-lete-benchmark.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-06-26T00:00:00+09:00, thread_id=none, original benchmark note containing the superseded `15:02` interpretation) [ad-hoc note]

### keywords

- Chaos Gloom, 카오스 더스크, 4:58, post-clear timer, exit timer, top-right buff, 40-minute potion, 30-minute buff, 5-6 minutes, correction

## User preferences

- when the user explicitly said to remember this as the `2026-06-26 레테 spec/context baseline` -> MapleStory character benchmark/screenshot context는 이후 보스 추천 비교에 바로 재사용할 수 있게 baseline 형태로 남깁니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- 캐릭터 baseline은 `레공레`, class `레테`, live level `276`였고, screenshot EXP state는 `Lv276 4,772,676,843,063 (38.136%)`였다. [Task 1] [ad-hoc note]
- Challenger World state는 `EMERALD 30000`, challenger coins `19250`, upper challenger coins `0`였다. Challenger pass는 `Lv.10`, weekly points `500/500`, EXP support line purchased/claimed through current visible tier였고 applied effects는 normal monster damage `+200%`, additional EXP `+20%`였다. [Task 1] [ad-hoc note]
- Emerald challenger buff snapshot은 `EXP 1.5x`, `attack/magic +80`, `normal monster damage +150%`, `boss damage +70%`, `ignore defense +70%`, `buff duration +60%`, `crit rate +30%`, `crit damage +40%`, `stance 100%`, `all stat +100`, `max HP/MP +5000`, `summon duration +10%`, `cooldown reduction -5%`, `guild contribution 2x`, `rune spell duration +50%`였다. [Task 1] [ad-hoc note]
- Item Burning Plus state는 stage 7 진행 중, `276/270`, hard Damien solo `1/1`, challenger emblem `2650/3000`, weekly hunting mission `10000/10000`였다. [Task 1] [ad-hoc note]
- actual-control benchmark로는 Hard Will practice가 가장 직접적이다. screenshot은 boss HP `0.1%`, remaining time `1:48`, death count remaining around `9`였고 actual clear는 approximately `18:13-18:20`로 본다. 가이드 없이 깬 기준이라 clearable but slower/learning-heavy anchor로 쓸 수 있다. [Task 1] [ad-hoc note]
- Chaos Gloom practice clear는 initial note의 `15:02`가 아니라 correction note 기준으로 `about 5-6 minutes`가 맞다. center `4:58`은 boss remaining timer가 아니라 kill 뒤 뜨는 post-clear 5-minute exit/cleanup timer이고, top-right buff/potion area의 `40-minute buff at 34 remaining`과 `30-minute buff at 24 remaining`이 실제 elapsed cue다. [Task 1][Task 2] [ad-hoc note]
- future boss recommendation에서는 Chaos Gloom은 already within practical expectation, Hard Will은 clearable but slower/learning-heavy로 본다. next practical comparisons는 `Hard Darknell`, `Chaos Guardian Angel Slime`, `Hard Lucid`, `Hard Verus Hilla`였다. [Task 1][Task 2] [ad-hoc note]

## Failures and how to do differently

- 증상: Chaos Gloom screenshot의 center `4:58`을 boss remaining timer로 읽어 clear time을 `15:02`로 과대추정했다. 원인: 새 post-clear 5-minute exit/cleanup timer를 전투 timer로 오인했다. 수정: clear 직후 스샷은 top-right buff/potion timer를 먼저 보고, center countdown이 post-clear UI인지 확인한다. [Task 2] [ad-hoc note]
- 증상: correction이 나온 뒤에도 earlier benchmark note의 수치를 그대로 재사용할 수 있다. 원인: baseline note와 correction note를 분리 저장했지만 superseded status를 메모에 명시하지 않으면 검색 시 오래된 숫자가 먼저 잡힌다. 수정: Chaos Gloom benchmark는 `about 5-6 minutes`로 overwrite하고, `15:02`는 superseded interpretation으로만 남긴다. [Task 1][Task 2] [ad-hoc note]

# Task Group: MapleStory boss benchmark and boss-ratio decision rules
scope: MapleStory 보스 비교나 다음 솔로 목표 판단에서 `오렌지솥밥` 캐릭터의 실제 클리어 앵커와 환산/Maplescouter 비율 기준을 빠르게 재사용할 때 쓴다. 이 캐릭터 전용 기준이며, 스샷 시간 충돌과 피로도까지 함께 반영해야 한다.
applies_to: cwd=/Users/wooojin; reuse_rule=같은 캐릭터 `오렌지솥밥`의 보스 비교/추천에는 재사용 가능하지만, 스펙 수치와 실제 가능 보스는 업그레이드 이후 다시 갱신해야 한다.

## Task 1: Record 2026-06-25 MapleStory boss benchmark for 오렌지솥밥, success

### rollout_summary_files

- extensions/ad_hoc/notes/2026-06-25-maple-orange-boss-benchmark.md (cwd=/Users/wooojin, rollout_path=none, updated_at=2026-06-25T00:00:00+09:00, thread_id=none, user explicitly asked to remember future boss-comparison data) [ad-hoc note]

### keywords

- MapleStory, 오렌지솥밥, Maplescouter, 환산주스탯, Champion Black Mage, Normal Seren, Easy Kalos, Easy Adversary, boss ratio, conservative screenshot

## Reusable knowledge

- 캐릭터 baseline은 `오렌지솥밥, Luna, Ren, Lv.282`, latest Maplescouter snapshot after 2026-06-25 upgrades는 `combat power 70,409,457`, `boss300 46,180`, `boss380 45,796`, `arcane force 1350`, `authentic force 340`, `ascent_const 0.008657956840101733`였다. [Task 1] [ad-hoc note]
- 이 캐릭터 비교는 HP table보다 `환산주스탯/Maplescouter-style boss ratio first`가 우선이고, actual clear anchors는 Champion Black Mage clear와 Normal Seren clear다. [Task 1] [ad-hoc note]
- Champion Black Mage는 about `110.5%`, rough 20-minute model time `18.1m`였고, conservative screenshot anchor는 `0.6% HP at 1:48 remaining`이다. `0.1% HP at 4:53 remaining` 스샷도 있지만 file order/timer progression과 충돌해서 optimistic/phase-display evidence로만 둔다. [Task 1] [ad-hoc note]
- Normal Seren은 about `212.7%`, rough 20-minute model time `9.4m`였고 comfortably stable로 본다. Seren screenshots는 `0.9% HP at 8:55 remaining`과 clear/cutscene `4:58-4:56 remaining`이 함께 있어도 conservative 쪽은 lower remaining time 기준으로 본다. [Task 1] [ad-hoc note]
- Easy Kalos는 about `171.0%`라 damage는 충분하고 main variable은 mechanics/downtime이다. Easy Adversary는 about `119.8%`라 ratio만 보면 가능하지만 피로도와 unfamiliar patterns 때문에 same-day push 추천 대상은 아니다. [Task 1] [ad-hoc note]
- 현재 비현실 target은 `Normal Kalos 49.5%`, `Champion Kalos 34.3%`, `Normal Adversary 34.9%`, `Hard Seren 86.9%`, `Champion Seren 71.5%`였다. [Task 1] [ad-hoc note]
- future rule of thumb: around `110%`는 near-cut으로 last 1-2 minutes 예상, around `120%`는 some mistakes allowed, around `170%`는 damage sufficient so mechanics/fatigue decision, around `200%+`는 stable farm/comfortable clear 쪽이다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: 스크린샷 timer display가 서로 충돌해 clear benchmark가 과하게 낙관적으로 잡힐 수 있다. 원인: file order/timer progression이 맞지 않는 장면을 같은 무게로 썼다. 수정: `Prefer conservative screenshot time if timer displays conflict`를 기본값으로 둔다. [Task 1] [ad-hoc note]
- 증상: Kalos/Adversary를 단순 HP 또는 비율만으로 추천하고 싶어진다. 원인: mechanics/downtime와 fatigue 변수를 과소평가했다. 수정: Kalos/Adversary는 pattern burden을 별도 가중하고, 사용자가 tired하다고 하면 new mechanic-heavy boss push는 추천하지 않는다. [Task 1] [ad-hoc note]

# Task Group: Maplog manual representative-only cover selection
scope: `/Users/wooojin/App/maplog`에서 Gathering cover를 한 장의 수동 대표사진과 자동 rear/layer selection으로 유지하고, 이전 full-cover-order 상태를 안전하게 이행할 때 쓴다.
applies_to: cwd=/Users/wooojin/App/maplog; reuse_rule=동일한 cover-selection contract와 migration에 재사용한다. UI gesture/geometry의 구체 구현은 현재 code와 별도 검증이 필요하다.

## Task 1: Keep Maplog cover selection manual for one representative only, user-confirmed

### rollout_summary_files

- extensions/ad_hoc/notes/2026-07-12-maplog-manual-representative-only.md (cwd=/Users/wooojin/App/maplog, rollout_path=none, updated_at=2026-07-21T12:45:20Z (source-file git timestamp), thread_id=none, user-confirmed decision that supersedes a user-selected full cover order) [ad-hoc note]

### keywords

- Maplog, manual representative-only, Gathering, 1/2/3-photo map-pin tiers, rear layers, 다른 사진으로 할래요, hand fan, lifted card, deterministic, re-entry, relaunch, legacy cover order, migration

## User preferences

- when choosing a Gathering cover -> 사용자는 대표 사진 한 장만 직접 고르고, 1/2/3-photo map-pin tier의 rear/layer 사진은 Maplog가 자동으로 고르길 확정했습니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- `다른 사진으로 할래요`에 들어가면 기존 automatic preview card는 selected/lifted/slot state 없이 hand fan으로 돌아간다. 탭하거나 scrub-commit한 한 카드만 manual representative로 lifted되고, 다른 카드를 고르면 이전 representative는 fan으로 돌아간다. [Task 1] [ad-hoc note]
- automatic rear choice는 uncurated하게 보이되 같은 input에서 deterministic하고 re-entry/relaunch에도 안정적이어야 한다. photo add/delete 뒤에는 recompute하되 유효한 manual representative는 유지한다. legacy full cover order는 superseded됐으므로 migration은 첫 legacy user cover만 manual representative로 해석하고 rear layer를 자동 재생성한다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: rear/layer photo까지 user-editable slot으로 노출하거나 full cover order를 보존한다. 원인: superseded된 cover-selection contract를 계속 적용했다. 수정: manual state는 representative 한 장만 보관하고 rear layer는 deterministic automatic selection으로 재생성하며, legacy migration은 첫 cover만 대표로 읽는다. [Task 1] [ad-hoc note]

# Task Group: local Claude / Codex CLI configuration and cmux troubleshooting
scope: Claude Code 인증 충돌 정리, Codex-to-Claude 전역 지침/skill 동기화, Claude hook과 cmux socket mismatch 진단처럼 로컬 CLI 동작을 바로잡는 작업에 쓴다. 원격 API 일반론보다 이 Mac의 실제 파일/프로세스 상태 확인에 초점을 둔다.
applies_to: cwd=/Users/wooojin; reuse_rule=같은 사용자 홈의 `.claude`, `.codex`, `.local/state/cmux`를 다루는 로컬 CLI 설정/장애 대응에는 재사용 가능하지만, live env var와 socket path는 시점 의존적이므로 매번 다시 확인해야 한다.

## Task 1: Remove Claude auth conflict by disabling local API-key injection and approval state, success

### rollout_summary_files

- rollout_summaries/2026-06-10T04-27-05-xbew-claude_auth_fix_and_codex_skill_sync.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/06/10/rollout-2026-06-10T13-27-05-019eafc8-af7f-7533-b407-1d31e1f0baa8.jsonl, updated_at=2026-06-10T04:45:11+00:00, thread_id=019eafc8-af7f-7533-b407-1d31e1f0baa8, auth conflict was fixed by removing local API-key path rather than tolerating it)

### keywords

- Claude Code, ANTHROPIC_API_KEY, anthropic.env, customApiKeyResponses, claude.ai login, Google login, ~/.claude.json, launchctl getenv

## Task 2: Sync Codex global guidance and user skills into Claude-specific locations, success

### rollout_summary_files

- rollout_summaries/2026-06-10T04-27-05-xbew-claude_auth_fix_and_codex_skill_sync.md (cwd=/Users/wooojin, rollout_path=/Users/wooojin/.codex/sessions/2026/06/10/rollout-2026-06-10T13-27-05-019eafc8-af7f-7533-b407-1d31e1f0baa8.jsonl, updated_at=2026-06-10T04:45:11+00:00, thread_id=019eafc8-af7f-7533-b407-1d31e1f0baa8, Codex skills and AGENTS guidance were copied into Claude paths with environment-specific path fixes)

### keywords

- ~/.claude/CLAUDE.md, ~/.codex/AGENTS.md, ~/.claude/skills, ~/.codex/skills, settings.json, skill sync, path rewrite, .DS_Store

## Task 3: Port framing/reframing to Claude Code and verify discovery, success

### rollout_summary_files

- rollout_summaries/2026-08-04T02-48-42-CVQC-kb_ai_submission_check_and_claude_skill_port.md (cwd=/Users/wooojin/App/maplog, rollout_path=/Users/wooojin/.codex/sessions/2026/08/04/rollout-2026-08-04T11-48-42-019fcaac-6218-7d51-9588-26b61af9a752.jsonl, updated_at=2026-08-04T14:50:45+00:00, thread_id=019fcaac-6218-7d51-9588-26b61af9a752, Claude-native selective skill port and smoke-tested installation)

### keywords

- framing, reframing, Claude Code, Agent, meight, consult, CLAUDE.md, ~/.claude/skills, claude-framing-skills-staging, sensitive file, Task(Agent), roo-channel, trigger-evals.json, skill discovery

## User preferences

- when the user said `API_KEY 입력된거 빼주고, 그냥 1번 구글 로그인으로만 작동하게 로컬 로그인 빼줘` -> Claude auth 충돌은 경고 무시 대신 local API-key path와 승인 흔적까지 제거하는 쪽을 기본값으로 둡니다. [Task 1]
- when the user said `우리 지금 사용중인 코덱스 skill이랑 전역세팅 클로드에 적용시켜줘` -> Codex에서 쓰는 운영 모델을 Claude에도 실제 파일 변경으로 복제하는 쪽을 기대합니다. [Task 2]
- when the user said “매번 사용이 아니라 특이 사항 설계 간에서 사용하는 것” -> `framing`/`reframing`을 일반 작업의 상시 게이트로 만들지 않고 명시적·선택적 호출 도구로 유지한다. [Task 3]
- when the user asked to have it “Claude한테 맞는 방식으로 수정해서 설치” -> do not copy Codex skill files verbatim; inspect the target `CLAUDE.md`, tool names, skill conventions, and actual discovery before calling the port complete. [Task 3]

## Reusable knowledge

- Claude auth conflict의 실제 주입점은 `/Users/wooojin/.claude/anthropic.env`였고, approval state는 `/Users/wooojin/.claude.json`의 `customApiKeyResponses`였다. 둘 다 정리해야 `Google/claude.ai login only` 상태가 깔끔해진다. [Task 1]
- 환경 변수 cleanup 뒤에는 `env`뿐 아니라 `launchctl getenv ANTHROPIC_API_KEY`까지 보고, 실행 중인 셸/세션 stale state를 감안해야 한다. [Task 1]
- Claude 전역 지침 파일은 `/Users/wooojin/.claude/CLAUDE.md`, Codex 전역 지침은 `/Users/wooojin/.codex/AGENTS.md`다. 내용을 복제할 때는 source는 그대로 두고 Claude 사본의 skill path만 `.claude/skills/...`로 바꾼다. [Task 2]
- Simple Codex user skills were nearly 1:1 syncable to `/Users/wooojin/.claude/skills`, with `.DS_Store` and `.system` metadata differences; agent-environment-dependent skills require an adapted port and validation instead of a blind copy. [Task 2][Task 3]
- At the 2026-08-04 check, Claude used `Agent`; `meight` routed Codex worker/mate work and `consult` the external high-quality review route. The installed targets were `/Users/wooojin/.claude/skills/framing` and `/Users/wooojin/.claude/skills/reframing`; recheck these environment-dependent names and paths before a later port. [Task 3]
- For a Claude skill port, verify in this order: file tree, frontmatter, internal relative links, JSON validity (for example `trigger-evals.json`), grep for Codex-only remnants, then a fresh Claude-session `/framing` and `/reframing` discovery smoke test. `framing` is for unusual design forks; `reframing` is manual after user approval when the team is stuck or options converge. [Task 3]

## Failures and how to do differently

- 증상: API key backup을 만들었는데 secret이 그대로 남았다. 원인: backup 정책이 사용자 요청 취지보다 앞섰다. 수정: secret-bearing backup도 scrub/delete 대상으로 포함한다. [Task 1]
- 증상: broad path rewrite가 Codex 원본 `AGENTS.md`까지 건드릴 뻔했다. 원인: source와 target 경로를 분리하지 않고 치환했다. 수정: copy본만 rewrite하고 원본 diff를 즉시 재검토한다. [Task 2]
- Symptom: a helper cannot write directly under `~/.claude/skills` and reports a `sensitive file` boundary. Cause: the target path is protected in that execution environment. Fix: create the port first in an allowed staging directory such as `/Users/wooojin/Downloads/claude-framing-skills-staging`, then have the authorized outer process perform the final move. [Task 3]
- Symptom: a staged port retains `Task(Agent)`, a nonexistent `roo-channel` reference, or root-relative `references/...` links. Cause: Codex-specific wording and paths were copied without checking the target layout. Fix: compare against actual `CLAUDE.md`/existing skills and validate links from each file's directory before installation. [Task 3]

# Task Group: Maplog live-map QA native-quality escalation
scope: Maplog live map QA처럼 지도/실시간 UI에서 체감 품질이 부족할 때, 현재 구현 계층 튜닝을 계속할지 native/정석 계층으로 피벗할지 판단하는 작업에 쓴다. 성능 수치 자체보다 marker sync 같은 핵심 품질 기준 충족 여부를 본다.
applies_to: cwd=/Users/wooojin/Documents/Codex/2026-06-07/maplog-side-qa; reuse_rule=Maplog 계열 QA와 지도/캔버스/미디어/실시간 UI 품질 판단에는 재사용 가능하지만, 실제 SDK 선택과 구현 범위는 현재 프로젝트 구조를 다시 확인해야 한다.

## Task 1: Prefer native overlay over tuned SwiftUI compromise for live map marker sync, success

### rollout_summary_files

- extensions/ad_hoc/notes/20260607-215956-maplog-native-quality-principle.md (cwd=/Users/wooojin/Documents/Codex/2026-06-07/maplog-side-qa, rollout_path=none, updated_at=2026-06-07T21:59:56+09:00, thread_id=none, authoritative extension note on native-quality pivot) [ad-hoc note]

### keywords

- Maplog, live map QA, SwiftUI overlay, 60fps, marker 위치 동기화, NMFMarker, native overlay, 네이버 지도 앱, scenario expected actual verdict evidence follow-up

## User preferences

- when app quality still felt wrong after tuning, the note preserved: `조금 나아진 타협안`보다 `사용자가 요구한 핵심 품질을 만족하는 정석 구현` -> 체감 품질이 큰 UI는 미세튜닝 성과보다 품질 ceiling을 먼저 봅니다. [Task 1] [ad-hoc note]
- when native marker sync finally matched the desired feel and the user reacted `이거야` -> 품질 기준이 명확히 드러난 순간에는 `충분히 괜찮음`에서 멈추지 않고 first-party/native 구현 가능성을 먼저 검토합니다. [Task 1] [ad-hoc note]

## Reusable knowledge

- SwiftUI overlay 라벨을 `60fps`까지 올려도 marker 위치 동기화가 어긋나면 성능 문제가 아니라 계층 적합성 문제일 수 있다. 이 경우 Naver SDK `NMFMarker` 같은 native overlay가 정석 해법이 될 수 있다. [Task 1] [ad-hoc note]
- 비슷한 QA에서는 `현재 구현 계층에서 구조적으로 가능한가`, `native SDK / first-party API / proven engine이 더 맞는가`, `튜닝 전에 계층 전환이 정석인가`를 먼저 묻는 편이 시행착오를 줄인다. [Task 1] [ad-hoc note]
- QA 메모를 `scenario / expected / actual / verdict / evidence / follow-up` 순서로 남기면 품질 판단과 피벗 근거가 선명해진다. [Task 1] [ad-hoc note]

## Failures and how to do differently

- 증상: `60fps` 튜닝 뒤에도 사용자는 품질 부족으로 느꼈다. 원인: 프레임레이트 개선과 marker 위치 동기화 정확도는 다른 문제였고, 현재 계층이 요구 품질을 구조적으로 못 맞췄다. 수정: 추가 튜닝 전에 native overlay 전환 가능성부터 평가한다. [Task 1] [ad-hoc note]
