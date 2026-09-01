---
name: research-browser-router
description: >-
  Route current external-evidence work among ChatGPT web consult quick/deep,
  Grok High public or logged-in Aside browser work, and local verification.
  Use when a task needs research, a second opinion, current web sources, or
  browser interaction. Skip local-only work and direct stable lookups.
---

# Research Browser Router

Keep the active work session in charge of the question, permissions, evidence, final verification, synthesis, and cleanup. External models provide leads or judgment; they do not make a claim verified and do not own the final decision.

Automatic invocation is enabled. Requests such as “리서치해줘”, “최신 자료 확인”, “공개 반응 찾아봐”, or “로그인 페이지에서 확인해줘” should load this router first. Loading the router does not require an external call: local evidence still wins when it already answers the question.

## Route

Use the smallest surface that can change the answer:

- Local repo, supplied files, or a stable direct fact is sufficient: stay local.
- A bounded public-source comparison, current-doc check, or short independent judgment: use `consult --mode quick`. Aside verifies GPT-5.6 Sol with `매우 높음` reasoning in ChatGPT web.
- A difficult, high-impact, or multi-part public analysis needs sustained judgment: use `consult --mode deep` with GPT-5.6 Sol Pro. Length alone is not a reason to promote a simple task.
- Public discovery needs wide search, counterexamples, community signals, or several pages visited: use the Grok runner.
- Login state, JavaScript rendering, visual evidence, downloads, filters, forms, or exact clicks are needed: use the same Grok runner. Grok operates the logged-in Aside browser through MCP and completes reversible browser work end to end.
- A deterministic browser path is already verified and encoded with exact selectors, an API contract, and a postcondition: execute it directly with the routed browser CLI instead of paying Grok reasoning latency again. Escalate back to Grok only when the page or contract no longer matches.
- Sol normally reads the compact report and performs the final comparison. Sol should not mirror Grok's browser steps or take over routine clicking.

Aside CLI account authentication and target-site authentication are separate. Verify the target site before spending a query or changing filters. CLI-managed tabs may be headless and need not appear as a visible macOS browser window; never tell the user a visible tab is open unless a desktop window was actually observed.

Grok may use Aside's existing login state but must not extract or report cookies, tokens, session identifiers, or unrelated private content. Purchases, applications, submissions, messages, deletion, account/security changes, and other consequential mutations still require explicit authorization before the final action.

Consult uses Aside's logged-in personal ChatGPT Pro session. Its task-owned ChatGPT tab counts as one of the two Aside scratch tabs, and the consult runner must close it after saving the response and conversation URL.

## Budgets and handoffs

Before an external call, state one decision question and what evidence would stop the search. Prefer one external reasoning call at a time. Run independent calls in parallel only when comparison value exceeds the extra tabs, cost, and synthesis work.

For Grok, use `scripts/run_grok_research.py`; do not reproduce its CLI flags ad hoc. The runner launches Aside's connected `xai-grok-oauth/grok-4.6` agent, budgets pages/actions and wall time, saves partial output, terminates the process group, and cleans task-owned browser tabs. Grok completes exact reversible interactions itself and reports evidence, state changes, and any consequential approval still needed.

Use quick for a bounded lookup or one short interaction path. Use deep for multi-step forms, three or more independent comparisons, or work that must repeatedly apply and reset state. In the task packet, tell Grok to extract scoped text first and stop once the requested fields are verified. Request screenshots only when pixels are evidence or scoped text is contradictory; do not spend the run collecting duplicate proof after the decision values are already present.

Do not bundle several high-cardinality marketplace searches into one Grok run. When one item can return hundreds of rows, give Grok one item and a maximum of three result pages to discover the useful sort/tooltip path. Once selectors and postconditions are known, continue the remaining pages or sibling items with deterministic browser CLI. This limits exposure to provider-capacity failures and preserves completed mutations even when the model cannot produce a final report.

When Grok can run independently alongside useful local work, use the managed background callback in [references/background-callback.md](references/background-callback.md). Start it first with a fixed `--run-id`, pass `--timeout 0`, yield immediately, and let its `finally`-guarded terminal `notify()` resume the active task. The runner still enforces the action budget and a no-output watchdog. After local work is exhausted, stop generating tool calls and commentary; do not call `functions.wait` or emit periodic status messages. The background cell's internal process wait does not enter model context, and its terminal `notify()` is the only completion wake-up. Do not finalize the user turn before decision-critical evidence arrives.

Run the Python wrapper without an outer PTY; the wrapper owns the child process group and lifecycle. Give each mission a stable `--mission-id`, list the minimum `--allowed-tool` values, and restrict known sites with `--allowed-domain`.

Grok browser work defaults to the isolated Aside account `u1`. The personal account `u0` is rejected before launch unless the caller explicitly passes `--allow-personal-account`; do not use that exception for ordinary work. If u1 lacks provider authentication, stop and ask for the isolated account to be connected rather than falling back to u0.

Each invocation writes a unique run under `.research/grok/runs/<run_id>/`. Treat `.research/grok/latest.json` as the pointer to the current terminal run. A result is readable only when its `done.json` has the same `runId`, a terminal state, no forbidden tools, restored browser invariants, `orphanCheck: gone`, and `remoteAgentState: cli_exited`. Never treat the compatibility files at `.research/grok/grok-report.md` or `.research/grok/grok-run.json` as current without this check.

On success, Sol reads only the run's `grok-report.md`, `grok-run.json`, and `done.json`. Do not load raw stdout/stderr unless the run failed, the result contradicts recorded browser state, or the harness reports a protocol violation.

For Consult, keep the packet self-contained and narrow. Use quick by default; promote to deep only for decision risk or multi-part reasoning. Length alone is not enough. Continue the saved conversation URL for a narrow follow-up instead of opening another conversation.

Use direct `aside repl` from Sol for a concrete contradiction, runner failure, final verification, or a previously verified deterministic path. It is not the default for unknown-page exploration.

For navigation, filtering, forms, or temporary state changes, prefer the existing `about:blank` scratch tab or one task-owned tab even when a relevant user tab exists. Reuse an existing user tab only for inspection that depends on that exact ephemeral state. Restore scratch tabs to `about:blank`; close other task tabs. The runner treats a blank scratch tab as neutral browser state because Aside may keep a closed tab target alive.

Treat every external result as provisional. Decision-critical claims become verified only after the active work session checks the underlying primary URL or the saved browser artifact. Preserve the retrieval time for freshness-sensitive facts.

## Browser and process cleanup

Existing user tabs are never owned by the task and must not be closed or navigated away from. Close task-owned Aside tabs in reverse order and list tabs again to verify the baseline. Exit the persistent Aside CLI session after cleanup.

The Consult runner always closes its task-owned Aside tab after capturing the response or failure evidence. It preserves only the ChatGPT conversation URL for a later follow-up; it never leaves a hidden generation or an untracked provider tab running.

Terminate Grok processes started by the task after a final or partial report is saved. Never leave an untracked retry running. Report which surfaces ran, what evidence was saved, and anything that could not be closed or verified.

## Grok command

Quick research or browser work:

```bash
python3 /Users/wooojin/.codex/skills/research-browser-router/scripts/run_grok_research.py \
  --mode quick \
  --mission-id "<one-site-one-decision>" \
  --allowed-tool repl \
  --allowed-domain example.com \
  --question "<one exact research or browser task>"
```

`--timeout 0` disables the fixed wall-clock deadline, not every safety boundary. Use it only through the managed background callback; the default idle watchdog remains 600 seconds, `--idle-timeout` can tune it, and the reference documents graceful cancellation.

Use `--mode deep` only when wider source coverage can materially change the decision. Outputs are saved under `.research/grok/`: `grok-brief.md`, `grok-report.md`, `grok-run.json`, and stdout/stderr logs.

Exit codes are `0` complete, `1` failed without a usable report, `2` invalid input, and `3` partial or unstructured report saved. Code `3` is evidence to inspect, not permission to retry automatically.

Before promoting a runner change, run `python3 scripts/test_grok_harness.py`. For a live pilot, use one primary site and a read-only or reversible mission, then require exact expected values, zero forbidden tools, restored tabs, and no orphan process before expanding scope.
