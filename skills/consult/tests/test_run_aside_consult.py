"""Tests for the parts of the Aside consult runner that must never depend on a browser."""

from __future__ import annotations

import fcntl
import json
import contextlib
import io
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import run_aside_consult as runner  # noqa: E402


PROJECT_SLUG = "g-p-694fe6d680f08191975e034b52dde66e-ujin"
PROJECT_URL = f"https://chatgpt.com/g/{PROJECT_SLUG}/project"
PROJECT_CONVERSATION_URL = (
    f"https://chatgpt.com/g/{PROJECT_SLUG}/c/6a881c19-b2c4-83ee-9808-95efd1b9d581"
)
LEGACY_CONVERSATION_URL = "https://chatgpt.com/c/legacy123"


class ExplodingRun(AssertionError):
    """Raised when the runner would have driven the browser."""


def no_browser(*_args, **_kwargs):
    raise ExplodingRun("the runner reached the browser when it should have stopped")


def checkpoint(**overrides):
    record = {
        "status": "submitted",
        "runId": "run-1",
        "submissionId": "run-1",
        "packetHash": runner.hash_text("packet"),
        "promptHash": runner.hash_text("prompt"),
        "projectUrl": PROJECT_URL,
        "projectId": PROJECT_SLUG,
        "conversationUrl": PROJECT_CONVERSATION_URL,
        "submittedAt": "2026-08-21T00:00:00Z",
        "model": "GPT-5.6 Sol",
        "effort": "매우 높음",
        "account": "u0",
        "ownedTabLeftOpen": True,
        "ownedTabTargetId": "owned-1",
    }
    record.update(overrides)
    return record


def pending_checkpoint(**overrides):
    record = checkpoint(
        status="sending",
        conversationUrl=None,
        pendingAt="2026-08-21T00:00:00Z",
    )
    record.pop("submittedAt")
    record.update(overrides)
    return record


class FakeBrowserFixture:
    """Execute the generated REPL program against a deterministic in-memory page."""

    PRELUDE = r"""
const fixtureState = {
  url: process.env.FIXTURE_URL,
  sends: 0,
  userCount: process.env.FIXTURE_FOLLOW_UP === '1' ? 1 : 0,
  open: false,
  view: 'base',
  attached: false,
  prompt: '',
  perfClicks: 0,
  everOpened: false,
  events: [],
  closedOwned: false,
  performanceIndex: 5,
};
const performanceLabels = ['즉시', '중간', '높음', '매우 높음', 'Pro'];
const fixtureConsoleLog = console.log.bind(console);
console.log = (...args) => {
  if (String(args[0] || '').startsWith('__ASIDE_CONSULT_SUBMITTED__')) fixtureState.events.push('checkpoint');
  fixtureConsoleLog(...args);
};
const fixtureModelOk = process.env.FIXTURE_MODEL_OK !== '0';
const fixtureSurface = process.env.FIXTURE_SURFACE || 'chat-pro';
const fixturePacket = process.env.FIXTURE_PACKET;
const sleep = async () => {};
const pwd = '/tmp/fake-aside';
const fs = {writeFile: async () => {}};
const path = {join: (...parts) => parts.join('/')};
const Buffer = globalThis.Buffer;
const baseline = process.env.FIXTURE_RESUME_EXISTING === '1'
  ? [{targetId:'base-1'}, {targetId:'owned-1'}]
  : [{targetId:'base-1'}];
async function listBrowserTabs() {
  if (fixtureState.open) return baseline.some(tab => tab.targetId === 'owned-1') ? baseline : [...baseline, {targetId:'owned-1'}];
  if (fixtureState.everOpened && process.env.FIXTURE_BASELINE_GROWTH === '1') return [{targetId:'base-2'}, {targetId:'base-3'}];
  if (fixtureState.everOpened && process.env.FIXTURE_BASELINE_CHURN === '1') return [{targetId:'base-2'}];
  if (fixtureState.closedOwned) return baseline.filter(tab => tab.targetId !== 'owned-1');
  return baseline;
}
async function openTab() { fixtureState.open = true; fixtureState.everOpened = true; return fakePage; }
async function attachBrowserTab() { fixtureState.open = true; fixtureState.everOpened = true; return fakePage; }
async function closeTab() { fixtureState.open = false; fixtureState.closedOwned = true; }
function baseTree() {
  return [
    fixtureSurface === 'free'
      ? 'text "개인 계정 Free 님"'
      : fixtureSurface === 'new-pro'
        ? `button "프로필 메뉴 열기" [ref=profile]\nbutton "${performanceLabels[fixtureState.performanceIndex-1]}" [ref=perf]`
        : 'text "개인 계정 ChatGPT  Pro"',
    fixtureSurface === 'work' ? 'radio "Work" [checked]' : 'radio "Chat" [checked]',
    'button "매우 높음" [ref=perf]',
    fixtureState.attached ? `text "${fixturePacket}"` : '',
    'textbox "ChatGPT 새 채팅" [ref=textbox]',
    'button "프롬프트 보내기" [ref=send]',
  ].join('\n');
}
async function snapshot() {
  if (fixtureState.view === 'profile') return {tree:'menuitem [ref=account]: text "WY 개인 계정"', diff:''};
  if (fixtureState.view === 'modern-menu') return {
    tree:`menuitem "모델 선택" [ref=model-select]: "${performanceLabels[fixtureState.performanceIndex-1]}"\nmenuitem "성능" [ref=performance]\ntext: "${performanceLabels[fixtureState.performanceIndex-1]}, 5개 중 ${fixtureState.performanceIndex}번째.왼쪽/오른쪽 화살표 키로 성능을 조정합니다."`,
    diff:'',
  };
  if (fixtureState.view === 'modern-model') return {
    tree:'menuitemradio "GPT-5.6 Sol" [checked] [ref=modern-model]\nmenuitemradio "GPT-5.5" [ref=other-model]',
    diff:'',
  };
  if (fixtureState.view === 'menu') return {tree: fixtureModelOk
    ? 'menuitem "모델 GPT-5.6 Sol" [ref=model]\nmenuitem "추론 수준 매우 높음" [ref=reason]'
    : 'menuitem "모델 다른 모델" [ref=model]\nmenuitem "추론 수준 매우 높음" [ref=reason]', diff:''};
  if (fixtureState.view === 'levels') return {tree:'menuitemradio "매우 높음" [checked] [ref=level]', diff:''};
  return {tree:baseTree(), diff:''};
}
function locator(selector) {
  const api = {
    count: async () => {
      if (selector === 'input[type="file"]') return 1;
      if (selector === '[data-message-author-role="user"]') return fixtureState.userCount;
      if (selector === '[data-message-author-role="assistant"]') return process.env.FIXTURE_RESPONSE === '1' ? 1 : 0;
      if (selector.includes('stop-button')) return process.env.FIXTURE_STOP_VISIBLE === '1' ? 1 : 0;
      return 0;
    },
    nth: () => api,
    setInputFiles: async () => { fixtureState.attached = true; },
    getAttribute: async () => null,
    innerText: async () => selector === '[data-message-author-role="assistant"]' ? 'fixture answer' : fixtureState.prompt,
    locator: (child) => locator(child),
    focus: async () => {},
    click: async () => {
      if (selector === 'profile') fixtureState.view = 'profile';
      if (selector === 'perf') {
        fixtureState.view = fixtureSurface === 'new-pro' ? 'modern-menu' : 'menu';
        fixtureState.perfClicks += 1;
      }
      if (selector === 'model-select') fixtureState.view = 'modern-model';
      if (selector === 'reason') fixtureState.view = 'levels';
      if (selector === 'send') {
        fixtureState.events.push('send-click');
        fixtureState.sends += 1;
        fixtureState.userCount += 1;
        if (process.env.FIXTURE_FOLLOW_UP !== '1' && process.env.FIXTURE_SLOW_URL !== '1') fixtureState.url = 'https://chatgpt.com/g/g-p-694fe6d680f08191975e034b52dde66e-ujin/c/6a881c19-b2c4-83ee-9808-95efd1b9d581';
      }
      if (selector.includes('stop-button')) fixtureState.events.push('stop-click');
    },
  };
  return api;
}
const fakePage = {
  evaluate: async () => fixtureState.url,
  locator,
  keyboard: {
    press: async (key) => {
      if (key === 'ArrowLeft' && fixtureState.view === 'modern-menu') fixtureState.performanceIndex = Math.max(1, fixtureState.performanceIndex-1);
      if (key === 'ArrowRight' && fixtureState.view === 'modern-menu') fixtureState.performanceIndex = Math.min(5, fixtureState.performanceIndex+1);
      if (key === 'Escape') fixtureState.view = 'base';
      if (key === 'Escape' && fixtureState.perfClicks >= 2 && process.env.FIXTURE_NAVIGATE === 'before-attach') {
        fixtureState.url = 'https://chatgpt.com/';
      }
    },
    insertText: async (value) => {
      fixtureState.prompt = value;
      if (process.env.FIXTURE_NAVIGATE === 'before-send') fixtureState.url = 'https://chatgpt.com/';
    },
  },
};
"""

    @classmethod
    def run_raw(
        cls, *, live_url, model_ok=True, surface="chat-pro", follow_up=False,
        phase="submit", slow_url=False, navigate=None, baseline_churn=False,
        baseline_growth=False, response=False, resume_existing=False,
        stop_visible=False, timeout_seconds=1, mode="quick",
    ):
        if not shutil.which("node"):
            raise unittest.SkipTest("node is required for the fake Aside fixture")
        js = runner.build_js(
            mode=mode,
            phase=phase,
            packet_b64=runner.encode_text("packet"),
            prompt_b64=runner.encode_text("prompt"),
            packet_name="packet.md",
            timeout_seconds=timeout_seconds,
            start_url=(PROJECT_CONVERSATION_URL if follow_up or phase == "collect" else PROJECT_URL),
            follow_up=follow_up,
            project_id=(None if follow_up else PROJECT_SLUG),
            project_url=PROJECT_URL,
            run_id="run-1",
            packet_hash=runner.hash_text("packet"),
            prompt_hash=runner.hash_text("prompt"),
            account="u0",
            resume_target_id="owned-1" if resume_existing else None,
        )
        program = cls.PRELUDE + "\n" + js + "\nconsole.log('__FIXTURE__' + JSON.stringify(fixtureState));"
        env = {
            **runner.os.environ,
            "FIXTURE_URL": live_url,
            "FIXTURE_MODEL_OK": "1" if model_ok else "0",
            "FIXTURE_SURFACE": surface,
            "FIXTURE_FOLLOW_UP": "1" if follow_up else "0",
            "FIXTURE_PACKET": "packet.md",
            "FIXTURE_SLOW_URL": "1" if slow_url else "0",
            "FIXTURE_NAVIGATE": navigate or "",
            "FIXTURE_BASELINE_CHURN": "1" if baseline_churn else "0",
            "FIXTURE_BASELINE_GROWTH": "1" if baseline_growth else "0",
            "FIXTURE_RESPONSE": "1" if response else "0",
            "FIXTURE_RESUME_EXISTING": "1" if resume_existing else "0",
            "FIXTURE_STOP_VISIBLE": "1" if stop_visible else "0",
        }
        proc = subprocess.run(
            ["node", "--input-type=module", "--eval", program],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )
        if proc.returncode:
            raise AssertionError(proc.stderr)
        fixture = runner.extract_marker(proc.stdout, "__FIXTURE__")
        result = runner.extract_marker(proc.stdout, runner.MARKER)
        submitted = runner.extract_marker(proc.stdout, runner.SUBMIT_MARKER)
        return fixture, result, submitted, proc.stdout

    @classmethod
    def run(cls, **kwargs):
        return cls.run_raw(**kwargs)[:3]


class ProjectResolutionTest(unittest.TestCase):
    def resolve(self, url):
        args = mock.Mock(project_url=url)
        with mock.patch.dict("os.environ", {}, clear=True), mock.patch.object(runner, "read_config_value", return_value=None):
            return runner.resolve_project_url(args)

    def test_project_url_yields_its_unique_id(self):
        resolved = self.resolve("https://chatgpt.com/g/g-p-abc123XY/project")
        self.assertEqual(resolved, ("https://chatgpt.com/g/g-p-abc123XY/project", "g-p-abc123XY"))

    def test_personal_chat_root_is_not_a_project(self):
        self.assertIsNone(self.resolve("https://chatgpt.com/"))

    def test_project_id_on_another_host_is_not_accepted(self):
        self.assertIsNone(self.resolve("https://example.com/g/g-p-abc123XY/project"))

    def test_missing_configuration_is_not_a_project(self):
        self.assertIsNone(self.resolve(None))

    def test_project_scoped_conversation_url_is_accepted(self):
        self.assertTrue(runner.is_conversation_url(PROJECT_CONVERSATION_URL))

    def test_legacy_unscoped_conversation_url_remains_accepted(self):
        self.assertTrue(runner.is_conversation_url(LEGACY_CONVERSATION_URL))

    def test_default_session_path_is_absolute_and_outside_the_working_directory(self):
        session_path = runner.default_session_path("u0")
        with tempfile.TemporaryDirectory(dir="/tmp") as project_dir:
            self.assertTrue(runner.DEFAULT_SESSION_DIR.is_absolute())
            self.assertTrue(session_path.is_absolute())
            self.assertFalse(session_path.resolve().is_relative_to(Path(project_dir).resolve()))


class BrowserAcceptanceFixtureTest(unittest.TestCase):
    def test_personal_chat_root_fails_before_send(self):
        fixture, result, submitted = FakeBrowserFixture.run(live_url="https://chatgpt.com/")
        self.assertEqual(fixture["sends"], 0)
        self.assertFalse(fixture["attached"])
        self.assertEqual(fixture["prompt"], "")
        self.assertFalse(result["ok"])
        self.assertIsNone(submitted)

    def test_other_project_fails_before_send(self):
        fixture, result, submitted = FakeBrowserFixture.run(
            live_url="https://chatgpt.com/g/g-p-other/project"
        )
        self.assertEqual(fixture["sends"], 0)
        self.assertFalse(fixture["attached"])
        self.assertEqual(fixture["prompt"], "")
        self.assertFalse(result["ok"])
        self.assertIsNone(submitted)

    def test_configured_project_sends_once_and_restores_tabs(self):
        fixture, result, submitted = FakeBrowserFixture.run(
            live_url=PROJECT_URL, phase="both", response=True
        )
        self.assertEqual(fixture["sends"], 1)
        self.assertTrue(result["ok"])
        self.assertTrue(result["baselineRestored"])
        self.assertEqual(result["baselineTargetIds"], ["base-1"])
        self.assertEqual(result["finalTargetIds"], ["base-1"])
        self.assertEqual(result["conversationUrl"], PROJECT_CONVERSATION_URL)
        self.assertEqual(submitted["conversationUrl"], PROJECT_CONVERSATION_URL)
        self.assertFalse(result["ownedTabLeftOpen"])
        self.assertFalse(fixture["open"])
        self.assertTrue(runner.is_valid_checkpoint(submitted))

    def test_model_verification_failure_never_sends(self):
        fixture, result, submitted = FakeBrowserFixture.run(
            live_url=PROJECT_URL, model_ok=False
        )
        self.assertEqual(fixture["sends"], 0)
        self.assertFalse(result["ok"])
        self.assertIsNone(submitted)

    def test_deep_mode_verifies_pro_without_sending(self):
        fixture, result, submitted = FakeBrowserFixture.run(
            live_url=PROJECT_URL, mode="deep", phase="verify", surface="new-pro"
        )
        self.assertEqual(fixture["sends"], 0)
        self.assertTrue(result["ok"])
        self.assertEqual(result["verifiedModel"], "GPT-5.6 Sol")
        self.assertEqual(result["verifiedEffort"], "Pro")
        self.assertIsNone(submitted)

    def test_work_or_non_pro_surface_never_sends(self):
        for surface in ("work", "free"):
            with self.subTest(surface=surface):
                fixture, result, submitted = FakeBrowserFixture.run(
                    live_url=PROJECT_URL, surface=surface
                )
                self.assertEqual(fixture["sends"], 0)
                self.assertFalse(result["ok"])
                self.assertIsNone(submitted)

    def test_new_profile_menu_personal_pro_surface_passes_account_gate(self):
        fixture, result, submitted = FakeBrowserFixture.run(
            live_url=PROJECT_URL,
            surface="new-pro",
        )
        self.assertEqual(fixture["sends"], 1)
        self.assertEqual(result["accountEvidence"], 'menuitem [ref=account]: text "WY 개인 계정"')
        self.assertIsNotNone(submitted)

    def test_send_only_does_not_wait_for_an_answer(self):
        fixture, result, submitted = FakeBrowserFixture.run(
            live_url=PROJECT_URL, phase="submit"
        )
        self.assertEqual(fixture["sends"], 1)
        self.assertTrue(result["ok"])
        self.assertNotIn("response", result)
        self.assertTrue(result["ownedTabLeftOpen"])
        self.assertEqual(result["ownedTabTargetId"], "owned-1")
        self.assertTrue(fixture["open"])
        self.assertTrue(submitted["ownedTabLeftOpen"])
        self.assertEqual(submitted["ownedTabTargetId"], "owned-1")
        self.assertTrue(runner.is_valid_checkpoint(submitted))

    def test_follow_up_uses_the_existing_conversation_url(self):
        fixture, result, submitted = FakeBrowserFixture.run(
            live_url=PROJECT_CONVERSATION_URL, follow_up=True
        )
        self.assertEqual(fixture["sends"], 1)
        self.assertEqual(result["conversationUrl"], PROJECT_CONVERSATION_URL)
        self.assertEqual(submitted["conversationUrl"], PROJECT_CONVERSATION_URL)

    def test_slow_conversation_url_emits_pending_before_result(self):
        fixture, result, submitted, stdout = FakeBrowserFixture.run_raw(
            live_url=PROJECT_URL,
            phase="both",
            slow_url=True,
            timeout_seconds=0,
        )
        self.assertEqual(fixture["sends"], 1)
        self.assertEqual(fixture["userCount"], 1)
        self.assertEqual(submitted["status"], "sending")
        self.assertIsNone(submitted["conversationUrl"])
        self.assertTrue(result["sendClicked"])
        self.assertEqual(result["conversationUrlCandidates"], [PROJECT_URL])
        self.assertIn(PROJECT_URL, result["error"])
        self.assertLess(fixture["events"].index("checkpoint"), fixture["events"].index("send-click"))
        self.assertLess(stdout.index(runner.SUBMIT_MARKER), stdout.index(runner.MARKER))

    def test_phase_both_checkpoints_before_response_collection_failure(self):
        fixture, result, submitted, stdout = FakeBrowserFixture.run_raw(
            live_url=PROJECT_URL,
            phase="both",
            timeout_seconds=0,
            stop_visible=True,
        )
        self.assertEqual(fixture["sends"], 1)
        self.assertEqual(submitted["status"], "submitted")
        self.assertFalse(result["ok"])
        self.assertIn("no ChatGPT response", result["error"])
        self.assertTrue(result["ownedTabLeftOpen"])
        self.assertEqual(result["ownedTabTargetId"], "owned-1")
        self.assertTrue(fixture["open"])
        self.assertEqual(result["baselineTargetIds"], ["base-1"])
        self.assertEqual(result["finalTargetIds"], ["base-1", "owned-1"])
        self.assertTrue(submitted["ownedTabLeftOpen"])
        self.assertEqual(submitted["ownedTabTargetId"], "owned-1")
        self.assertNotIn("stop-click", fixture["events"])
        marker_positions = [
            index for index in range(len(stdout))
            if stdout.startswith(runner.SUBMIT_MARKER, index)
        ]
        self.assertGreaterEqual(len(marker_positions), 2)
        self.assertLess(marker_positions[-1], stdout.index(runner.MARKER))

    def test_partial_response_is_not_stopped_and_owned_tab_stays_open(self):
        fixture, result, submitted = FakeBrowserFixture.run(
            live_url=PROJECT_URL,
            phase="both",
            response=True,
            stop_visible=True,
            timeout_seconds=0.01,
        )
        self.assertTrue(result["ok"])
        self.assertTrue(result["partial"])
        self.assertEqual(result["response"], "fixture answer")
        self.assertTrue(result["ownedTabLeftOpen"])
        self.assertTrue(fixture["open"])
        self.assertNotIn("stop-click", fixture["events"])
        self.assertTrue(submitted["ownedTabLeftOpen"])

    def test_project_is_rechecked_immediately_before_attachment_and_send(self):
        before_attach, result, _submitted = FakeBrowserFixture.run(
            live_url=PROJECT_URL, navigate="before-attach"
        )
        self.assertFalse(before_attach["attached"])
        self.assertEqual(before_attach["sends"], 0)
        self.assertFalse(result["ok"])

        before_send, result, _submitted = FakeBrowserFixture.run(
            live_url=PROJECT_URL, navigate="before-send"
        )
        self.assertTrue(before_send["attached"])
        self.assertEqual(before_send["sends"], 0)
        self.assertFalse(result["ok"])

    def test_tab_baseline_churn_does_not_discard_owned_tab_cleanup(self):
        fixture, result, submitted = FakeBrowserFixture.run(
            live_url=PROJECT_URL, phase="both", response=True, baseline_churn=True
        )
        self.assertEqual(fixture["sends"], 1)
        self.assertEqual(result["baselineTargetIds"], ["base-1"])
        self.assertEqual(result["finalTargetIds"], ["base-2"])
        self.assertTrue(result["baselineRestored"])
        self.assertEqual(submitted["status"], "submitted")

    def test_user_tab_count_change_does_not_discard_owned_tab_cleanup(self):
        fixture, result, submitted = FakeBrowserFixture.run(
            live_url=PROJECT_URL, phase="both", response=True, baseline_growth=True
        )
        self.assertEqual(fixture["sends"], 1)
        self.assertEqual(result["baselineTargetIds"], ["base-1"])
        self.assertEqual(result["finalTargetIds"], ["base-2", "base-3"])
        self.assertNotEqual(len(result["baselineTargetIds"]), len(result["finalTargetIds"]))
        self.assertTrue(result["baselineRestored"])
        self.assertNotIn(result["ownedTargetId"], result["finalTargetIds"])
        self.assertEqual(submitted["status"], "submitted")

    def test_resume_reuses_left_open_owned_tab_and_closes_it_after_success(self):
        fixture, result, _submitted = FakeBrowserFixture.run(
            live_url=PROJECT_CONVERSATION_URL,
            phase="collect",
            response=True,
            resume_existing=True,
        )
        self.assertTrue(result["ok"])
        self.assertTrue(result["reusedOwnedTab"])
        self.assertEqual(result["ownedTargetId"], "owned-1")
        self.assertFalse(result["ownedTabLeftOpen"])
        self.assertTrue(result["baselineRestored"])
        self.assertEqual(result["finalTargetIds"], ["base-1"])
        self.assertFalse(fixture["open"])

    def test_runner_contains_no_conversation_delete_move_or_archive_action(self):
        js = runner.build_js(
            mode="quick", phase="submit", packet_b64="", prompt_b64="", packet_name="packet.md",
            timeout_seconds=1, start_url="https://chatgpt.com/g/g-p-id/project", follow_up=False,
            project_id="g-p-id", project_url="https://chatgpt.com/g/g-p-id/project", run_id="run",
            packet_hash="hash", prompt_hash="hash", account="u0",
        )
        for forbidden in ("deleteConversation", "archiveConversation", "moveConversation"):
            self.assertNotIn(forbidden, js)


class SubmissionGuardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.session = self.root / "session.json"
        self.packet = self.root / "packet.md"
        self.prompt = self.root / "prompt.md"
        self.packet.write_text("packet", encoding="utf-8")
        self.prompt.write_text("prompt", encoding="utf-8")

    def run_new_consult(self, extra=()):
        argv = [
            "--packet", str(self.packet),
            "--prompt-file", str(self.prompt),
            "--session-file", str(self.session),
            "--project-url", PROJECT_URL,
            "--json-output", str(self.root / "evidence.json"),
            "--stderr-output", str(self.root / "stderr.log"),
            "--response-output", str(self.root / "response.md"),
            *extra,
        ]
        with mock.patch.object(runner.shutil, "which", side_effect=lambda name: f"/usr/bin/{name}"), \
             mock.patch.object(runner.subprocess, "run", side_effect=no_browser):
            return runner.main(argv)

    def test_legacy_submitted_conversation_is_never_resent(self):
        self.session.write_text(
            json.dumps({"status": "submitted", "conversationUrl": LEGACY_CONVERSATION_URL}),
            encoding="utf-8",
        )
        self.assertEqual(self.run_new_consult(), runner.EXIT_ALREADY_SUBMITTED)

    def test_legacy_completed_record_without_identity_does_not_block_a_new_consult(self):
        self.session.write_text(
            json.dumps({"status": "complete", "conversationUrl": LEGACY_CONVERSATION_URL}),
            encoding="utf-8",
        )
        with self.assertRaises(ExplodingRun):
            self.run_new_consult()

    def test_same_completed_submission_is_not_sent_again(self):
        self.session.write_text(
            json.dumps(checkpoint(status="complete")),
            encoding="utf-8",
        )
        self.assertEqual(self.run_new_consult(), runner.EXIT_ALREADY_SUBMITTED)

    def test_explicit_new_overrides_the_guard(self):
        self.session.write_text(
            json.dumps({"status": "submitted", "conversationUrl": LEGACY_CONVERSATION_URL}),
            encoding="utf-8",
        )
        with self.assertRaises(ExplodingRun):
            self.run_new_consult(["--new"])

    def test_missing_project_configuration_stops_before_the_browser(self):
        with mock.patch.dict("os.environ", {}, clear=True), \
             mock.patch.object(runner, "read_config_value", return_value=None), \
             mock.patch.object(runner.shutil, "which", side_effect=lambda name: f"/usr/bin/{name}"), \
             mock.patch.object(runner.subprocess, "run", side_effect=no_browser):
            code = runner.main([
                "--packet", str(self.packet),
                "--prompt-file", str(self.prompt),
                "--session-file", str(self.session),
                "--json-output", str(self.root / "evidence.json"),
                "--stderr-output", str(self.root / "stderr.log"),
            ])
        self.assertEqual(code, runner.EXIT_INVALID)


class MainPostSendTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.packet = self.root / "packet.md"
        self.prompt = self.root / "prompt.md"
        self.session = self.root / "session.json"
        self.packet.write_text("packet", encoding="utf-8")
        self.prompt.write_text("prompt", encoding="utf-8")

    def run_main(self, lines, *, extra=(), explicit_session=True):
        argv = [
            "--packet", str(self.packet),
            "--prompt-file", str(self.prompt),
            "--project-url", PROJECT_URL,
            "--json-output", str(self.root / "evidence.json"),
            "--stderr-output", str(self.root / "stderr.log"),
            "--response-output", str(self.root / "response.md"),
        ]
        if explicit_session:
            argv.extend(["--session-file", str(self.session)])
        argv.extend(extra)

        class Process:
            stdout = list(lines)
            stderr = []

            def wait(self):
                return 1

        with mock.patch.object(runner.shutil, "which", side_effect=lambda name: f"/usr/bin/{name}"), \
             mock.patch.object(runner, "ensure_aside_running", return_value=True), \
             mock.patch.object(runner.subprocess, "Popen", return_value=Process()):
            return runner.main(argv)

    def test_main_turns_clicked_without_url_into_pending_exit_four(self):
        result = {
            "ok": False,
            "error": "send was clicked but no accepted conversation URL appeared",
            "baselineRestored": True,
        }
        code = self.run_main([runner.MARKER + json.dumps(result) + "\n"])
        saved = json.loads(self.session.read_text(encoding="utf-8"))
        self.assertEqual(code, runner.EXIT_ALREADY_SUBMITTED)
        self.assertEqual(saved["status"], "sending")
        self.assertIsNone(saved["conversationUrl"])

    def test_main_keeps_checkpoint_when_result_marker_is_malformed(self):
        record = checkpoint()
        code = self.run_main([
            runner.SUBMIT_MARKER + json.dumps(record) + "\n",
            runner.MARKER + "{malformed\n",
        ])
        self.assertEqual(code, runner.EXIT_ALREADY_SUBMITTED)
        self.assertEqual(json.loads(self.session.read_text(encoding="utf-8"))["conversationUrl"], record["conversationUrl"])

    def test_main_records_and_reports_left_open_tab_after_collection_failure(self):
        record = checkpoint()
        result = {
            "ok": False,
            "submitted": True,
            "conversationUrl": record["conversationUrl"],
            "error": "no ChatGPT response was captured before timeout",
            "baselineRestored": False,
            "ownedTabLeftOpen": True,
            "ownedTabTargetId": "owned-1",
            "ownedTargetId": "owned-1",
            "ownedTabUrl": record["conversationUrl"],
        }
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = self.run_main([
                runner.SUBMIT_MARKER + json.dumps(record) + "\n",
                runner.MARKER + json.dumps(result) + "\n",
            ])
        saved = json.loads(self.session.read_text(encoding="utf-8"))
        self.assertEqual(code, runner.EXIT_ALREADY_SUBMITTED)
        self.assertTrue(saved["ownedTabLeftOpen"])
        self.assertEqual(saved["ownedTabTargetId"], "owned-1")
        self.assertIn("owned tab left open at", stderr.getvalue())
        self.assertIn("collect later with --resume", stderr.getvalue())

    def test_main_allows_send_only_with_intentionally_open_owned_tab(self):
        record = checkpoint()
        result = {
            "ok": True,
            "submitted": True,
            "conversationUrl": record["conversationUrl"],
            "baselineRestored": False,
            "ownedTabLeftOpen": True,
            "ownedTabTargetId": "owned-1",
            "ownedTargetId": "owned-1",
            "ownedTabUrl": record["conversationUrl"],
        }
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = self.run_main(
                [
                    runner.SUBMIT_MARKER + json.dumps(record) + "\n",
                    runner.MARKER + json.dumps(result) + "\n",
                ],
                extra=("--send-only",),
            )
        self.assertEqual(code, runner.EXIT_OK)
        self.assertTrue(json.loads(self.session.read_text(encoding="utf-8"))["ownedTabLeftOpen"])
        self.assertIn("owned tab left open at", stdout.getvalue())

    def test_main_marks_owned_tab_closed_after_successful_collection(self):
        record = checkpoint()
        result = {
            "ok": True,
            "submitted": True,
            "conversationUrl": record["conversationUrl"],
            "baselineRestored": True,
            "ownedTabLeftOpen": False,
            "ownedTabTargetId": None,
            "response": "answer",
            "completedAt": "2026-08-21T01:00:00Z",
        }
        code = self.run_main([
            runner.SUBMIT_MARKER + json.dumps(record) + "\n",
            runner.MARKER + json.dumps(result) + "\n",
        ])
        saved = json.loads(self.session.read_text(encoding="utf-8"))
        self.assertEqual(code, runner.EXIT_OK)
        self.assertFalse(saved["ownedTabLeftOpen"])
        self.assertIsNone(saved["ownedTabTargetId"])

    def test_follow_up_main_preserves_original_identity_and_guard(self):
        original = checkpoint(status="complete", runId="original", submissionId="original")
        self.session.write_text(json.dumps(original), encoding="utf-8")
        follow_up = checkpoint(
            status="submitted",
            runId="follow-up",
            submissionId="follow-up",
            packetHash=runner.hash_text(""),
            promptHash=runner.hash_text("narrow question"),
        )
        result = {
            "ok": True,
            "submitted": True,
            "conversationUrl": original["conversationUrl"],
            "baselineRestored": True,
            "response": "answer",
            "completedAt": "2026-08-21T01:00:00Z",
        }
        code = self.run_main(
            [
                runner.SUBMIT_MARKER + json.dumps(follow_up) + "\n",
                runner.MARKER + json.dumps(result) + "\n",
            ],
            extra=("--follow-up", "narrow question"),
        )
        saved = json.loads(self.session.read_text(encoding="utf-8"))
        self.assertEqual(code, runner.EXIT_OK)
        self.assertEqual(saved["runId"], "original")
        self.assertEqual(saved["packetHash"], runner.hash_text("packet"))
        self.assertEqual(saved["promptHash"], runner.hash_text("prompt"))
        self.assertEqual(saved["followUps"][-1]["packetHash"], runner.hash_text(""))

        with mock.patch.object(runner.shutil, "which", side_effect=lambda name: f"/usr/bin/{name}"), \
             mock.patch.object(runner, "ensure_aside_running", side_effect=ExplodingRun):
            rerun = runner.main([
                "--packet", str(self.packet),
                "--prompt-file", str(self.prompt),
                "--session-file", str(self.session),
                "--project-url", PROJECT_URL,
            ])
        self.assertEqual(rerun, runner.EXIT_ALREADY_SUBMITTED)

    def test_default_session_path_survives_working_directory_change(self):
        global_sessions = self.root / "global-sessions"
        cwd_a = self.root / "a"
        cwd_b = self.root / "b"
        cwd_a.mkdir()
        cwd_b.mkdir()
        result = {
            "ok": False,
            "error": "send was clicked but no accepted conversation URL appeared",
            "baselineRestored": True,
        }
        original_cwd = Path.cwd()
        try:
            with mock.patch.object(runner, "DEFAULT_SESSION_DIR", global_sessions):
                runner.os.chdir(cwd_a)
                first = self.run_main(
                    [runner.MARKER + json.dumps(result) + "\n"],
                    explicit_session=False,
                )
                self.assertEqual(first, runner.EXIT_ALREADY_SUBMITTED)
                self.assertTrue(runner.default_session_path("u0").exists())

                runner.os.chdir(cwd_b)
                with mock.patch.object(runner.shutil, "which", side_effect=lambda name: f"/usr/bin/{name}"), \
                     mock.patch.object(runner, "ensure_aside_running", side_effect=ExplodingRun):
                    second = runner.main([
                        "--packet", str(self.packet),
                        "--prompt-file", str(self.prompt),
                        "--project-url", PROJECT_URL,
                    ])
                self.assertEqual(second, runner.EXIT_ALREADY_SUBMITTED)
        finally:
            runner.os.chdir(original_cwd)

    def test_new_checkpoint_archives_previous_conversation(self):
        old = checkpoint(status="submitted", runId="old", submissionId="old")
        new = pending_checkpoint(runId="new", submissionId="new")
        merged = runner.merge_checkpoint(old, new, follow_up=False)
        self.assertEqual(merged["runId"], "new")
        self.assertEqual(merged["previous"][-1]["conversationUrl"], old["conversationUrl"])

    def test_follow_up_rejects_a_different_conversation_url(self):
        self.session.write_text(json.dumps(checkpoint()), encoding="utf-8")
        code = self.run_main([], extra=(
            "--follow-up", "more",
            "--session", f"https://chatgpt.com/g/{PROJECT_SLUG}/c/different",
        ))
        self.assertEqual(code, runner.EXIT_INVALID)


class AsideLaunchTest(unittest.TestCase):
    def test_a_running_and_responsive_aside_is_not_relaunched(self):
        with mock.patch.object(runner, "aside_is_running", return_value=True), \
             mock.patch.object(runner, "aside_responds", return_value=True), \
             mock.patch.object(runner.subprocess, "run", side_effect=no_browser):
            self.assertTrue(runner.ensure_aside_running("/usr/bin/aside", "/usr/bin/script", "u0"))

    def test_a_closed_aside_is_opened_and_awaited(self):
        opened = []
        with mock.patch.object(runner, "aside_is_running", return_value=False), \
             mock.patch.object(runner, "aside_responds", side_effect=[False, True]), \
             mock.patch.object(runner.subprocess, "run", side_effect=lambda cmd, **kw: opened.append(cmd)):
            self.assertTrue(runner.ensure_aside_running("/usr/bin/aside", "/usr/bin/script", "u0"))
        self.assertEqual(opened, [["open", "-gj", "-a", "Aside"]])

    def test_an_unreachable_aside_gives_up_instead_of_looping(self):
        with mock.patch.object(runner, "aside_is_running", return_value=False), \
             mock.patch.object(runner, "aside_responds", return_value=False), \
             mock.patch.object(runner.subprocess, "run", return_value=None), \
             mock.patch.object(runner, "ASIDE_LAUNCH_TIMEOUT", 0):
            self.assertFalse(runner.ensure_aside_running("/usr/bin/aside", "/usr/bin/script", "u0"))


class CheckpointRecoveryTest(unittest.TestCase):
    def test_submission_marker_survives_a_lost_result_marker(self):
        record = {"status": "submitted", "conversationUrl": LEGACY_CONVERSATION_URL}
        stdout = f"noise\n{runner.SUBMIT_MARKER}{json.dumps(record)}\x1b[0m\nmore noise\n"
        self.assertEqual(runner.extract_marker(stdout, runner.SUBMIT_MARKER), record)
        self.assertIsNone(runner.extract_marker(stdout, runner.MARKER))

    def test_atomic_write_leaves_no_temporary_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "nested" / "session.json"
            runner.write_json(target, {"status": "submitted"})
            self.assertEqual(json.loads(target.read_text(encoding="utf-8")), {"status": "submitted"})
            self.assertEqual([p.name for p in target.parent.iterdir()], ["session.json"])

    def test_checkpoint_is_durable_before_the_repl_waits_or_disconnects(self):
        with tempfile.TemporaryDirectory() as tmp:
            session = Path(tmp) / "session.json"
            record = checkpoint()

            class Lines:
                def __iter__(self):
                    yield runner.SUBMIT_MARKER + json.dumps(record) + "\n"

            class FakeProcess:
                stdout = Lines()
                stderr = []

                def wait(self):
                    self.saved_before_wait = json.loads(session.read_text(encoding="utf-8"))
                    return 1

            process = FakeProcess()
            with mock.patch.object(runner.subprocess, "Popen", return_value=process):
                code, _stdout, _stderr, submitted = runner.run_aside_repl(["fake"], session)
            self.assertEqual(code, 1)
            self.assertEqual(process.saved_before_wait, record)
            self.assertEqual(submitted, record)

    def test_pending_checkpoint_is_durable_before_the_repl_waits(self):
        with tempfile.TemporaryDirectory() as tmp:
            session = Path(tmp) / "session.json"
            record = pending_checkpoint()

            class Process:
                stdout = [runner.SUBMIT_MARKER + json.dumps(record) + "\n"]
                stderr = []

                def wait(self):
                    self.saved_before_wait = json.loads(session.read_text(encoding="utf-8"))
                    return 1

            process = Process()
            with mock.patch.object(runner.subprocess, "Popen", return_value=process):
                _code, _stdout, _stderr, submitted = runner.run_aside_repl(["fake"], session)
            self.assertEqual(process.saved_before_wait["status"], "sending")
            self.assertIsNone(process.saved_before_wait["conversationUrl"])
            self.assertEqual(submitted, record)

    def test_malformed_result_marker_does_not_erase_an_accepted_submission(self):
        record = checkpoint()
        stdout = (
            runner.SUBMIT_MARKER + json.dumps(record) + "\n"
            + runner.MARKER + "{malformed\n"
        )
        self.assertEqual(runner.extract_marker(stdout, runner.SUBMIT_MARKER), record)
        self.assertIsNone(runner.extract_marker(stdout, runner.MARKER))

    def test_response_collection_failure_keeps_the_submission_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            session = Path(tmp) / "session.json"
            record = checkpoint()

            class FakeProcess:
                stdout = [
                    runner.SUBMIT_MARKER + json.dumps(record) + "\n",
                    runner.MARKER + json.dumps({
                        "ok": False,
                        "submitted": True,
                        "conversationUrl": record["conversationUrl"],
                        "error": "response collection failed",
                    }) + "\n",
                ]
                stderr = []

                def wait(self):
                    return 1

            with mock.patch.object(runner.subprocess, "Popen", return_value=FakeProcess()):
                _code, stdout, _stderr, submitted = runner.run_aside_repl(["fake"], session)
            self.assertEqual(submitted, record)
            self.assertEqual(json.loads(session.read_text(encoding="utf-8")), record)
            self.assertFalse(runner.extract_marker(stdout, runner.MARKER)["ok"])

    def test_checkpoint_has_every_required_identity_field(self):
        self.assertTrue(runner.is_valid_checkpoint(checkpoint()))
        for field in (
            "runId", "submissionId", "packetHash", "promptHash", "projectUrl", "projectId",
            "conversationUrl", "submittedAt", "model", "effort", "account",
        ):
            broken = checkpoint()
            broken.pop(field)
            self.assertFalse(runner.is_valid_checkpoint(broken), field)


class SessionLockTest(unittest.TestCase):
    """The lock closes the read-decide-write window that os.replace cannot."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.session = self.root / "session.json"
        self.packet = self.root / "packet.md"
        self.prompt = self.root / "prompt.txt"
        self.packet.write_text("packet", encoding="utf-8")
        self.prompt.write_text("prompt", encoding="utf-8")
        self.addCleanup(self.release_process_lock)

    def release_process_lock(self):
        if runner._session_lock_handle is not None:
            runner._session_lock_handle.close()
            runner._session_lock_handle = None

    def run_new_consult(self):
        argv = [
            "--packet", str(self.packet),
            "--prompt-file", str(self.prompt),
            "--session-file", str(self.session),
            "--project-url", PROJECT_URL,
            "--json-output", str(self.root / "evidence.json"),
            "--stderr-output", str(self.root / "stderr.log"),
            "--response-output", str(self.root / "response.md"),
        ]
        with mock.patch.object(runner.shutil, "which", side_effect=lambda name: f"/usr/bin/{name}"), \
             mock.patch.object(runner.subprocess, "run", side_effect=no_browser):
            return runner.main(argv)

    def test_a_second_run_on_the_same_session_never_reaches_the_browser(self):
        holder = (self.root / "session.json.lock").open("w")
        self.addCleanup(holder.close)
        fcntl.flock(holder.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        # no_browser raises, so anything past the lock would fail loudly.
        self.assertEqual(self.run_new_consult(), runner.EXIT_LOCKED)

    def test_releasing_the_lock_lets_the_next_run_proceed(self):
        holder = (self.root / "session.json.lock").open("w")
        fcntl.flock(holder.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        holder.close()
        with self.assertRaises(ExplodingRun):
            self.run_new_consult()

    def test_a_killed_holder_leaves_no_stale_lock(self):
        lock_path = self.root / "session.json.lock"
        child = subprocess.Popen(
            [
                sys.executable, "-c",
                "import fcntl,sys,time\n"
                "f=open(sys.argv[1],'w')\n"
                "fcntl.flock(f.fileno(), fcntl.LOCK_EX)\n"
                "print('locked', flush=True)\n"
                "time.sleep(60)\n",
                str(lock_path),
            ],
            stdout=subprocess.PIPE,
            text=True,
        )
        self.addCleanup(child.wait)
        self.addCleanup(child.kill)
        self.assertEqual(child.stdout.readline().strip(), "locked")
        self.assertFalse(runner.acquire_session_lock(self.session))
        child.kill()
        child.wait(timeout=10)
        self.assertTrue(runner.acquire_session_lock(self.session))


if __name__ == "__main__":
    unittest.main()
