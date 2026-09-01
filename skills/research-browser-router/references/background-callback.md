# Background Grok callback

Use this only when the current surface exposes `functions.exec` with `yield_control()` and `notify()`. It keeps the current Codex task active while Grok runs; it is not a public cross-thread messaging API.

## Contract

1. Start Grok before local work with a caller-generated `--run-id`.
2. Pass `--timeout 0` only on this managed path. The runner still enforces the action budget and a default 600-second no-output watchdog. Override the watchdog with `--idle-timeout <seconds>`, but it must remain positive when wall time is disabled.
3. Yield immediately, continue useful local work, and do not manually poll Grok. When local work is finished, stop and wait for the callback: the caller must not use `functions.wait`, repeat status commentary, inspect timestamps, or poll the child session. The loop inside the background cell is process plumbing and does not re-enter model context.
4. The background cell owns its child session and calls `notify()` exactly once from `finally`, including tool-error paths.
5. The callback contains `runId` and `donePath`; read that exact run's `done.json`, `grok-run.json`, and `grok-report.md`. Never resolve a callback through the mutable `latest.json` pointer.
6. Do not finalize or archive the user task while decision-critical Grok evidence is pending. If the user ends or replaces the task, cancel the runner and report that cancellation instead of leaving an ownerless process.
7. An `about:blank` scratch target is neutral, but only one scratch tab is allowed. Any second scratch or nonblank extra tab is a cleanup failure.

## `functions.exec` pattern

```js
const runId = `grok-${Date.now()}-${Math.random().toString(16).slice(2, 10)}`;
const donePath = `<cwd>/.research/grok/runs/${runId}/done.json`;
let payload = { kind: "grok_done", runId, donePath, state: "starting" };

try {
  const first = await tools.exec_command({
    cmd: `python3 /Users/wooojin/.codex/skills/research-browser-router/scripts/run_grok_research.py --mode deep --timeout 0 --run-id ${runId} ...`,
    workdir: "<cwd>",
    yield_time_ms: 250,
    max_output_tokens: 2000,
  });

  if (!first.session_id) {
    payload = { ...payload, state: "terminal", output: first.output, exitCode: first.exit_code };
  } else {
    text(JSON.stringify({ kind: "grok_started", runId, sessionId: first.session_id }));
    yield_control();

    let current = first;
    while (current.session_id) {
      current = await tools.write_stdin({
        session_id: current.session_id,
        chars: "",
        yield_time_ms: 300000,
        max_output_tokens: 2000,
      });
    }
    payload = { ...payload, state: "terminal", output: current.output, exitCode: current.exit_code };
  }
} catch (error) {
  payload = { ...payload, state: "callback_error", error: String(error) };
} finally {
  notify(JSON.stringify(payload));
}
```

## Cancellation

Prefer a graceful wrapper signal so its handler terminates the Aside process group and writes terminal metadata:

```bash
kill -TERM "$(jq -r .wrapperPid '<run-dir>/grok-run.json')"
```

After the wrapper reaches a terminal state, terminate or close the background exec cell if it is still present. Do not send a second live call until the first run is terminal and its result justifies a narrow follow-up.
