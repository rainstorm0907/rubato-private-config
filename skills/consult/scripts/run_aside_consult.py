#!/usr/bin/env python3
"""Run a ChatGPT web consult through the user's logged-in Aside browser."""

from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import threading
import time
from typing import Any
from urllib.parse import urlparse
import uuid


MARKER = "__ASIDE_CONSULT_RESULT__"
SUBMIT_MARKER = "__ASIDE_CONSULT_SUBMITTED__"
DEFAULT_SESSION_DIR = Path.home() / ".config" / "consult" / "sessions"
DEFAULT_JSON_OUTPUT = ".consult/aside-consult-response.json"
DEFAULT_STDERR_OUTPUT = ".consult/aside-consult-stderr.log"
MAX_PACKET_BYTES = 500_000
CONFIG_PATHS = (
    Path.home() / ".config" / "consult" / "consult.env",
    Path.home() / ".codex" / "consult.env",
)

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_INVALID = 2
EXIT_PARTIAL = 3
EXIT_ALREADY_SUBMITTED = 4
EXIT_LOCKED = 5

ASIDE_APP = "Aside"
ASIDE_LAUNCH_TIMEOUT = 90


def aside_is_running() -> bool:
    return subprocess.run(["pgrep", "-x", ASIDE_APP], capture_output=True).returncode == 0


def aside_responds(aside: str, script: str, account: str) -> bool:
    probe = subprocess.run(
        [script, "-q", "/dev/null", aside, "repl", "--account", account, "console.log('__ASIDE_PROBE__')"],
        capture_output=True,
        text=True,
        errors="replace",
        check=False,
        timeout=60,
    )
    return "__ASIDE_PROBE__" in probe.stdout


def ensure_aside_running(aside: str, script: str, account: str) -> bool:
    """Start Aside Browser when it is closed, so a consult never depends on the user opening it."""
    if aside_is_running() and aside_responds(aside, script, account):
        return True
    subprocess.run(["open", "-gj", "-a", ASIDE_APP], check=False)
    deadline = time.monotonic() + ASIDE_LAUNCH_TIMEOUT
    while time.monotonic() < deadline:
        if aside_responds(aside, script, account):
            return True
    return False


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, value: str) -> None:
    """Publish a file atomically so a crashed run never leaves a half-written record."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        handle.write(value)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)
    try:
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except OSError:
        # Some filesystems do not support syncing directory descriptors. The
        # atomic replace above is still the required publication boundary.
        pass


def write_json(path: Path, payload: Any) -> None:
    write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def encode_text(value: str) -> str:
    return base64.b64encode(value.encode("utf-8")).decode("ascii")


def hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def is_conversation_url(value: Any) -> bool:
    return bool(
        isinstance(value, str)
        and re.fullmatch(
            r"https://chatgpt\.com/(?:c|g/[A-Za-z0-9_-]+/c)/[A-Za-z0-9_-]+/?",
            value,
        )
    )


def is_valid_checkpoint(record: dict[str, Any] | None) -> bool:
    required = {
        "runId",
        "submissionId",
        "packetHash",
        "promptHash",
        "projectUrl",
        "projectId",
        "conversationUrl",
        "submittedAt",
        "model",
        "effort",
        "account",
    }
    return bool(
        record
        and required.issubset(record)
        and all(isinstance(record.get(field), str) and record.get(field) for field in required)
        and is_conversation_url(record.get("conversationUrl"))
    )


def is_valid_pending_checkpoint(record: dict[str, Any] | None) -> bool:
    required = {
        "runId",
        "submissionId",
        "packetHash",
        "promptHash",
        "projectUrl",
        "projectId",
        "pendingAt",
        "model",
        "effort",
        "account",
    }
    return bool(
        record
        and record.get("status") == "sending"
        and record.get("conversationUrl") is None
        and required.issubset(record)
        and all(isinstance(record.get(field), str) and record.get(field) for field in required)
    )


def default_session_path(account: str) -> Path:
    safe_account = re.sub(r"[^A-Za-z0-9_.-]", "_", account)
    return DEFAULT_SESSION_DIR / f"aside-consult-session-{safe_account}.json"


_session_lock_handle: Any = None


def acquire_session_lock(session_path: Path) -> bool:
    """Serialise runs that share a session file.

    os.replace makes a single write atomic, but the read-decide-write span that
    guards against duplicate submissions is not. Without this, two runs can both
    read "no checkpoint" and both submit. The lock is held for the life of the
    process; flock is released by the kernel even on SIGKILL, so a crashed run
    never leaves a lock behind for someone to clean up.
    """
    global _session_lock_handle
    if _session_lock_handle is not None:
        # One process runs one consult at a time, so an earlier lock in this
        # process is this same run and must not block it.
        _session_lock_handle.close()
        _session_lock_handle = None
    lock_path = session_path.with_name(session_path.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    handle = lock_path.open("w")
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        handle.close()
        return False
    _session_lock_handle = handle
    return True


def session_records(record: dict[str, Any]) -> list[dict[str, Any]]:
    records = [record] if record else []
    previous = record.get("previous") if isinstance(record, dict) else None
    if isinstance(previous, list):
        records.extend(item for item in previous if isinstance(item, dict))
    return records


def merge_checkpoint(
    existing: dict[str, Any], incoming: dict[str, Any], *, follow_up: bool
) -> dict[str, Any]:
    """Preserve original submission identity and archived conversations."""
    if follow_up and existing:
        merged = dict(existing)
        follow_ups = list(merged.get("followUps") or [])
        if follow_ups and follow_ups[-1].get("runId") == incoming.get("runId"):
            follow_ups[-1] = {**follow_ups[-1], **incoming}
        else:
            follow_ups.append(dict(incoming))
        merged["followUps"] = follow_ups
        merged["updatedAt"] = incoming.get("submittedAt") or incoming.get("pendingAt")
        return merged

    if existing and existing.get("runId") == incoming.get("runId"):
        return {**existing, **incoming}

    previous = list(existing.get("previous") or []) if existing else []
    if existing:
        previous.append({key: value for key, value in existing.items() if key != "previous"})
    merged = dict(incoming)
    if previous:
        merged["previous"] = previous
    return merged


def read_config_value(key: str) -> str | None:
    for config_path in CONFIG_PATHS:
        if not config_path.exists():
            continue
        for line in read_text(config_path).splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            name, value = stripped.split("=", 1)
            if name.strip() != key:
                continue
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
                value = value[1:-1]
            if value:
                return value
    return None


def load_session(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        record = json.loads(read_text(path))
    except json.JSONDecodeError:
        return {}
    return record if isinstance(record, dict) else {}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Consult through Aside and ChatGPT web.")
    parser.add_argument("--mode", choices=("quick", "deep"), default="quick")
    parser.add_argument("--packet", default=".consult/consult-packet.md")
    parser.add_argument("--prompt-file", default=".consult/chatgpt-upload-instructions.md")
    parser.add_argument("--response-output", default=".consult/consult-response.md")
    parser.add_argument("--json-output", default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--stderr-output", default=DEFAULT_STDERR_OUTPUT)
    parser.add_argument(
        "--session-file",
        default=None,
        help="Checkpoint path. Defaults to a stable per-account path outside the working directory.",
    )
    parser.add_argument(
        "--session",
        default=None,
        help="Conversation URL for resume; a follow-up may only repeat the saved URL.",
    )
    parser.add_argument("--follow-up", default=None)
    parser.add_argument("--project-url", default=None, help="ChatGPT project URL that owns every new consult conversation.")
    parser.add_argument("--send-only", action="store_true", help="Submit and checkpoint, then exit without waiting for the answer.")
    parser.add_argument("--resume", action="store_true", help="Collect the answer of an already submitted conversation.")
    parser.add_argument("--dry-run", action="store_true", help="Verify account, project, and model state, then stop without sending.")
    parser.add_argument("--new", action="store_true", help="Start a new conversation even though a submitted one is on record.")
    parser.add_argument("--timeout", type=int, default=None)
    parser.add_argument("--account", default="u0")
    return parser.parse_args(argv)


def build_js(
    *,
    mode: str,
    phase: str,
    packet_b64: str,
    prompt_b64: str,
    packet_name: str,
    timeout_seconds: int,
    start_url: str,
    follow_up: bool,
    project_id: str | None,
    project_url: str | None,
    run_id: str,
    packet_hash: str,
    prompt_hash: str,
    account: str,
    resume_target_id: str | None = None,
) -> str:
    config = {
        "mode": mode,
        "phase": phase,
        "packetB64": packet_b64,
        "promptB64": prompt_b64,
        "packetName": packet_name,
        "timeoutMs": timeout_seconds * 1000,
        "startUrl": start_url,
        "followUp": follow_up,
        "projectId": project_id,
        "projectUrl": project_url,
        "runId": run_id,
        "packetHash": packet_hash,
        "promptHash": prompt_hash,
        "account": account,
        "resumeTargetId": resume_target_id,
    }
    config_json = json.dumps(config, ensure_ascii=False)
    # Keep all browser state and cleanup in one Aside REPL lifetime. Snapshot refs
    # are parsed only from the fresh snapshot that produced them.
    return f"""
const cfg = {config_json};
const result = {{ok:false, mode:cfg.mode, phase:cfg.phase, requestedModel:'GPT-5.6 Sol', requestedEffort:cfg.mode === 'deep' ? 'Pro' : '매우 높음', projectId:cfg.projectId, startedAt:new Date().toISOString()}};
const baselineTabs = await listBrowserTabs();
const baselineIds = new Set(baselineTabs.map(t => t.targetId));
const STOP_SELECTOR = 'button[data-testid="stop-button"], button[aria-label*="중지"], button[aria-label*="Stop"]';
result.conversationUrlCandidates = [];
let consultPage = null;
let conversationUrlsBeforeSend = [];
let userMessagesBeforeSend = 0;
let accountVerified = false;
function refFromLine(tree, predicate) {{
  const lines = tree.split('\\n').filter(predicate);
  if (!lines.length) throw new Error('required browser control not found');
  const match = lines[lines.length - 1].match(/\\[ref=([^\\]]+)\\]/);
  if (!match) throw new Error('browser control has no fresh ref: ' + lines[lines.length - 1]);
  return match[1];
}}
function lineFor(tree, predicate) {{
  const lines = tree.split('\\n').filter(predicate);
  return lines.length ? lines[lines.length - 1] : '';
}}
async function currentUrl() {{ return await consultPage.evaluate(() => location.href); }}
async function snap(interactive=false) {{ return await snapshot(consultPage, interactive ? {{interactive:true}} : undefined); }}
async function clickFresh(tree, predicate) {{
  try {{
    await consultPage.locator(refFromLine(tree, predicate)).click();
  }} catch (error) {{
    if (!String(error).includes('detached')) throw error;
    const refreshed = await snap(true);
    await consultPage.locator(refFromLine(refreshed.tree, predicate)).click();
  }}
}}
async function conversationUrls() {{
  const links = consultPage.locator('a[href*="/c/"]');
  const urls = [];
  for (let i=0; i<await links.count(); i++) {{
    const href = await links.nth(i).getAttribute('href');
    if (href) {{
      const absolute = href.startsWith('http://') || href.startsWith('https://')
        ? href
        : 'https://chatgpt.com' + (href.startsWith('/') ? href : '/' + href);
      if (!urls.includes(absolute)) urls.push(absolute);
    }}
  }}
  return urls;
}}
function isConversationUrl(value) {{
  const prefix = 'https://chatgpt.com';
  if (typeof value !== 'string' || !value.startsWith(prefix + '/')) return false;
  const pathname = value.slice(prefix.length).split(/[?#]/, 1)[0];
  const parts = pathname.split('/').filter(Boolean);
  const validPart = (part) => /^[A-Za-z0-9_-]+$/.test(part || '');
  return (
    parts.length === 2 && parts[0] === 'c' && validPart(parts[1])
  ) || (
    parts.length === 4 && parts[0] === 'g' && validPart(parts[1]) && parts[2] === 'c' && validPart(parts[3])
  );
}}
function rememberConversationUrlCandidate(value) {{
  if (value && !result.conversationUrlCandidates.includes(value) && result.conversationUrlCandidates.length < 200) {{
    result.conversationUrlCandidates.push(value);
  }}
}}
async function discoverConversationUrl() {{
  if (isConversationUrl(cfg.startUrl)) return cfg.startUrl;
  for (let attempt=0; attempt<40; attempt++) {{
    const live = await currentUrl();
    rememberConversationUrlCandidate(live);
    if (isConversationUrl(live)) return live;
    const after = await conversationUrls();
    after.forEach(rememberConversationUrlCandidate);
    const created = after.find(url => !conversationUrlsBeforeSend.includes(url) && isConversationUrl(url));
    if (created) return created;
    await sleep(250);
  }}
  throw new Error(
    'send was clicked but no accepted conversation URL appeared; candidates=' +
    JSON.stringify(result.conversationUrlCandidates)
  );
}}
async function verifyAccountOnce() {{
  if (accountVerified) return;
  async function accountSnapshot() {{
    const base = await snap(false);
    if (base.tree.includes('개인 계정')) return base;
    const profileLine = lineFor(
      base.tree,
      line => line.includes('button "프로필 메뉴 열기"') || line.includes('button "Open profile menu"')
    );
    if (!profileLine) return base;
    const profileRef = refFromLine(base.tree, line => line === profileLine);
    await consultPage.locator(profileRef).click();
    const menu = await snap(false);
    await consultPage.keyboard.press('Escape');
    return {{tree: base.tree + '\\n' + menu.tree, diff: menu.diff}};
  }}
  const isPersonalPaid = (tree) =>
    tree.includes('개인 계정') &&
    !tree.includes('Free 님') &&
    !tree.includes('button "로그인"');
  let base = await accountSnapshot();
  for (let attempt=0; attempt<20 && !isPersonalPaid(base.tree); attempt++) {{
    if (base.tree.includes('Free 님') || base.tree.includes('button "로그인"')) throw new Error('Aside ChatGPT login is missing or not Pro');
    await sleep(500);
    base = await accountSnapshot();
  }}
  if (!isPersonalPaid(base.tree)) throw new Error('Aside ChatGPT is not signed into the personal paid account');
  // The Chat/Work radio pair only renders on the chat root. Inside a project the
  // profile line carrying '개인 계정' is the personal-surface evidence; a Work
  // workspace names itself there instead.
  const workLine = lineFor(base.tree, line => line.includes('radio "Work"'));
  if (workLine.includes('[checked]')) throw new Error('ChatGPT Work surface detected; switch to personal Chat');
  const chatLine = lineFor(base.tree, line => line.includes('radio "Chat"'));
  if (chatLine && !chatLine.includes('[checked]')) throw new Error('personal Chat surface was not verified');
  result.accountEvidence = lineFor(base.tree, line => line.includes('개인 계정')).trim();
  accountVerified = true;
}}
// A new conversation must be born inside the configured project. Check the unique
// project id in the live URL, never the display name, and check it before any
// file is attached so a wrong surface costs nothing.
async function verifyProject() {{
  if (!cfg.projectId) throw new Error('no project id was configured for a new consult conversation');
  let current = await currentUrl();
  const isConfiguredNewChat = (value) => {{
    const prefix = 'https://chatgpt.com';
    if (typeof value !== 'string' || !value.startsWith(prefix + '/')) return false;
    const pathname = value.slice(prefix.length).split(/[?#]/, 1)[0];
    const normalizedPath = pathname.endsWith('/') ? pathname.slice(0, -1) : pathname;
    return normalizedPath === '/g/' + cfg.projectId + '/project';
  }};
  for (let attempt=0; attempt<20 && !isConfiguredNewChat(current); attempt++) {{
    await sleep(500);
    current = await currentUrl();
  }}
  if (!isConfiguredNewChat(current)) throw new Error('consult did not land in the configured project new-chat screen: ' + current);
  result.projectUrlAtSubmit = current;
}}
async function verifyConversation() {{
  const current = await currentUrl();
  if (current !== cfg.startUrl) throw new Error('follow-up conversation changed before send: ' + current);
}}
async function openAdvancedModeMenu() {{
  await verifyAccountOnce();
  const base = await snap(false);
  const perfLabels = ['즉시','중간','높음','매우 높음','Pro','Think','추론 수준'];
  const perfRef = refFromLine(base.tree, line => line.includes('button "') && perfLabels.some(label => line.includes('button "' + label + '"')));
  await consultPage.locator(perfRef).click();
  let menu = await snap(true);
  if (menu.tree.includes('고급 옵션 표시')) {{
    await clickFresh(menu.tree, line => line.includes('menuitem "고급 옵션 표시"'));
    menu = await snap(true);
  }}
  const legacy = menu.tree.includes('모델 GPT-5.6 Sol');
  const modern = menu.tree.includes('menuitem "모델 선택"') && menu.tree.includes('menuitem "성능"');
  if (!legacy && !modern) throw new Error('GPT-5.6 Sol model state was not exposed');
  return menu;
}}
async function configureMode() {{
  let menu = await openAdvancedModeMenu();
  const target = cfg.mode === 'deep' ? 'Pro' : '매우 높음';
  if (menu.tree.includes('menuitem "모델 선택"') && menu.tree.includes('menuitem "성능"')) {{
    await clickFresh(menu.tree, line => line.includes('menuitem "모델 선택"'));
    const models = await snap(true);
    const modelLine = lineFor(models.tree, line => line.includes('menuitemradio "GPT-5.6 Sol"'));
    if (!modelLine) throw new Error('GPT-5.6 Sol model choice was not exposed');
    if (!modelLine.includes('[checked]')) {{
      await consultPage.locator(refFromLine(models.tree, line => line.includes('menuitemradio "GPT-5.6 Sol"'))).click();
    }}
    await consultPage.keyboard.press('Escape');
    await consultPage.keyboard.press('Escape');
    menu = await openAdvancedModeMenu();
    const performanceLine = lineFor(menu.tree, line => line.includes('menuitem "성능"'));
    const statusLine = lineFor(menu.tree, line => line.includes('5개 중') && line.includes('번째'));
    const currentMatch = statusLine.match(/5개 중 (\\d+)번째/);
    if (!performanceLine || !currentMatch) throw new Error('reasoning performance state was not exposed');
    const currentIndex = Number(currentMatch[1]);
    const targetIndex = cfg.mode === 'deep' ? 5 : 4;
    await consultPage.locator(refFromLine(menu.tree, line => line.includes('menuitem "성능"'))).focus();
    const key = targetIndex > currentIndex ? 'ArrowRight' : 'ArrowLeft';
    for (let step=0; step<Math.abs(targetIndex-currentIndex); step++) await consultPage.keyboard.press(key);
    const verified = await snap(false);
    const effortLine = lineFor(verified.tree, line => line.includes(target + ', 5개 중 ' + targetIndex + '번째'));
    if (!effortLine) throw new Error('requested reasoning level was not verified: ' + target);
    result.verifiedModel = 'GPT-5.6 Sol';
    result.verifiedEffort = target;
    result.modelEvidence = {{modelLine, effortLine}};
    await consultPage.keyboard.press('Escape');
    await consultPage.keyboard.press('Escape');
    return;
  }}
  await clickFresh(menu.tree, line => line.includes('menuitem "추론 수준'));
  let levels = await snap(true);
  const targetLine = lineFor(levels.tree, line => line.includes('menuitemradio "' + target + '"'));
  if (!targetLine) throw new Error('requested reasoning level not available: ' + target);
  if (!targetLine.includes('[checked]')) await consultPage.locator(refFromLine(levels.tree, line => line.includes('menuitemradio "' + target + '"'))).click();
  else await consultPage.keyboard.press('Escape');
  await consultPage.keyboard.press('Escape');
  menu = await openAdvancedModeMenu();
  const modelLine = lineFor(menu.tree, line => line.includes('menuitem "모델 GPT-5.6 Sol"'));
  const effortLine = lineFor(menu.tree, line => line.includes('menuitem "추론 수준 ' + target + '"'));
  if (!modelLine || !effortLine) throw new Error('model or reasoning level verification failed');
  result.verifiedModel = 'GPT-5.6 Sol';
  result.verifiedEffort = target;
  result.modelEvidence = {{modelLine, effortLine}};
  await consultPage.keyboard.press('Escape');
  await consultPage.keyboard.press('Escape');
}}
// The submission checkpoint is published the moment the conversation exists, before
// any waiting begins. Everything after this point is recoverable; a lost checkpoint
// is what turns one consult into a pile of duplicate chats.
async function checkpointSubmission() {{
  result.submittedAt = new Date().toISOString();
  const record = {{
    status: 'submitted',
    runId: cfg.runId,
    submissionId: cfg.runId,
    packetHash: cfg.packetHash,
    promptHash: cfg.promptHash,
    projectUrl: cfg.projectUrl,
    mode: cfg.mode,
    projectId: cfg.projectId,
    projectUrlAtSubmit: result.projectUrlAtSubmit || null,
    conversationUrl: result.conversationUrl,
    model: result.verifiedModel,
    effort: result.verifiedEffort,
    account: result.accountEvidence || cfg.account,
    asideAccount: cfg.account,
    submittedAt: result.submittedAt,
    ownedTabLeftOpen: true,
    ownedTabTargetId: result.ownedTargetId,
  }};
  console.log('{SUBMIT_MARKER}' + JSON.stringify(record));
}}
async function checkpointSending() {{
  result.sendPendingAt = new Date().toISOString();
  const record = {{
    status: 'sending',
    runId: cfg.runId,
    submissionId: cfg.runId,
    packetHash: cfg.packetHash,
    promptHash: cfg.promptHash,
    projectUrl: cfg.projectUrl,
    projectId: cfg.projectId,
    projectUrlAtSubmit: result.projectUrlAtSubmit || null,
    conversationUrl: null,
    model: result.verifiedModel,
    effort: result.verifiedEffort,
    account: result.accountEvidence || cfg.account,
    asideAccount: cfg.account,
    pendingAt: result.sendPendingAt,
    ownedTabLeftOpen: true,
    ownedTabTargetId: result.ownedTargetId,
  }};
  console.log('{SUBMIT_MARKER}' + JSON.stringify(record));
}}
async function submitPrompt() {{
  const promptText = Buffer.from(cfg.promptB64, 'base64').toString('utf8');
  if (!cfg.followUp) {{
    await verifyProject();
    const packetPath = path.join(pwd, cfg.packetName);
    await fs.writeFile(packetPath, Buffer.from(cfg.packetB64, 'base64'));
    const fileInputs = consultPage.locator('input[type="file"]');
    if (await fileInputs.count() < 1) throw new Error('ChatGPT file input not found');
    await fileInputs.nth(0).setInputFiles(packetPath);
    const attached = await snap(true);
    if (!attached.tree.includes(cfg.packetName)) throw new Error('packet upload was not visible in the composer');
  }}
  const composer = await snap(true);
  const textboxRef = refFromLine(composer.tree, line => line.includes('textbox "ChatGPT') || (line.includes('textbox "') && (line.includes('새 채팅') || line.includes('New chat in'))));
  const textbox = consultPage.locator(textboxRef);
  await textbox.click();
  await consultPage.keyboard.insertText(promptText);
  const collapseWhitespace = (value) => value.replace(/\\s+/g, ' ').trim();
  const inserted = collapseWhitespace(await textbox.innerText());
  const expectedHead = collapseWhitespace(promptText).slice(0, Math.min(80, promptText.length));
  if (!inserted || !expectedHead || !inserted.includes(expectedHead)) throw new Error('ChatGPT prompt insertion was not verified');
  let ready = await snap(true);
  let sendLine = lineFor(ready.tree, line => line.includes('button "프롬프트 보내기"') || line.includes('button "Send"'));
  for (let attempt=0; attempt<20 && (!sendLine || sendLine.includes('[disabled]')); attempt++) {{
    await sleep(500);
    ready = await snap(true);
    sendLine = lineFor(ready.tree, line => line.includes('button "프롬프트 보내기"') || line.includes('button "Send"'));
  }}
  if (!sendLine || sendLine.includes('[disabled]')) throw new Error('ChatGPT send button did not become ready');
  if (cfg.followUp) await verifyConversation();
  else await verifyProject();
  conversationUrlsBeforeSend = await conversationUrls();
  userMessagesBeforeSend = await consultPage.locator('[data-message-author-role="user"]').count();
  await checkpointSending();
  result.sendClicked = true;
  await consultPage.locator(refFromLine(ready.tree, line => line === sendLine)).click();
  let accepted = false;
  for (let attempt=0; attempt<40 && !accepted; attempt++) {{
    await snap(false);
    accepted = await consultPage.locator('[data-message-author-role="user"]').count() > userMessagesBeforeSend;
    if (!accepted) await sleep(250);
  }}
  if (!accepted) throw new Error('follow-up send was not accepted by the conversation');
  result.conversationUrl = await discoverConversationUrl();
  result.submitted = true;
  await checkpointSubmission();
}}
async function collectResponse() {{
  const deadline = Date.now() + cfg.timeoutMs;
  const assistant = consultPage.locator('[data-message-author-role="assistant"]');
  let lastText = '';
  let stable = 0;
  while (Date.now() < deadline) {{
    const count = await assistant.count();
    let current = '';
    if (count > 0) current = (await assistant.nth(count - 1).innerText()).trim();
    const stopCount = await consultPage.locator(STOP_SELECTOR).count();
    if (current && current === lastText && stopCount === 0) stable += 1;
    else stable = 0;
    lastText = current;
    if (stable >= 3) break;
    await sleep(2000);
  }}
  if (!lastText) throw new Error('no ChatGPT response was captured before timeout');
  const partial = stable < 3;
  const count = await assistant.count();
  const last = assistant.nth(count - 1);
  const links = last.locator('a[href]');
  const sources = [];
  for (let i=0; i<await links.count(); i++) {{
    const href = await links.nth(i).getAttribute('href');
    if (href && href.startsWith('https://') && !sources.includes(href)) sources.push(href);
  }}
  result.response = lastText;
  result.sources = sources;
  result.partial = partial;
  result.conversationUrl = await discoverConversationUrl();
  result.completedAt = new Date().toISOString();
}}
try {{
  const resumableTab = cfg.phase === 'collect' && cfg.resumeTargetId
    ? baselineTabs.find(t => t.targetId === cfg.resumeTargetId)
    : null;
  if (resumableTab) {{
    consultPage = await attachBrowserTab(cfg.resumeTargetId);
    result.ownedTargetId = cfg.resumeTargetId;
    result.reusedOwnedTab = true;
  }} else {{
    consultPage = await openTab(cfg.startUrl);
    const afterOpen = await listBrowserTabs();
    const owned = afterOpen.find(t => !baselineIds.has(t.targetId));
    result.ownedTargetId = owned ? owned.targetId : null;
    result.reusedOwnedTab = false;
  }}
  if (cfg.phase === 'collect') {{
    result.conversationUrl = cfg.startUrl;
    await collectResponse();
  }} else {{
    if (!cfg.followUp) await verifyProject();
    await configureMode();
    if (cfg.phase !== 'verify') {{
      // The send path is reachable only after the required surface checks above
      // have returned successfully in this same REPL lifetime.
      await submitPrompt();
      if (cfg.phase === 'both') await collectResponse();
    }}
  }}
  result.ok = true;
}} catch (error) {{
  result.error = String(error && error.stack ? error.stack : error);
  result.completedAt = new Date().toISOString();
  const preserveInFlightAnswer = Boolean(result.sendClicked || result.submitted || cfg.phase === 'collect');
  if (!preserveInFlightAnswer) {{
    try {{
      const stops = consultPage ? consultPage.locator(STOP_SELECTOR) : null;
      if (stops && await stops.count()) await stops.nth(0).click();
    }} catch {{}}
  }}
}} finally {{
  const leaveOpen = Boolean(
    consultPage && (
      (cfg.phase === 'submit' && result.submitted) ||
      result.partial ||
      (!result.ok && (result.sendClicked || result.submitted || cfg.phase === 'collect'))
    )
  );
  result.ownedTabLeftOpen = leaveOpen;
  result.ownedTabTargetId = leaveOpen ? result.ownedTargetId : null;
  if (leaveOpen) {{
    try {{ result.ownedTabUrl = await currentUrl(); }} catch {{ result.ownedTabUrl = result.conversationUrl || cfg.startUrl; }}
  }} else {{
    try {{ if (consultPage) await closeTab(consultPage); }} catch (closeError) {{ result.cleanupError = String(closeError); }}
  }}
  const finalTabs = await listBrowserTabs();
  result.baselineTargetIds = baselineTabs.map(t => t.targetId);
  result.finalTargetIds = finalTabs.map(t => t.targetId);
  result.baselineRestored = !leaveOpen && Boolean(result.ownedTargetId) && !result.finalTargetIds.includes(result.ownedTargetId);
}}
console.log('{MARKER}' + JSON.stringify(result));
"""


def extract_marker(output: str, marker: str) -> dict[str, Any] | None:
    index = output.rfind(marker)
    if index < 0:
        return None
    payload = output[index + len(marker) :]
    payload = re.split(r"\r?\n", payload, maxsplit=1)[0].strip()
    # PTY output can leave ANSI reset codes at the end of the JSON line.
    payload = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", payload).strip()
    try:
        record = json.loads(payload)
    except json.JSONDecodeError:
        return None
    return record if isinstance(record, dict) else None


def run_aside_repl(
    command: list[str], session_path: Path, *, follow_up: bool = False
) -> tuple[int, str, str, dict[str, Any] | None]:
    """Stream the REPL and durably publish an accepted submission immediately."""
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors="replace",
        env=os.environ.copy(),
    )
    stdout_chunks: list[str] = []
    stderr_chunks: list[str] = []

    def drain_stderr() -> None:
        assert proc.stderr is not None
        stderr_chunks.extend(proc.stderr)

    stderr_thread = threading.Thread(target=drain_stderr, daemon=True)
    stderr_thread.start()
    submitted: dict[str, Any] | None = None
    assert proc.stdout is not None
    for line in proc.stdout:
        stdout_chunks.append(line)
        candidate = extract_marker(line, SUBMIT_MARKER)
        if is_valid_checkpoint(candidate) or is_valid_pending_checkpoint(candidate):
            merged = merge_checkpoint(load_session(session_path), candidate, follow_up=follow_up)
            write_json(session_path, merged)
            submitted = candidate
    return_code = proc.wait()
    stderr_thread.join()
    return return_code, "".join(stdout_chunks), "".join(stderr_chunks), submitted


def resolve_project_url(args: argparse.Namespace) -> tuple[str, str] | None:
    project_url = args.project_url or os.environ.get("CONSULT_PROJECT_URL") or read_config_value("CONSULT_PROJECT_URL")
    if not project_url:
        return None
    parsed = urlparse(project_url)
    match = re.fullmatch(r"/g/(g-p-[A-Za-z0-9_-]+)/project/?", parsed.path)
    if parsed.scheme != "https" or parsed.netloc != "chatgpt.com":
        return None
    if not match:
        return None
    return project_url, match.group(1)


def project_setup_error(configured: str | None) -> str:
    if configured:
        return (
            f"CONSULT_PROJECT_URL is not a ChatGPT project URL: {configured}\n"
            "Expected a URL containing a project id such as https://chatgpt.com/g/g-p-<id>/project"
        )
    return (
        "no ChatGPT project is configured, so a new consult would land in the personal chat root.\n"
        f"Set CONSULT_PROJECT_URL in {CONFIG_PATHS[0]} , for example:\n"
        "  CONSULT_PROJECT_URL=https://chatgpt.com/g/g-p-<id>/project"
    )


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    aside = shutil.which("aside")
    script = shutil.which("script")
    if not aside:
        print("aside CLI not found", file=sys.stderr)
        return 127
    if not script:
        print("script utility not found; a PTY is required for Aside REPL", file=sys.stderr)
        return 127

    packet_path = Path(args.packet).expanduser()
    prompt_path = Path(args.prompt_file).expanduser()
    response_path = Path(args.response_output).expanduser()
    json_path = Path(args.json_output).expanduser()
    stderr_path = Path(args.stderr_output).expanduser()
    session_path = (
        Path(args.session_file).expanduser()
        if args.session_file
        else default_session_path(args.account)
    )

    if sum((args.send_only, args.resume, args.dry_run)) > 1:
        print("choose only one of --send-only, --resume, or --dry-run", file=sys.stderr)
        return EXIT_INVALID

    if not acquire_session_lock(session_path):
        print(
            f"another consult run holds {session_path}; wait for it to finish "
            "rather than starting a second submission",
            file=sys.stderr,
        )
        return EXIT_LOCKED

    saved = load_session(session_path)
    project_id: str | None = None
    project_url: str | None = None
    if args.resume:
        phase = "collect"
    elif args.dry_run:
        phase = "verify"
    elif args.send_only:
        phase = "submit"
    else:
        phase = "both"

    if args.resume:
        saved_url = str(saved.get("conversationUrl") or "")
        start_url = args.session or saved_url
        if not is_conversation_url(start_url):
            print("--resume needs a saved ChatGPT conversation URL", file=sys.stderr)
            return EXIT_INVALID
        packet_text = ""
        prompt_text = ""
    elif args.follow_up:
        packet_text = ""
        prompt_text = args.follow_up
        saved_url = str(saved.get("conversationUrl") or "")
        if not is_conversation_url(saved_url) or (args.session and args.session != saved_url):
            print("follow-up must use the conversation URL in the saved session file", file=sys.stderr)
            return EXIT_INVALID
        start_url = saved_url
        project_url = str(saved.get("projectUrl") or "") or None
        project_id = str(saved.get("projectId") or "") or None
        if not project_url or not project_id:
            print("follow-up requires project identity in the saved session file", file=sys.stderr)
            return EXIT_INVALID
    else:
        resolved = resolve_project_url(args)
        if not resolved:
            configured = args.project_url or os.environ.get("CONSULT_PROJECT_URL") or read_config_value("CONSULT_PROJECT_URL")
            print(project_setup_error(configured), file=sys.stderr)
            return EXIT_INVALID
        start_url, project_id = resolved
        project_url = start_url
        if phase == "verify":
            packet_text = ""
            prompt_text = ""
        elif not packet_path.exists():
            print(f"consult packet not found: {packet_path}", file=sys.stderr)
            return EXIT_INVALID
        elif not prompt_path.exists():
            print(f"consult prompt not found: {prompt_path}", file=sys.stderr)
            return EXIT_INVALID
        elif packet_path.stat().st_size > MAX_PACKET_BYTES:
            print(f"consult packet exceeds {MAX_PACKET_BYTES:,} bytes; narrow the packet", file=sys.stderr)
            return EXIT_INVALID
        else:
            packet_text = read_text(packet_path)
            prompt_text = read_text(prompt_path)

        packet_hash = hash_text(packet_text)
        prompt_hash = hash_text(prompt_text)
        same_submission = any(
            record.get("packetHash") == packet_hash
            and record.get("promptHash") == prompt_hash
            and record.get("projectId") == project_id
            for record in session_records(saved)
        )
        unfinished = saved.get("status") in {"sending", "submitted", "partial"}
        legacy_follow_up = (
            saved.get("status") == "complete"
            and saved.get("packetHash") == hash_text("")
            and not saved.get("followUps")
        )
        if not args.new and phase != "verify" and (unfinished or same_submission or legacy_follow_up):
            if saved.get("status") == "sending":
                location = f"pending checkpoint: {session_path} (conversation URL not captured)"
                next_step = "Inspect the pending run manually; do not resend automatically."
            else:
                location = str(saved.get("conversationUrl"))
                next_step = "Use --resume for an unfinished answer, or --new only when a separate conversation is intentional."
            print(
                "this consult is already recorded and will not be sent again:\n"
                f"  {location}\n"
                f"{next_step}",
                file=sys.stderr,
            )
            return EXIT_ALREADY_SUBMITTED

    packet_hash = hash_text(packet_text)
    prompt_hash = hash_text(prompt_text)
    run_id = str(uuid.uuid4())

    timeout = args.timeout or (3600 if args.mode == "deep" else 600)
    session_path.parent.mkdir(parents=True, exist_ok=True)
    js = build_js(
        mode=args.mode,
        phase=phase,
        packet_b64=encode_text(packet_text),
        prompt_b64=encode_text(prompt_text),
        packet_name=packet_path.name,
        timeout_seconds=timeout,
        start_url=start_url,
        follow_up=bool(args.follow_up),
        project_id=project_id,
        project_url=project_url,
        run_id=run_id,
        packet_hash=packet_hash,
        prompt_hash=prompt_hash,
        account=args.account,
        resume_target_id=(str(saved.get("ownedTabTargetId") or "") or None) if args.resume else None,
    )

    if not ensure_aside_running(aside, script, args.account):
        print("Aside Browser could not be started or reached; open it and retry", file=sys.stderr)
        return EXIT_FAILED

    command = [script, "-q", "/dev/null", aside, "repl", "--account", args.account, js]
    _return_code, stdout, stderr, submitted = run_aside_repl(
        command, session_path, follow_up=bool(args.follow_up)
    )
    write_text(stderr_path, stderr)
    result = extract_marker(stdout, MARKER)

    # A malformed submission marker can still be recovered from a complete result.
    if not submitted and result and result.get("submitted") and is_conversation_url(result.get("conversationUrl")):
        submitted = {
            "status": "submitted",
            "runId": run_id,
            "submissionId": run_id,
            "packetHash": packet_hash,
            "promptHash": prompt_hash,
            "projectUrl": project_url,
            "projectId": project_id,
            "conversationUrl": result.get("conversationUrl"),
            "submittedAt": result.get("submittedAt") or result.get("completedAt"),
            "model": result.get("verifiedModel"),
            "effort": result.get("verifiedEffort"),
            "account": result.get("accountEvidence") or args.account,
            "asideAccount": args.account,
            "ownedTabLeftOpen": bool(result.get("ownedTabLeftOpen")),
            "ownedTabTargetId": result.get("ownedTabTargetId") or result.get("ownedTargetId"),
        }
        if is_valid_checkpoint(submitted):
            write_json(
                session_path,
                merge_checkpoint(load_session(session_path), submitted, follow_up=bool(args.follow_up)),
            )
        else:
            submitted = None

    send_was_clicked = bool(
        result
        and (
            result.get("sendClicked")
            or "send was clicked but no accepted conversation URL appeared"
            in str(result.get("error") or "")
        )
    )
    if not submitted and send_was_clicked:
        submitted = {
            "status": "sending",
            "runId": run_id,
            "submissionId": run_id,
            "packetHash": packet_hash,
            "promptHash": prompt_hash,
            "projectUrl": project_url,
            "projectId": project_id,
            "conversationUrl": None,
            "pendingAt": result.get("sendPendingAt") or datetime.now(timezone.utc).isoformat(),
            "model": result.get("verifiedModel") or "GPT-5.6 Sol",
            "effort": result.get("verifiedEffort") or ("Pro" if args.mode == "deep" else "매우 높음"),
            "account": result.get("accountEvidence") or args.account,
            "asideAccount": args.account,
            "ownedTabLeftOpen": bool(result.get("ownedTabLeftOpen", True)),
            "ownedTabTargetId": result.get("ownedTabTargetId") or result.get("ownedTargetId"),
        }
        if is_valid_pending_checkpoint(submitted):
            write_json(
                session_path,
                merge_checkpoint(load_session(session_path), submitted, follow_up=bool(args.follow_up)),
            )
        else:
            submitted = None

    if result is None:
        write_text(stderr_path, stderr + "\n[stdout]\n" + stdout)
        if submitted:
            if submitted.get("status") == "sending":
                print(
                    "Aside consult reached the send boundary but no conversation URL was captured.\n"
                    f"The pending checkpoint is recorded at {session_path}; do not resend automatically.",
                    file=sys.stderr,
                )
            else:
                print(
                    "Aside consult lost its result marker after the prompt was already sent.\n"
                    f"The conversation is recorded at {submitted.get('conversationUrl')}; collect it with --resume.",
                    file=sys.stderr,
                )
            if submitted.get("ownedTabLeftOpen"):
                print(
                    "owned tab left open at "
                    f"{submitted.get('conversationUrl') or start_url} "
                    "so the in-flight answer can finish; collect later with --resume",
                    file=sys.stderr,
                )
            return EXIT_ALREADY_SUBMITTED
        print(f"Aside consult result parsing failed; see {stderr_path}", file=sys.stderr)
        return EXIT_FAILED

    write_json(json_path, result)
    if result.get("ownedTabLeftOpen"):
        open_record = dict(load_session(session_path))
        if open_record:
            open_record.update(
                {
                    "ownedTabLeftOpen": True,
                    "ownedTabTargetId": result.get("ownedTabTargetId") or result.get("ownedTargetId"),
                    "ownedTabUrl": result.get("ownedTabUrl") or result.get("conversationUrl"),
                }
            )
            write_json(session_path, open_record)
    durable_submission = submitted or (
        saved if args.resume and saved.get("status") in {"sending", "submitted", "partial"} else None
    )
    if not result.get("ok"):
        print(f"Aside consult failed: {result.get('error', 'unknown error')}; see {json_path}", file=sys.stderr)
        if result.get("ownedTabLeftOpen"):
            print(
                "owned tab left open at "
                f"{result.get('ownedTabUrl') or result.get('conversationUrl')} "
                "so the in-flight answer can finish; collect later with --resume",
                file=sys.stderr,
            )
        return EXIT_ALREADY_SUBMITTED if durable_submission else EXIT_FAILED
    if not result.get("baselineRestored") and not result.get("ownedTabLeftOpen"):
        print(f"Aside consult completed but tab baseline was not restored; see {json_path}", file=sys.stderr)
        return EXIT_ALREADY_SUBMITTED if durable_submission else EXIT_FAILED

    if phase == "verify":
        print(f"verified project: {result.get('projectUrlAtSubmit')}")
        print(f"verified model: {result.get('verifiedModel')} / {result.get('verifiedEffort')}")
        print("nothing was sent")
        return EXIT_OK

    if phase == "submit":
        print(f"submitted consult: {result.get('conversationUrl')}")
        print(f"saved consult session: {session_path.resolve()}")
        if result.get("ownedTabLeftOpen"):
            print(
                "owned tab left open at "
                f"{result.get('ownedTabUrl') or result.get('conversationUrl')} "
                "so the in-flight answer can finish"
            )
        print("collect the answer with --resume")
        return EXIT_OK

    response = str(result.get("response") or "").rstrip()
    sources = result.get("sources") if isinstance(result.get("sources"), list) else []
    if sources:
        response += "\n\n## Captured source links\n\n" + "\n".join(f"- {url}" for url in sources)
    write_text(response_path, response + "\n")
    partial = bool(result.get("partial"))
    session_record = dict(load_session(session_path))
    completion = {
        "status": "partial" if partial else "complete",
        "mode": args.mode,
        "verifiedModel": result.get("verifiedModel"),
        "verifiedEffort": result.get("verifiedEffort"),
        "conversationUrl": result.get("conversationUrl"),
        "responseOutput": str(response_path),
        "updatedAt": result.get("completedAt"),
        "ownedTabLeftOpen": bool(result.get("ownedTabLeftOpen")),
        "ownedTabTargetId": result.get("ownedTabTargetId"),
        "ownedTabUrl": result.get("ownedTabUrl"),
    }
    if args.follow_up:
        follow_ups = list(session_record.get("followUps") or [])
        if follow_ups:
            follow_ups[-1] = {**follow_ups[-1], **completion}
            session_record["followUps"] = follow_ups
            session_record["updatedAt"] = result.get("completedAt")
    else:
        session_record.update(completion)
    write_json(session_path, session_record)
    print(f"wrote consult response: {response_path.resolve()}")
    print(f"saved Aside consult evidence: {json_path.resolve()}")
    print(f"saved consult session: {session_path.resolve()}")
    return EXIT_PARTIAL if partial else EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
