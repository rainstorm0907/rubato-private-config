#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import io
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).with_name("run_grok_research.py")
SPEC = importlib.util.spec_from_file_location("run_grok_research", MODULE_PATH)
assert SPEC and SPEC.loader
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class GrokHarnessTests(unittest.TestCase):
    def test_atomic_write_replaces_content_without_temp_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "status.json"
            runner.atomic_write_text(target, "one")
            runner.atomic_write_text(target, "two")
            self.assertEqual(target.read_text(), "two")
            self.assertEqual([path.name for path in target.parent.iterdir()], ["status.json"])

    def test_detects_colored_forbidden_tool(self) -> None:
        line = "\x1b[32mbash\x1b[0m(title: 'scan')\n"
        self.assertEqual(runner.tool_calls_in_line(line), ["bash"])

    def test_detects_plain_allowed_tool(self) -> None:
        self.assertEqual(runner.tool_calls_in_line("repl(title: 'read')\n"), ["repl"])

    def test_ignores_tool_name_in_prose(self) -> None:
        self.assertEqual(runner.tool_calls_in_line("Do not call bash(command).\n"), [])

    def test_extracts_one_closed_report(self) -> None:
        body = "\n".join(runner.REQUIRED_HEADINGS)
        raw = f"noise\n{runner.REPORT_START}\n{body}\n{runner.REPORT_END}\n"
        report, closed, violations = runner.extract_report(raw)
        self.assertTrue(closed)
        self.assertEqual(violations, [])
        self.assertIn("## 직접 관찰", report)

    def test_ignores_report_markers_inside_dim_thinking_block(self) -> None:
        body = "\n".join(runner.REQUIRED_HEADINGS)
        raw = (
            f"\x1b[2mThinking: draft {runner.REPORT_START}\n"
            "## 직접 관찰\n\x1b[0m\n"
            f"{runner.REPORT_START}\n{body}\n{runner.REPORT_END}\n"
        )
        report, closed, violations = runner.extract_report(raw)
        self.assertTrue(closed)
        self.assertEqual(violations, [])
        self.assertIn("## 직접 관찰", report)

    def test_multiple_report_starts_fail_closed(self) -> None:
        raw = f"{runner.REPORT_START}\nold\n{runner.REPORT_START}\nnew\n{runner.REPORT_END}"
        report, closed, violations = runner.extract_report(raw)
        self.assertFalse(closed)
        self.assertIn("multiple_report_starts", violations)
        self.assertEqual(report, "new")

    def test_missing_report_end_is_partial(self) -> None:
        report, closed, violations = runner.extract_report(f"{runner.REPORT_START}\npartial")
        self.assertFalse(closed)
        self.assertEqual(report, "partial")
        self.assertIn("missing_report_end", violations)

    def test_missing_report_start_has_no_log_fallback(self) -> None:
        report, closed, violations = runner.extract_report("tool output only")
        self.assertEqual(report, "")
        self.assertFalse(closed)
        self.assertEqual(violations, ["missing_report_start"])

    def test_browser_invariants_accept_exact_baseline(self) -> None:
        tabs = [{"targetId": "a", "title": "Auction", "url": "https://example.com", "active": True}]
        result = runner.browser_invariants(tabs, list(tabs))
        self.assertTrue(result["ok"])

    def test_browser_invariants_reject_missing_changed_and_extra_tabs(self) -> None:
        baseline = [
            {"targetId": "a", "title": "Auction", "url": "https://example.com"},
            {"targetId": "b", "title": "Guide", "url": "https://guide.example.com"},
        ]
        final = [
            {"targetId": "a", "title": "Changed", "url": "https://other.example.com"},
            {"targetId": "c", "title": "Extra", "url": "https://extra.example.com"},
        ]
        result = runner.browser_invariants(baseline, final)
        self.assertFalse(result["ok"])
        self.assertEqual(result["missingBaselineTargetIds"], ["b"])
        self.assertEqual(result["extraTargetIds"], ["c"])
        self.assertEqual(len(result["changedExistingTabs"]), 1)

    def test_browser_invariants_ignore_blank_scratch_tab(self) -> None:
        baseline = [{"targetId": "a", "title": "Auction", "url": "https://example.com"}]
        final = [
            {"targetId": "a", "title": "Auction", "url": "https://example.com"},
            {"targetId": "scratch", "title": "", "url": "about:blank"},
        ]
        result = runner.browser_invariants(baseline, final)
        self.assertTrue(result["ok"])
        self.assertEqual(result["extraTargetIds"], [])
        self.assertEqual(result["ignoredScratchTargetIds"], ["scratch"])

    def test_browser_invariants_allow_only_one_blank_scratch(self) -> None:
        baseline: list[dict[str, object]] = []
        final = [
            {"targetId": "scratch-1", "title": "", "url": "about:blank"},
            {"targetId": "scratch-2", "title": "", "url": "about:blank"},
        ]
        result = runner.browser_invariants(baseline, final)
        self.assertFalse(result["ok"])
        self.assertEqual(result["ignoredScratchTargetIds"], ["scratch-1"])
        self.assertEqual(result["extraTargetIds"], ["scratch-2"])

    def test_browser_invariants_reject_new_scratch_when_baseline_has_one(self) -> None:
        baseline = [{"targetId": "scratch-1", "title": "", "url": "about:blank"}]
        final = baseline + [{"targetId": "scratch-2", "title": "", "url": "about:blank"}]
        result = runner.browser_invariants(baseline, final)
        self.assertFalse(result["ok"])
        self.assertEqual(result["ignoredScratchTargetIds"], [])
        self.assertEqual(result["extraTargetIds"], ["scratch-2"])

    def test_prompt_names_tool_and_domain_boundaries(self) -> None:
        prompt = runner.build_prompt("read only", 2, 3, ["repl"], ["maplescouter.com"])
        self.assertIn("The only allowed tools are: repl", prompt)
        self.assertIn("Allowed domains: maplescouter.com", prompt)
        self.assertIn("After printing the report start marker, call no more tools", prompt)
        self.assertIn("Reuse an existing `about:blank` tab as the task-owned scratch tab", prompt)
        self.assertIn("Prefer scoped textual extraction", prompt)

    def test_isolated_browser_account_is_default(self) -> None:
        args = runner.parse_args(["--question", "read only"])
        self.assertEqual(args.browser_account, "u1")
        self.assertFalse(args.allow_personal_account)

    def test_explicit_zero_timeout_is_preserved(self) -> None:
        args = runner.parse_args(["--question", "read only", "--timeout", "0"])
        self.assertEqual(args.timeout, 0)
        self.assertEqual(runner.resolve_timeout(args.timeout, 480), 0)
        self.assertEqual(runner.resolve_timeout(None, 480), 480)
        self.assertEqual(runner.resolve_idle_timeout(0, None), 600)
        self.assertEqual(runner.resolve_idle_timeout(0, 120), 120)
        self.assertEqual(runner.resolve_idle_timeout(480, None), 0)

    def test_allowed_action_count_ignores_forbidden_events(self) -> None:
        events = [
            {"tool": "repl", "allowed": True},
            {"tool": "repl", "allowed": True},
            {"tool": "bash", "allowed": False},
        ]
        self.assertEqual(runner.allowed_action_count(events), 2)

    def test_tool_after_report_start_records_protocol_violation_without_forced_stop(self) -> None:
        stream = io.StringIO(f"{runner.REPORT_START}\n\x1b[32mrepl\x1b[0m(title: 'late')\n")
        destination = io.StringIO()
        chunks: list[str] = []
        tool_events: list[dict[str, object]] = []
        violation = runner.threading.Event()
        report_started = runner.threading.Event()
        protocol: list[str] = []
        runner.pump(
            stream,
            destination,
            chunks,
            {"repl"},
            tool_events,
            violation,
            report_started,
            protocol,
        )
        self.assertFalse(violation.is_set())
        self.assertEqual(protocol, ["tool_after_report_start"])

    def test_thinking_report_marker_does_not_start_runtime_report(self) -> None:
        stream = io.StringIO(
            f"\x1b[2mThinking: draft {runner.REPORT_START}\n"
            "## 직접 관찰\n\x1b[0m\n"
            "\x1b[32mrepl\x1b[0m(title: 'still allowed')\n"
        )
        destination = io.StringIO()
        chunks: list[str] = []
        tool_events: list[dict[str, object]] = []
        violation = runner.threading.Event()
        report_started = runner.threading.Event()
        protocol: list[str] = []
        runner.pump(
            stream,
            destination,
            chunks,
            {"repl"},
            tool_events,
            violation,
            report_started,
            protocol,
        )
        self.assertFalse(report_started.is_set())
        self.assertFalse(violation.is_set())
        self.assertEqual(protocol, [])


if __name__ == "__main__":
    unittest.main()
