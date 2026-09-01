#!/usr/bin/env python3
"""One-command entry point for a verified ChatGPT web consult."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import time
from typing import Sequence


SCRIPT_DIR = Path(__file__).resolve().parent


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a focused packet, select the verified GPT-5.6 Sol reasoning "
            "level, and run Consult in the configured Woojin ChatGPT project."
        )
    )
    parser.add_argument("--question", "-q", required=True, help="One exact question for the consultant.")
    parser.add_argument("--files", "-f", nargs="*", default=[], help="Relevant files or directories.")
    parser.add_argument("--glob", action="append", default=[], help="Repo-relative glob; repeat as needed.")
    parser.add_argument("--log-file", action="append", default=[], help="Log or command output file; repeat as needed.")
    parser.add_argument("--mode", choices=("quick", "deep"), default=None)
    parser.add_argument("--deep", action="store_true", help="Alias for --mode deep.")
    parser.add_argument("--include-diff", action="store_true", help="Include the current git diff in a quick packet.")
    parser.add_argument("--allow-outside-repo", action="store_true")
    parser.add_argument("--output-dir", default=".consult")
    parser.add_argument("--send-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Verify project, model, and reasoning without sending.")
    parser.add_argument("--new", action="store_true", help="Intentionally start a separate conversation.")
    parser.add_argument("--timeout", type=int, default=None)
    parser.add_argument(
        "--collect-window",
        type=int,
        default=30,
        help="Seconds each fresh response-collection connection may stay open.",
    )
    parser.add_argument(
        "--collect-attempts",
        type=int,
        default=None,
        help="Fresh collection attempts; defaults to 20 for quick and 120 for deep.",
    )
    parser.add_argument("--account", default="u0")
    args = parser.parse_args(argv)
    if args.deep and args.mode == "quick":
        parser.error("--deep conflicts with --mode quick")
    if args.send_only and args.dry_run:
        parser.error("--send-only conflicts with --dry-run")
    args.mode = "deep" if args.deep else (args.mode or "quick")
    if args.collect_window < 1:
        parser.error("--collect-window must be at least 1")
    if args.collect_attempts is not None and args.collect_attempts < 1:
        parser.error("--collect-attempts must be at least 1")
    return args


def build_commands(args: argparse.Namespace, cwd: Path | None = None) -> list[list[str]]:
    workdir = (cwd or Path.cwd()).resolve()
    output_dir = Path(args.output_dir).expanduser()
    if not output_dir.is_absolute():
        output_dir = workdir / output_dir
    packet = output_dir / "consult-packet.md"
    full_prompt = output_dir / "chatgpt-web-prompt.md"
    upload_prompt = output_dir / "chatgpt-upload-instructions.md"
    response = output_dir / "consult-response.md"
    evidence = output_dir / "aside-consult-response.json"
    stderr_log = output_dir / "aside-consult-stderr.log"

    build = [
        sys.executable,
        str(SCRIPT_DIR / "build_consult_packet.py"),
        "--question",
        args.question,
        "--cwd",
        str(workdir),
        "--output",
        str(packet),
    ]
    if args.files:
        build.extend(["--files", *args.files])
    for pattern in args.glob:
        build.extend(["--glob", pattern])
    for log_file in args.log_file:
        build.extend(["--log-file", log_file])
    if args.mode == "deep":
        build.append("--deep")
    elif args.include_diff:
        build.append("--include-diff")
    if args.allow_outside_repo:
        build.append("--allow-outside-repo")

    prepare = [
        sys.executable,
        str(SCRIPT_DIR / "prepare_chatgpt_web_prompt.py"),
        "--mode",
        args.mode,
        "--packet",
        str(packet),
        "--output",
        str(full_prompt),
        "--upload-instructions",
        str(upload_prompt),
    ]

    run = [
        sys.executable,
        str(SCRIPT_DIR / "run_aside_consult.py"),
        "--mode",
        args.mode,
        "--packet",
        str(packet),
        "--prompt-file",
        str(upload_prompt),
        "--response-output",
        str(response),
        "--json-output",
        str(evidence),
        "--stderr-output",
        str(stderr_log),
        "--account",
        args.account,
    ]
    for enabled, flag in (
        (args.send_only, "--send-only"),
        (args.dry_run, "--dry-run"),
        (args.new, "--new"),
    ):
        if enabled:
            run.append(flag)
    if args.timeout is not None:
        run.extend(["--timeout", str(args.timeout)])
    return [build, prepare, run]


def build_resume_command(args: argparse.Namespace, run_command: list[str]) -> list[str]:
    option_values = {
        flag: run_command[run_command.index(flag) + 1]
        for flag in (
            "--mode",
            "--response-output",
            "--json-output",
            "--stderr-output",
            "--account",
        )
    }
    return [
        sys.executable,
        str(SCRIPT_DIR / "run_aside_consult.py"),
        "--mode",
        option_values["--mode"],
        "--resume",
        "--response-output",
        option_values["--response-output"],
        "--json-output",
        option_values["--json-output"],
        "--stderr-output",
        option_values["--stderr-output"],
        "--account",
        option_values["--account"],
        "--timeout",
        str(args.collect_window),
    ]


def run_stage(
    stage: str,
    command: list[str],
    *,
    show_success: bool = False,
    show_failure: bool = True,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode and show_failure:
        detail = (completed.stderr or completed.stdout or "").strip()
        print(f"consult stopped during {stage} (exit {completed.returncode})", file=sys.stderr)
        if detail:
            print(detail, file=sys.stderr)
    elif not completed.returncode and show_success:
        detail = (completed.stdout or "").strip()
        if detail:
            print(detail)
    return completed


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    build, prepare, run = build_commands(args)
    Path(args.output_dir).expanduser().mkdir(parents=True, exist_ok=True)
    for stage, command in (("packet build", build), ("prompt preparation", prepare)):
        completed = run_stage(stage, command)
        if completed.returncode:
            return completed.returncode

    if args.dry_run or args.send_only:
        return run_stage("verified consult", run, show_success=True).returncode

    # Submission and collection deliberately use separate Aside REPL lifetimes.
    # A dropped collector can be retried safely; the prompt is never submitted twice.
    submit = [*run, "--send-only"]
    completed = run_stage("submission", submit)
    if completed.returncode:
        return completed.returncode

    resume = build_resume_command(args, run)
    attempts = args.collect_attempts or (120 if args.mode == "deep" else 20)
    retryable = {1, 3, 4}
    return_code = 1
    completed: subprocess.CompletedProcess[str] | None = None
    for attempt in range(1, attempts + 1):
        completed = run_stage(
            f"response collection {attempt}/{attempts}",
            resume,
            show_failure=False,
        )
        return_code = completed.returncode
        if return_code == 0:
            response_path = resume[resume.index("--response-output") + 1]
            print(f"consult complete after {attempt} collection attempt(s)")
            print(f"response: {Path(response_path).resolve()}")
            return 0
        if return_code not in retryable:
            detail = (completed.stderr or completed.stdout or "").strip()
            print(
                f"consult stopped during response collection "
                f"{attempt}/{attempts} (exit {return_code})",
                file=sys.stderr,
            )
            if detail:
                print(detail, file=sys.stderr)
            return return_code
        if attempt < attempts:
            time.sleep(2)
    detail = (completed.stderr or completed.stdout or "").strip() if completed else ""
    print(
        f"consult response collection exhausted {attempts} fresh connections "
        f"(exit {return_code}); the submitted conversation was not resent",
        file=sys.stderr,
    )
    if detail:
        print(detail, file=sys.stderr)
    return return_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
