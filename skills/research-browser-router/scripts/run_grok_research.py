#!/usr/bin/env python3
"""Run bounded Grok 4.6 High research in the logged-in Aside browser."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from typing import Any, TextIO
import uuid


DEFAULT_OUTPUT_DIR = ".research/grok"
ASIDE_MARKER = "__GROK_ASIDE_TABS__"
REPORT_START = "__GROK_REPORT_BEGIN__"
REPORT_END = "__GROK_REPORT_END__"
REQUIRED_HEADINGS = (
    "## 직접 관찰",
    "## 공식 확인",
    "## 해석",
    "## 미확인",
    "## 브라우저 작업",
    "## 상태 변경",
    "## 승인 필요",
)
URL_RE = re.compile(r"https?://[^\s<>\]\[)\"'`*]+")
ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
THINKING_BLOCK_RE = re.compile(r"\x1b\[2mThinking:.*?\x1b\[0m", re.DOTALL)
KNOWN_TOOL_NAMES = {
    "bash",
    "browsing_history_search",
    "edit_file",
    "memory_search",
    "read_file",
    "repl",
    "webfetch",
    "websearch",
    "write_file",
}
DEFAULT_ALLOWED_TOOLS = ("browsing_history_search", "repl", "webfetch", "websearch")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Grok research through Aside.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--question")
    source.add_argument("--brief")
    parser.add_argument("--mode", choices=("quick", "deep"), default="quick")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--timeout", type=int, default=None, help="wall-clock seconds; 0 disables the fixed deadline")
    parser.add_argument("--idle-timeout", type=int, default=None, help="seconds without runner output before cancellation; defaults to 600 when timeout is 0")
    parser.add_argument("--max-pages", type=int, default=None)
    parser.add_argument("--max-actions", type=int, default=None)
    parser.add_argument("--cwd", default=None)
    parser.add_argument("--browser-account", default="u1")
    parser.add_argument("--allow-personal-account", action="store_true")
    parser.add_argument("--provider", default="xai-grok-oauth")
    parser.add_argument("--model", default="grok-4.6")
    parser.add_argument("--mission-id", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--allowed-tool", action="append", default=None)
    parser.add_argument("--allowed-domain", action="append", default=None)
    return parser.parse_args(argv)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def atomic_write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
    try:
        with temp.open("w", encoding="utf-8") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        try:
            temp.unlink()
        except FileNotFoundError:
            pass


def iso_now() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def resolve_timeout(requested: int | None, default: int) -> int:
    return default if requested is None else requested


def resolve_idle_timeout(timeout: int, requested: int | None) -> int:
    if requested is not None:
        return requested
    return 600 if timeout == 0 else 0


def allowed_action_count(tool_events: list[dict[str, Any]]) -> int:
    return sum(1 for event in tool_events if event.get("allowed"))


def build_prompt(
    body: str,
    pages: int,
    actions: int,
    allowed_tools: list[str],
    allowed_domains: list[str],
) -> str:
    tools_text = ", ".join(allowed_tools)
    domains_text = ", ".join(allowed_domains) if allowed_domains else "task-relevant domains only"
    return f"""You are Grok 4.6 High, the research and browser-operation agent for a work session led by Sol.

Task:
{body.strip()}

Complete the research and reversible browser work yourself. Sol should receive only the compact result, not step-by-step narration.

Rules:
- The only allowed tools are: {tools_text}. Never call shell, filesystem, local-memory, session-history, or unrelated tools.
- Allowed domains: {domains_text}. Do not navigate outside this scope except a same-site login redirect.
- You may use public web research and the logged-in Aside browser state only when the allowed tools permit it.
- Maximum distinct pages inspected: {pages}. Maximum meaningful browser actions: {actions}.
- Prefer primary sources. Never promote a search snippet to verified fact without opening the source.
- Before browser work, inventory tabs. Reuse an existing `about:blank` tab as the task-owned scratch tab when available. Reuse any other existing tab only for inspection that depends on its exact ephemeral state. For navigation, filters, forms, or temporary state changes, use the scratch tab or open one task-owned tab. Restore scratch tabs to `about:blank` and close other task-owned tabs before finishing.
- Exact clicks, filters, searches, detail views, and read-only downloads are your responsibility. Inspect the updated page after each meaningful action.
- Retry a failed load or interaction at most once, then stop that branch and report the limitation.
- Restore temporary navigation on existing tabs unless the requested final state is useful to leave visible.
- Never reveal cookies, tokens, session identifiers, credentials, or unrelated private content.
- Purchases, applications, submissions, messages, deletion, account/security changes, and other consequential mutations require explicit authorization in this task. Without it, stop immediately before the final action and report the needed approval.
- Keep observations separate from inference. A number without page evidence must be written under `## 미확인`, never as observed or official.
- Do not draft an interim report in thinking or narration. Inspect every required page first. The first report marker must appear only after all tools are finished.
- If a requested value is missing from an interactive snapshot, retry once with a scoped full snapshot or scoped `innerText` before marking it unknown.
- Prefer scoped textual extraction. Capture screenshots only when pixels are evidence or scoped text is contradictory. Once every requested value is observed or explicitly unknown, stop collecting proof and clean up.
- Browser cleanup and baseline verification are tool work. Close task-owned tabs and verify the baseline before starting the report.
- Pre-report gate: every requested field is observed or explicitly unknown; every requested action is verified; task tabs are closed; baseline tabs are unchanged. Only then print the report start marker.
- After printing the report start marker, call no more tools.
- On large pages, use a selector- or ref-scoped snapshot instead of printing the full accessibility tree when the requested values can be narrowed.
- Keep the final report under 800 words unless the task explicitly requires more.

Finish with exactly one report enclosed by these markers:
{REPORT_START}
## 직접 관찰
## 공식 확인
## 해석
## 미확인
## 브라우저 작업
## 상태 변경
## 승인 필요
{REPORT_END}

Use all headings. Write `없음` where appropriate. If incomplete, put `# PARTIAL REPORT` immediately after the start marker.
"""


def tool_calls_in_line(line: str) -> list[str]:
    cleaned = ANSI_RE.sub("", line).lstrip()
    calls: list[str] = []
    for name in KNOWN_TOOL_NAMES:
        colored = f"\x1b[32m{name}\x1b" in line
        plain = cleaned.startswith(f"{name}(")
        if colored or plain:
            calls.append(name)
    return calls


def pump(
    stream: TextIO,
    destination: TextIO,
    chunks: list[str],
    allowed_tools: set[str],
    tool_events: list[dict[str, Any]],
    violation_event: threading.Event,
    report_started_event: threading.Event,
    runtime_protocol_violations: list[str],
    last_activity_at: list[float] | None = None,
) -> None:
    in_thinking = False
    for line in iter(stream.readline, ""):
        if last_activity_at is not None:
            last_activity_at[0] = time.monotonic()
        destination.write(line)
        destination.flush()
        chunks.append(line)
        cleaned = ANSI_RE.sub("", line)
        if "\x1b[2mThinking:" in line or cleaned.lstrip().startswith("Thinking:"):
            in_thinking = True
        if REPORT_START in cleaned and not in_thinking:
            if report_started_event.is_set() and "multiple_report_starts_runtime" not in runtime_protocol_violations:
                runtime_protocol_violations.append("multiple_report_starts_runtime")
                violation_event.set()
            report_started_event.set()
        for tool_name in tool_calls_in_line(line):
            allowed = tool_name in allowed_tools
            tool_events.append({"tool": tool_name, "allowed": allowed, "observedAt": iso_now()})
            if not allowed:
                violation_event.set()
            if report_started_event.is_set():
                if "tool_after_report_start" not in runtime_protocol_violations:
                    runtime_protocol_violations.append("tool_after_report_start")
        if in_thinking and "\x1b[0m" in line:
            in_thinking = False
    stream.close()


def terminate_group(proc: subprocess.Popen[str], cleanup: dict[str, Any]) -> None:
    if proc.poll() is not None:
        cleanup["signal"] = None
        return
    cleanup["signal"] = "SIGTERM"
    try:
        os.killpg(proc.pid, signal.SIGTERM)
        proc.wait(timeout=5)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        if proc.poll() is None:
            cleanup["signal"] = "SIGKILL"
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                pass


def run_aside_repl(code: str, account: str) -> tuple[int, str]:
    aside = shutil.which("aside")
    script = shutil.which("script")
    if not aside or not script:
        return 127, ""
    proc = subprocess.run(
        [script, "-q", "/dev/null", aside, "repl", "--account", account, code],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        timeout=30,
        check=False,
    )
    return proc.returncode, proc.stdout


def aside_tabs(account: str) -> tuple[list[dict[str, Any]], str | None]:
    code = (
        "const items = await listBrowserTabs(); "
        f"console.log('{ASIDE_MARKER}' + JSON.stringify(items.map(t => "
        "({targetId:t.targetId,title:t.title,url:t.url,active:t.active}))));"
    )
    try:
        return_code, output = run_aside_repl(code, account)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [], str(exc)
    index = output.rfind(ASIDE_MARKER)
    if return_code != 0 or index < 0:
        return [], "Aside tab inventory failed"
    payload = ANSI_RE.sub("", output[index + len(ASIDE_MARKER):].splitlines()[0].strip())
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        return [], str(exc)
    return data if isinstance(data, list) else [], None


def close_aside_tabs(target_ids: list[str], account: str) -> str | None:
    if not target_ids:
        return None
    code = (
        f"const ids = {json.dumps(target_ids)}; const closed = []; const reset = []; "
        "for (const id of ids) { try { const p = await attachBrowserTab(id); await closeTab(p); closed.push(id); } catch {} } "
        "const remaining = await listBrowserTabs(); "
        "for (const id of ids) { if (!remaining.some(t => t.targetId === id)) continue; "
        "try { const p = await attachBrowserTab(id); await p.goto('about:blank'); reset.push(id); } catch {} } "
        "console.log(JSON.stringify({closed,reset}));"
    )
    try:
        return_code, _ = run_aside_repl(code, account)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return str(exc)
    return None if return_code == 0 else "Aside tab cleanup failed"


def extract_report(raw: str) -> tuple[str, bool, list[str]]:
    raw = THINKING_BLOCK_RE.sub("", raw)
    cleaned = ANSI_RE.sub("", raw).replace("\r", "")
    starts = [match.start() for match in re.finditer(re.escape(REPORT_START), cleaned)]
    ends = [match.start() for match in re.finditer(re.escape(REPORT_END), cleaned)]
    violations: list[str] = []
    if len(starts) > 1:
        violations.append("multiple_report_starts")
    if len(ends) > 1:
        violations.append("multiple_report_ends")
    if not starts:
        return "", False, ["missing_report_start"]
    start = starts[-1]
    end = next((position for position in ends if position > start), -1)
    if end < 0:
        return cleaned[start + len(REPORT_START):].strip(), False, violations + ["missing_report_end"]
    return cleaned[start + len(REPORT_START):end].strip(), not violations, violations


def make_run_id() -> str:
    stamp = dt.datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%z")
    return f"{stamp}-{uuid.uuid4().hex[:8]}"


def browser_invariants(
    baseline_tabs: list[dict[str, Any]],
    final_tabs: list[dict[str, Any]],
) -> dict[str, Any]:
    baseline_by_id = {str(tab.get("targetId")): tab for tab in baseline_tabs}
    final_by_id = {str(tab.get("targetId")): tab for tab in final_tabs}
    missing = sorted(set(baseline_by_id) - set(final_by_id))
    changed = [
        {"before": baseline_by_id[target_id], "after": final_by_id[target_id]}
        for target_id in sorted(set(baseline_by_id) & set(final_by_id))
        if baseline_by_id[target_id].get("url") != final_by_id[target_id].get("url")
        or baseline_by_id[target_id].get("title") != final_by_id[target_id].get("title")
    ]
    raw_extras = sorted(set(final_by_id) - set(baseline_by_id))
    blank_extras = [
        target_id for target_id in raw_extras
        if str(final_by_id[target_id].get("url") or "") == "about:blank"
    ]
    baseline_scratch_count = sum(
        1 for tab in baseline_tabs if str(tab.get("url") or "") == "about:blank"
    )
    scratch_allowance = max(0, 1 - baseline_scratch_count)
    ignored_scratch = blank_extras[:scratch_allowance]
    extras = [target_id for target_id in raw_extras if target_id not in ignored_scratch]
    return {
        "ok": not missing and not changed and not extras,
        "missingBaselineTargetIds": missing,
        "changedExistingTabs": changed,
        "extraTargetIds": extras,
        "ignoredScratchTargetIds": ignored_scratch,
    }


def wait_for_browser_baseline(
    baseline_tabs: list[dict[str, Any]],
    account: str,
    attempts: int = 20,
    delay_seconds: float = 1.0,
) -> tuple[list[dict[str, Any]], str | None, dict[str, Any]]:
    final_tabs: list[dict[str, Any]] = []
    final_error: str | None = None
    invariants = browser_invariants(baseline_tabs, final_tabs)
    for attempt in range(attempts):
        final_tabs, final_error = aside_tabs(account)
        if final_error:
            return final_tabs, final_error, browser_invariants(baseline_tabs, final_tabs)
        invariants = browser_invariants(baseline_tabs, final_tabs)
        if invariants["ok"]:
            return final_tabs, None, invariants
        if attempt + 1 < attempts:
            time.sleep(delay_seconds)
    return final_tabs, final_error, invariants


def process_group_gone(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return True
    except PermissionError:
        return False
    return False


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.browser_account == "u0" and not args.allow_personal_account:
        print(
            "refusing Grok on personal Aside account u0; use the isolated account or pass --allow-personal-account explicitly",
            file=sys.stderr,
        )
        return 2
    aside = shutil.which("aside")
    if not aside:
        print("aside CLI not found", file=sys.stderr)
        return 127

    cwd = Path(args.cwd or os.getcwd()).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser()
    if not output_dir.is_absolute():
        output_dir = cwd / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = args.run_id or make_run_id()
    mission_id = args.mission_id or run_id
    run_dir = output_dir / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    brief_path = run_dir / "grok-brief.md"
    report_path = run_dir / "grok-report.md"
    run_path = run_dir / "grok-run.json"
    stdout_path = run_dir / "grok-stdout.log"
    stderr_path = run_dir / "grok-stderr.log"
    done_path = run_dir / "done.json"
    latest_path = output_dir / "latest.json"

    if args.brief:
        source = Path(args.brief).expanduser()
        if not source.exists():
            print(f"brief not found: {source}", file=sys.stderr)
            return 2
        body = read_text(source)
    else:
        body = str(args.question)
    if not body.strip():
        print("research question is empty", file=sys.stderr)
        return 2

    defaults = {
        "quick": {"timeout": 480, "pages": 8, "actions": 20},
        "deep": {"timeout": 900, "pages": 16, "actions": 40},
    }[args.mode]
    timeout = resolve_timeout(args.timeout, defaults["timeout"])
    idle_timeout = resolve_idle_timeout(timeout, args.idle_timeout)
    pages = args.max_pages or defaults["pages"]
    actions = args.max_actions or defaults["actions"]
    if timeout < 0 or idle_timeout < 0 or min(pages, actions) <= 0:
        print("budgets must be positive and timeouts must be non-negative", file=sys.stderr)
        return 2
    if timeout == 0 and idle_timeout == 0:
        print("timeout 0 requires a positive idle timeout", file=sys.stderr)
        return 2

    allowed_tools = list(dict.fromkeys(args.allowed_tool or DEFAULT_ALLOWED_TOOLS))
    unknown_tools = sorted(set(allowed_tools) - KNOWN_TOOL_NAMES)
    if unknown_tools:
        print(f"unknown allowed tools: {', '.join(unknown_tools)}", file=sys.stderr)
        return 2
    allowed_domains = list(dict.fromkeys(args.allowed_domain or []))
    prompt = build_prompt(body, pages, actions, allowed_tools, allowed_domains)
    atomic_write_text(brief_path, prompt)
    baseline_tabs, baseline_error = aside_tabs(args.browser_account)
    if baseline_error:
        terminal = {
            "runId": run_id,
            "missionId": mission_id,
            "state": "error",
            "reason": "browser_preflight_failed",
            "error": baseline_error,
            "completedAt": iso_now(),
        }
        atomic_write_text(done_path, json.dumps(terminal, ensure_ascii=False, indent=2) + "\n")
        atomic_write_text(latest_path, json.dumps({"runId": run_id, "runDir": str(run_dir), "state": "error"}, ensure_ascii=False, indent=2) + "\n")
        print(f"Grok browser preflight failed; see {done_path}", file=sys.stderr)
        return 1
    command = [
        aside, "exec",
        "--account", args.browser_account,
        "--model", args.model,
        "--provider", args.provider,
        "--effort", "high",
        prompt,
    ]
    metadata: dict[str, Any] = {
        "runId": run_id,
        "missionId": mission_id,
        "status": "running",
        "model": args.model,
        "provider": args.provider,
        "effort": "high",
        "mode": args.mode,
        "startedAt": iso_now(),
        "budget": {"maxPages": pages, "maxActions": actions, "timeoutSec": timeout, "idleTimeoutSec": idle_timeout},
        "cleanup": {},
        "browser": {"baseline": baseline_tabs, "baselineError": baseline_error},
        "policy": {"allowedTools": allowed_tools, "allowedDomains": allowed_domains},
        "wrapperPid": os.getpid(),
    }
    atomic_write_text(run_path, json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    atomic_write_text(
        output_dir / "grok-run.json",
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
    )
    started = time.monotonic()
    proc: subprocess.Popen[str] | None = None
    out_chunks: list[str] = []
    err_chunks: list[str] = []
    timed_out = False
    idle_timed_out = False
    aborted_signal: str | None = None
    termination_reason: str | None = None
    violation_event = threading.Event()
    report_started_event = threading.Event()
    runtime_protocol_violations: list[str] = []
    tool_events: list[dict[str, Any]] = []
    signal_event = threading.Event()
    previous_handlers: dict[int, Any] = {}
    last_activity_at = [time.monotonic()]

    def handle_signal(signum: int, _frame: Any) -> None:
        nonlocal aborted_signal
        aborted_signal = signal.Signals(signum).name
        signal_event.set()

    for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        previous_handlers[signum] = signal.getsignal(signum)
        signal.signal(signum, handle_signal)
    try:
        with stdout_path.open("w", encoding="utf-8") as out_file, stderr_path.open("w", encoding="utf-8") as err_file:
            proc = subprocess.Popen(
                command,
                cwd=str(cwd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                errors="replace",
                bufsize=1,
                start_new_session=True,
            )
            assert proc.stdout is not None and proc.stderr is not None
            threads = [
                threading.Thread(target=pump, args=(proc.stdout, out_file, out_chunks, set(allowed_tools), tool_events, violation_event, report_started_event, runtime_protocol_violations, last_activity_at), daemon=True),
                threading.Thread(target=pump, args=(proc.stderr, err_file, err_chunks, set(allowed_tools), tool_events, violation_event, report_started_event, runtime_protocol_violations, last_activity_at), daemon=True),
            ]
            for thread in threads:
                thread.start()
            deadline = None if timeout == 0 else time.monotonic() + timeout
            while proc.poll() is None:
                action_count = allowed_action_count(tool_events)
                if action_count > actions:
                    if "action_budget_exceeded" not in runtime_protocol_violations:
                        runtime_protocol_violations.append("action_budget_exceeded")
                    termination_reason = "action_budget"
                    terminate_group(proc, metadata["cleanup"])
                    break
                if violation_event.is_set():
                    termination_reason = "forbidden_tool" if any(not event["allowed"] for event in tool_events) else "protocol_violation"
                    terminate_group(proc, metadata["cleanup"])
                    break
                if signal_event.is_set():
                    termination_reason = "wrapper_signal"
                    terminate_group(proc, metadata["cleanup"])
                    break
                if deadline is not None and time.monotonic() >= deadline:
                    timed_out = True
                    termination_reason = "timeout"
                    terminate_group(proc, metadata["cleanup"])
                    break
                if idle_timeout > 0 and time.monotonic() - last_activity_at[0] >= idle_timeout:
                    idle_timed_out = True
                    termination_reason = "idle_timeout"
                    terminate_group(proc, metadata["cleanup"])
                    break
                time.sleep(0.1)
            for thread in threads:
                thread.join(timeout=2)
    except KeyboardInterrupt:
        if proc is not None:
            terminate_group(proc, metadata["cleanup"])
        raise
    finally:
        if proc is not None and proc.poll() is None:
            terminate_group(proc, metadata["cleanup"])
        for signum, handler in previous_handlers.items():
            signal.signal(signum, handler)

    raw = "".join(out_chunks)
    report, closed_marker, protocol_violations = extract_report(raw)
    protocol_violations = list(dict.fromkeys(protocol_violations + runtime_protocol_violations))
    structured = all(heading in report for heading in REQUIRED_HEADINGS)
    exit_code = proc.returncode if proc is not None else 1
    forbidden_tools = sorted({event["tool"] for event in tool_events if not event["allowed"]})
    if report:
        atomic_write_text(report_path, report.rstrip() + "\n")
    if forbidden_tools:
        status, return_code = "policy_violation", 1
    elif runtime_protocol_violations:
        status, return_code = "protocol_violation", 1
    elif aborted_signal:
        status, return_code = "aborted", 1
    elif timed_out and report:
        status, return_code = "partial", 3
    elif idle_timed_out and report:
        status, return_code = "partial", 3
    elif exit_code == 0 and closed_marker and structured and not protocol_violations:
        status, return_code = "complete", 0
    elif report:
        status, return_code = "partial", 3
    else:
        status, return_code = "error", 1

    final_tabs, final_error = aside_tabs(args.browser_account)
    baseline_ids = {str(tab.get("targetId")) for tab in baseline_tabs}
    new_ids = [str(tab.get("targetId")) for tab in final_tabs if str(tab.get("targetId")) not in baseline_ids]
    cleanup_error = close_aside_tabs(new_ids, args.browser_account)
    after_cleanup, after_cleanup_error, invariants = wait_for_browser_baseline(baseline_tabs, args.browser_account)
    if not invariants["ok"] and status == "complete":
        status, return_code = "browser_invariant_violation", 1
    metadata.update({
        "status": status,
        "completedAt": iso_now(),
        "elapsedSec": round(time.monotonic() - started, 3),
        "exitCode": exit_code,
        "timedOut": timed_out,
        "idleTimedOut": idle_timed_out,
        "structured": structured,
        "protocolViolations": protocol_violations,
        "terminationReason": termination_reason,
        "abortedSignal": aborted_signal,
        "toolEvents": tool_events,
        "forbiddenTools": forbidden_tools,
        "urls": list(dict.fromkeys(url.rstrip(".,;:!?") for url in URL_RE.findall(report))),
        "reportPath": str(report_path) if report else None,
    })
    metadata["browser"].update({
        "finalBeforeCleanup": final_tabs,
        "finalError": final_error,
        "taskTabsClosed": new_ids,
        "cleanupError": cleanup_error,
        "afterCleanup": after_cleanup,
        "afterCleanupError": after_cleanup_error,
        "invariants": invariants,
    })
    if proc is not None:
        metadata["cleanup"]["orphanCheck"] = "gone" if process_group_gone(proc.pid) else "present"
    orphan_check = metadata["cleanup"].get("orphanCheck")
    remote_agent_state = "unknown_after_forced_local_stop" if termination_reason in {"forbidden_tool", "protocol_violation", "action_budget", "wrapper_signal", "timeout", "idle_timeout"} else "cli_exited"
    metadata["cleanup"]["remoteAgentState"] = remote_agent_state
    if orphan_check != "gone" and status == "complete":
        status, return_code = "orphan_process", 1
        metadata["status"] = status
    if remote_agent_state != "cli_exited" and status == "complete":
        status, return_code = "unsafe_termination", 1
        metadata["status"] = status
    atomic_write_text(run_path, json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    if report:
        atomic_write_text(output_dir / "grok-report.md", report.rstrip() + "\n")
    atomic_write_text(output_dir / "grok-run.json", json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    done = {
        "runId": run_id,
        "missionId": mission_id,
        "state": status,
        "returnCode": return_code,
        "completedAt": metadata["completedAt"],
        "reportPath": str(report_path) if report else None,
        "runPath": str(run_path),
        "browserInvariants": invariants,
        "forbiddenTools": forbidden_tools,
        "protocolViolations": protocol_violations,
        "orphanCheck": orphan_check,
        "remoteAgentState": remote_agent_state,
    }
    atomic_write_text(done_path, json.dumps(done, ensure_ascii=False, indent=2) + "\n")
    atomic_write_text(
        latest_path,
        json.dumps({"runId": run_id, "runDir": str(run_dir), "state": status, "donePath": str(done_path)}, ensure_ascii=False, indent=2) + "\n",
    )
    if return_code == 0:
        print(f"wrote Grok report: {report_path}")
    elif report:
        print(f"saved partial Grok report: {report_path}", file=sys.stderr)
    else:
        print(f"Grok research failed without a report; see {stderr_path}", file=sys.stderr)
    return return_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
