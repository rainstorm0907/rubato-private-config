"""Tests for the one-command Consult entry point."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import consult  # noqa: E402


class DirectConsultCommandTest(unittest.TestCase):
    def test_quick_uses_one_verified_runner_pipeline(self):
        args = consult.parse_args(["--question", "Which fix is safer?", "--files", "src/a.py"])
        build, prepare, run = consult.build_commands(args, Path("/tmp/repo"))
        self.assertIn("src/a.py", build)
        self.assertNotIn("--deep", build)
        self.assertEqual(prepare[prepare.index("--mode") + 1], "quick")
        self.assertEqual(run[run.index("--mode") + 1], "quick")
        self.assertNotIn("--project-url", run)

    def test_deep_selects_broad_packet_and_pro_mode(self):
        args = consult.parse_args(["--question", "Research this precisely", "--deep", "--dry-run"])
        build, prepare, run = consult.build_commands(args, Path("/tmp/repo"))
        self.assertIn("--deep", build)
        self.assertEqual(prepare[prepare.index("--mode") + 1], "deep")
        self.assertEqual(run[run.index("--mode") + 1], "deep")
        self.assertIn("--dry-run", run)

    def test_default_collection_reopens_a_short_resume_connection(self):
        args = consult.parse_args(["--question", "Collect this safely"])
        _build, _prepare, run = consult.build_commands(args, Path("/tmp/repo"))
        resume = consult.build_resume_command(args, run)
        self.assertIn("--resume", resume)
        self.assertEqual(resume[resume.index("--timeout") + 1], "30")
        self.assertNotIn("--packet", resume)
        self.assertNotIn("--prompt-file", resume)
        self.assertNotIn("--new", resume)

    def test_conflicting_send_and_verification_modes_fail_before_building(self):
        with self.assertRaises(SystemExit):
            consult.parse_args(
                ["--question", "Do not build this", "--send-only", "--dry-run"]
            )

    def test_collector_disconnect_retries_resume_without_resubmitting(self):
        return_codes = [0, 0, 0, 4, 0]
        with tempfile.TemporaryDirectory() as output_dir, mock.patch.object(
            consult.subprocess,
            "run",
            side_effect=[mock.Mock(returncode=code) for code in return_codes],
        ) as run_mock, mock.patch.object(consult.time, "sleep"), contextlib.redirect_stdout(
            stdout := io.StringIO()
        ), contextlib.redirect_stderr(stderr := io.StringIO()):
            result = consult.main([
                "--question",
                "Retry collection only",
                "--output-dir",
                output_dir,
                "--collect-attempts",
                "2",
            ])
        self.assertEqual(result, 0)
        commands = [call.args[0] for call in run_mock.call_args_list]
        self.assertEqual(sum("--send-only" in command for command in commands), 1)
        self.assertEqual(sum("--resume" in command for command in commands), 2)
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(stdout.getvalue().count("\n"), 2)
        self.assertIn("consult complete after 2 collection attempt(s)", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
