"""Failure injection for the send runner: what the engine reports when the
REPL ends without proof, and that the send script never runs twice.

Background (2026-09-29): two real sends were reported as `exit 75 — 전송 안 됨`
because the transcript had no submission marker, yet both had reached ChatGPT.
A missing marker proves nothing; only an explicit pre-submit stage failure does.
"""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_aside_repl_outpost.py"
SPEC = importlib.util.spec_from_file_location("run_aside_repl_outpost_state_test", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


SUBMIT_LINE = (
    'ASIDE_REPL_SUBMIT_RESULT {"quality":"pro","model":"최신","tier":"Pro (5 of 5)","submitElapsedMs":1234,'
    '"conversationUrl":"https://chatgpt.com/g/g-p-test-work/c/1","targetId":"target"}'
)
RESPONSE_LINE = (
    'ASIDE_REPL_RESPONSE_RESULT {"modelSlug":"gpt-6-pro","responseText":"ok",'
    '"responseElapsedMs":5678,"conversationUrl":"https://chatgpt.com/g/g-p-test-work/c/1"}'
)


class FakeRepl:
    """A fake `aside` on PATH. Each call prints the next scripted transcript and
    counts how many times the send script was run."""

    def __init__(self, root: Path, transcripts: list[str], counter_dir: Path | None = None) -> None:
        self.root = root
        # The counter lives outside `root` so it can be read after the fake's
        # temp dir is gone.
        self.counter = (counter_dir or root) / "runs"
        self.counter.write_text("0", encoding="utf-8")
        script_lines = ["#!/bin/sh", f"n=$(cat '{self.counter}')", "n=$((n + 1))", f"printf '%s' \"$n\" > '{self.counter}'"]
        for index, transcript in enumerate(transcripts, start=1):
            body = Path(root / f"transcript{index}.txt")
            body.write_text(transcript, encoding="utf-8")
            script_lines.append(f"[ \"$n\" -eq {index} ] && cat '{body}' && exit 0")
        script_lines.append("exit 0")
        fake = root / "aside"
        fake.write_text("\n".join(script_lines) + "\n", encoding="utf-8")
        fake.chmod(0o755)

    @property
    def runs(self) -> int:
        return int(self.counter.read_text(encoding="utf-8") or "0")

    def path_env(self) -> dict[str, str]:
        return {"PATH": f"{self.root}{os.pathsep}{os.environ.get('PATH', '')}"}


class SubmissionStateTest(unittest.TestCase):
    def setUp(self) -> None:
        self._sessions_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._sessions_dir.cleanup)
        env = mock.patch.dict(
            os.environ,
            {"OUTPOST_SESSIONS_PATH": str(Path(self._sessions_dir.name) / "sessions.json")},
        )
        env.start()
        self.addCleanup(env.stop)
        self._keep = tempfile.TemporaryDirectory()
        self.addCleanup(self._keep.cleanup)
        self.keep = Path(self._keep.name)

    # --- runner -----------------------------------------------------------

    def test_transcript_without_marker_is_unknown_not_unsent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repl = FakeRepl(Path(temp), counter_dir=self.keep, transcripts=["some REPL chatter\nno markers at all\n"])
            with mock.patch.dict(os.environ, repl.path_env()):
                with mock.patch.object(MODULE, "recover_outpost_from_backend", return_value=None) as recover:
                    with self.assertRaises(MODULE.SubmitUnknownError) as raised:
                        MODULE.run_repl_outpost("ignored", submit_timeout=1, response_timeout=1, outpost_id="abc123")
            text = str(raised.exception)
        recover.assert_called_once_with("abc123")
        self.assertEqual(repl.runs, 1)
        self.assertIn("do not retry", text)
        self.assertNotIn("전송 안 됨", text)
        self.assertNotIn("was not sent", text)

    def test_daemon_lost_after_click_runs_send_script_once(self) -> None:
        # Attempt 1: the daemon dies right after the click, before any marker.
        # Attempt 2 would be a second Pro turn; it must never happen.
        with tempfile.TemporaryDirectory() as temp:
            repl = FakeRepl(
                Path(temp),
                counter_dir=self.keep,
                transcripts=[
                    "fetch failed: other side closed\nAside daemon is not reachable\n",
                    SUBMIT_LINE + "\n" + RESPONSE_LINE + "\n",
                ],
            )
            with mock.patch.dict(os.environ, repl.path_env()):
                with mock.patch.object(MODULE, "ensure_aside_daemon", return_value=None):
                    with mock.patch.object(MODULE, "recover_outpost_from_backend", return_value=None):
                        with self.assertRaises(MODULE.SubmitUnknownError):
                            MODULE.run_repl_outpost("ignored", submit_timeout=1, response_timeout=1, outpost_id="abc123")
        self.assertEqual(repl.runs, 1)

    def test_daemon_lost_after_click_recovers_from_backend(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repl = FakeRepl(Path(temp), counter_dir=self.keep, transcripts=["Aside daemon is not reachable\n"])
            submitted_seen: list[dict] = []
            with mock.patch.dict(os.environ, repl.path_env()):
                with mock.patch.object(
                    MODULE,
                    "recover_outpost_from_backend",
                    return_value={
                        "ok": True,
                        "responseText": "recovered",
                        "modelSlug": "gpt-6-pro",
                        "finished": True,
                        "idMatched": True,
                        "conversationUrl": "https://chatgpt.com/c/abc",
                    },
                ):
                    submitted, response, _s, _r, _t = MODULE.run_repl_outpost(
                        "ignored", submit_timeout=1, response_timeout=1, outpost_id="abc123", on_submit=submitted_seen.append
                    )
        self.assertEqual(repl.runs, 1)
        self.assertTrue(response["recoveredFromBackend"])
        self.assertEqual(submitted["conversationUrl"], "https://chatgpt.com/c/abc")
        self.assertEqual(len(submitted_seen), 1)

    def test_pre_submit_stage_failure_is_provably_unsent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repl = FakeRepl(Path(temp), counter_dir=self.keep, transcripts=["OUTPOST_FAIL stage=attach-packet packet attachment missing before send\n"])
            with mock.patch.dict(os.environ, repl.path_env()):
                with mock.patch.object(MODULE, "recover_outpost_from_backend") as recover:
                    with self.assertRaises(MODULE.NotSubmittedError) as raised:
                        MODULE.run_repl_outpost("ignored", submit_timeout=1, response_timeout=1, outpost_id="abc123")
        recover.assert_not_called()
        self.assertEqual(repl.runs, 1)
        self.assertIn("exit 75 — 전송 안 됨", str(raised.exception))
        self.assertIn("attach-packet", str(raised.exception))

    def test_click_stage_failure_is_not_proof_of_unsent(self) -> None:
        self.assertEqual(MODULE.classify_send_transcript("OUTPOST_FAIL stage=commit-user-turn click timed out\n"), "unknown")
        self.assertEqual(MODULE.classify_send_transcript("OUTPOST_FAIL stage=select-tier no Pro button\n"), "not_submitted")
        self.assertEqual(MODULE.classify_send_transcript(""), "unknown")
        self.assertEqual(MODULE.classify_send_transcript(SUBMIT_LINE + "\n"), "submitted")

    def test_send_script_makes_click_failure_and_deadline_explicit(self) -> None:
        script = MODULE.build_repl_script(
            project_url="https://chatgpt.com/g/g-p-test-work/project",
            project_name="Work",
            quality="pro",
            packet_name="outpost-x.md",
            packet_base64="",
            topic="t",
            outpost_id="x",
            response_timeout_ms=1000,
        )
        self.assertIn("OUTPOST_FAIL stage=ready-to-send pre-submit preparation exceeded 120 seconds", script)
        self.assertIn("send click did not complete", script)

    # --- main: exit code and saved state ---------------------------------

    def _main_args(self, root: Path, packet: Path) -> list[str]:
        return [
            "--quality", "pro",
            "--packet", str(packet),
            "--url", "https://chatgpt.com/g/g-p-test-work/project",
            "--response-output", str(root / "response.md"),
            "--json-output", str(root / "result.json"),
            "--stderr-output", str(root / "stderr.log"),
        ]

    def test_main_reports_76_and_blocks_resend_when_marker_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repl = FakeRepl(root, counter_dir=self.keep, transcripts=["no markers\n", SUBMIT_LINE + "\n" + RESPONSE_LINE + "\n"])
            packet = root / "packet.md"
            packet.write_text("# Test topic\n\nquestion", encoding="utf-8")
            with mock.patch.dict(os.environ, repl.path_env()):
                with mock.patch.object(MODULE, "ensure_aside_daemon", return_value=None):
                    with mock.patch.object(MODULE, "recover_outpost_from_backend", return_value=None):
                        first = MODULE.main(self._main_args(root, packet))
                        second = MODULE.main(self._main_args(root, packet))
            state = json.loads((root / "result.json").read_text(encoding="utf-8"))
            stderr = (root / "stderr.log").read_text(encoding="utf-8")
        self.assertEqual(first, 76)
        self.assertEqual(second, MODULE.DUPLICATE_SEND_EXIT)
        self.assertEqual(repl.runs, 1)
        self.assertEqual(state["status"], "submit_unknown")
        self.assertTrue(state["id"])
        self.assertIn("제출 여부 불명", stderr)
        self.assertNotIn("전송 안 됨", stderr)

    def test_main_reports_75_and_allows_resend_after_proven_pre_submit_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repl = FakeRepl(
                root,
                counter_dir=self.keep,
                transcripts=[
                    "OUTPOST_FAIL stage=select-tier Pro button missing\n",
                    SUBMIT_LINE + "\n" + RESPONSE_LINE + "\n",
                ],
            )
            packet = root / "packet.md"
            packet.write_text("# Test topic\n\nquestion", encoding="utf-8")
            with mock.patch.dict(os.environ, repl.path_env()):
                with mock.patch.object(MODULE, "ensure_aside_daemon", return_value=None):
                    first = MODULE.main(self._main_args(root, packet))
                    state_after_first = json.loads((root / "result.json").read_text(encoding="utf-8"))
                    second = MODULE.main(self._main_args(root, packet))
        self.assertEqual(first, 75)
        self.assertEqual(state_after_first["status"], "not_submitted")
        self.assertEqual(state_after_first["failureStage"], "select-tier")
        self.assertEqual(second, 0)
        self.assertEqual(repl.runs, 2)


if __name__ == "__main__":
    unittest.main()
