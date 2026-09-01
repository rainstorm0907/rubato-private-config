#!/usr/bin/env python3
"""Prepare a ChatGPT web prompt for GPT Consult.

This script is deliberately browser/API agnostic. It only reads the local consult
packet, writes a prompt file, and optionally copies text to the system clipboard
using normal OS clipboard commands. It does not use OpenAI APIs, private
endpoints, browser automation protocols, cookies, or tokens.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Sequence

DEFAULT_OUTPUT = ".consult/chatgpt-web-prompt.md"
DEFAULT_UPLOAD_INSTRUCTIONS = ".consult/chatgpt-upload-instructions.md"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def clipboard_command_for_paste() -> list[str] | None:
    if shutil.which("pbcopy"):
        return ["pbcopy"]
    if shutil.which("wl-copy"):
        return ["wl-copy"]
    if shutil.which("xclip"):
        return ["xclip", "-selection", "clipboard"]
    if shutil.which("xsel"):
        return ["xsel", "--clipboard", "--input"]
    if os.name == "nt" and shutil.which("clip"):
        return ["clip"]
    return None


def copy_to_clipboard(text: str) -> None:
    cmd = clipboard_command_for_paste()
    if not cmd:
        raise RuntimeError("no supported clipboard command found: expected pbcopy, wl-copy, xclip, xsel, or clip")
    proc = subprocess.run(cmd, input=text, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"clipboard command failed ({' '.join(cmd)}): {proc.stderr.strip()}")


QUESTION_PATTERN = re.compile(r"^- Consult question: (.+)$", re.MULTILINE)


def extract_question(packet: str) -> str:
    match = QUESTION_PATTERN.search(packet)
    return match.group(1).strip() if match else "repository packet review"


def build_full_prompt(packet: str, source_path: str, model_hint: str, question: str) -> str:
    generated = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    return f"""Consult: {question}

You are {model_hint} acting as a senior software architecture and debugging consultant for a coding agent.

Important context:
- You do not have repository access.
- You do not have terminal access.
- You do not have the previous coding-agent conversation.
- The packet below is intended to be self-contained.
- Use only the packet facts unless you explicitly state an assumption.
- Use web search and cite sources when current library/framework/API behavior, security advisories, release notes, browser behavior, or ecosystem best practice matters.
- Give actionable advice that the coding agent can apply in its current repo session.

답변은 한국어 보고서로 작성해 주세요. 문제에 맞는 구조와 표현을 자유롭게 선택하되, 자연스럽고 읽기 쉽게 설명해 주세요. 기술 용어와 영문 표현은 도움이 될 때 자유롭게 쓰셔도 됩니다. 권고와 그 근거, 확인 방법, 그리고 답을 뒤집을 만한 가정이나 빠진 정보는 어떤 형식으로든 반드시 담아 주세요.

Metadata:
- Generated for ChatGPT web: {generated}
- Packet source path in local repo: {source_path}

--- BEGIN SELF-CONTAINED CONSULT PACKET ---

{packet.rstrip()}

--- END SELF-CONTAINED CONSULT PACKET ---
"""


def build_upload_instructions(packet_path: str, model_hint: str, question: str) -> str:
    generated = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    return f"""Consult: {question}

You are {model_hint} acting as a senior software architecture and debugging consultant for a coding agent.

I have uploaded a Markdown file containing a self-contained repository-context packet.

Important context:
- You do not have repository access beyond the uploaded packet.
- You do not have terminal access.
- You do not have the previous coding-agent conversation.
- Treat the uploaded packet as the source of truth.
- Use web search and cite sources when current library/framework/API behavior, security advisories, release notes, browser behavior, or ecosystem best practice matters.
- Give actionable advice that the coding agent can apply in its current repo session.

답변은 한국어 보고서로 작성해 주세요. 문제에 맞는 구조와 표현을 자유롭게 선택하되, 자연스럽고 읽기 쉽게 설명해 주세요. 기술 용어와 영문 표현은 도움이 될 때 자유롭게 쓰셔도 됩니다. 권고와 그 근거, 확인 방법, 그리고 답을 뒤집을 만한 가정이나 빠진 정보는 어떤 형식으로든 반드시 담아 주세요.

Metadata:
- Generated for ChatGPT web: {generated}
- Local packet path: {packet_path}

Please analyze the uploaded packet now.
"""


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare a ChatGPT web prompt from a GPT consult packet.")
    parser.add_argument("--packet", default=".consult/consult-packet.md", help="Consult packet Markdown file.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Full paste prompt output file.")
    parser.add_argument("--upload-instructions", default=DEFAULT_UPLOAD_INSTRUCTIONS, help="Upload instruction prompt output file.")
    parser.add_argument("--mode", choices=("quick", "deep"), default="quick")
    parser.add_argument("--question", default=None, help="Chat title line; defaults to the question recorded in the packet.")
    parser.add_argument("--model-hint", default=None, help="Override the visible ChatGPT web model/mode wording.")
    parser.add_argument("--copy", action="store_true", help="Copy the full paste prompt to the system clipboard.")
    parser.add_argument("--copy-upload-instructions", action="store_true", help="Copy only the upload instruction prompt to the system clipboard.")
    parser.add_argument("--warn-chars", type=int, default=120000, help="Warn when the full prompt exceeds this many characters.")
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    packet_path = Path(args.packet).expanduser().resolve()
    if not packet_path.exists():
        print(f"packet not found: {packet_path}", file=sys.stderr)
        return 2

    packet = read_text(packet_path)
    model_hint = args.model_hint or (
        "GPT-5.6 Sol with Pro reasoning" if args.mode == "deep"
        else "GPT-5.6 Sol with very high reasoning"
    )
    question = args.question or extract_question(packet)
    full_prompt = build_full_prompt(packet, str(packet_path), model_hint, question)
    upload_instructions = build_upload_instructions(str(packet_path), model_hint, question)

    output_path = Path(args.output).expanduser()
    upload_path = Path(args.upload_instructions).expanduser()
    write_text(output_path, full_prompt)
    write_text(upload_path, upload_instructions)

    print(f"wrote full ChatGPT web prompt: {output_path.resolve()} ({len(full_prompt):,} chars)")
    print(f"wrote upload instructions: {upload_path.resolve()} ({len(upload_instructions):,} chars)")
    if len(full_prompt) > args.warn_chars:
        print(
            f"warning: full prompt is {len(full_prompt):,} chars; if pasting is unreliable, upload {packet_path} and paste {upload_path}",
            file=sys.stderr,
        )

    try:
        if args.copy and args.copy_upload_instructions:
            print("choose only one of --copy or --copy-upload-instructions", file=sys.stderr)
            return 2
        if args.copy:
            copy_to_clipboard(full_prompt)
            print("copied full prompt to clipboard")
        elif args.copy_upload_instructions:
            copy_to_clipboard(upload_instructions)
            print("copied upload instructions to clipboard")
    except RuntimeError as exc:
        print(f"clipboard copy failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
