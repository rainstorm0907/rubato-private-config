#!/usr/bin/env python3
"""Build a self-contained consult packet from local repo context.

The script is intentionally local-only: it reads files, git metadata, and optional
log files, then writes a Markdown packet that a code agent can augment before
sharing with an external consultant.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import glob as _glob
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Iterable, List, Sequence, Tuple

EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "bower_components",
    "dist",
    "build",
    "out",
    "target",
    "coverage",
    ".next",
    ".nuxt",
    ".turbo",
    ".cache",
    "__pycache__",
}

MANIFEST_NAMES = {
    "package.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "package-lock.json",
    "bun.lockb",
    "pyproject.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "poetry.lock",
    "Pipfile",
    "Pipfile.lock",
    "Cargo.toml",
    "Cargo.lock",
    "go.mod",
    "go.sum",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "Gemfile",
    "Gemfile.lock",
    "composer.json",
    "composer.lock",
    "deno.json",
    "deno.lock",
    "tsconfig.json",
    "vite.config.ts",
    "next.config.js",
    "next.config.mjs",
}

SECRET_PATTERNS: Sequence[Tuple[re.Pattern[str], str]] = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S), "<REDACTED_PRIVATE_KEY>"),
    (re.compile(r"(?i)(authorization\s*[:=]\s*bearer\s+)[A-Za-z0-9._~+/=-]+"), r"\1<REDACTED>"),
    (re.compile(r"(?i)((?:api[_-]?key|token|secret|password|passwd|pwd|client[_-]?secret)\s*[:=]\s*['\"]?)[^'\"\s,;]+"), r"\1<REDACTED>"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "<REDACTED_AWS_ACCESS_KEY>"),
    (re.compile(r"\bASIA[0-9A-Z]{16}\b"), "<REDACTED_AWS_SESSION_KEY>"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"), "<REDACTED_GITHUB_TOKEN>"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"), "<REDACTED_OPENAI_STYLE_KEY>"),
    (re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b"), "<REDACTED_ANTHROPIC_KEY>"),
    (re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"), "<REDACTED_JWT>"),
]

LANG_BY_SUFFIX = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "jsx",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".java": "java",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".php": "php",
    ".cs": "csharp",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".c": "c",
    ".h": "c",
    ".hpp": "cpp",
    ".swift": "swift",
    ".scala": "scala",
    ".sql": "sql",
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
    ".ps1": "powershell",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".xml": "xml",
    ".html": "html",
    ".css": "css",
    ".scss": "scss",
    ".md": "markdown",
}


def run(cmd: Sequence[str], cwd: Path, timeout: int = 12) -> str:
    try:
        proc = subprocess.run(
            list(cmd),
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return f"command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return f"command timed out after {timeout}s: {' '.join(cmd)}"

    out = proc.stdout.strip()
    err = proc.stderr.strip()
    if err:
        out = f"{out}\n[stderr]\n{err}" if out else f"[stderr]\n{err}"
    return out.strip()


def detect_repo_root(start: Path) -> Path:
    result = run(["git", "rev-parse", "--show-toplevel"], start)
    if result and not result.startswith("[stderr]") and "not a git repository" not in result.lower():
        candidate = Path(result.splitlines()[0]).expanduser()
        if candidate.exists():
            return candidate.resolve()
    return start.resolve()


def is_git_repo(root: Path) -> bool:
    result = run(["git", "rev-parse", "--is-inside-work-tree"], root)
    return result.splitlines()[:1] == ["true"]


def redact(text: str, enabled: bool = True) -> str:
    if not enabled:
        return text
    redacted = text
    for pattern, replacement in SECRET_PATTERNS:
        redacted = pattern.sub(replacement, redacted)
    return redacted


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def is_probably_binary(data: bytes) -> bool:
    if b"\0" in data:
        return True
    if not data:
        return False
    text_bytes = sum(1 for b in data[:4096] if b in (9, 10, 13) or 32 <= b <= 126)
    return text_bytes / min(len(data), 4096) < 0.72


def read_text_file(path: Path, max_bytes: int, redact_enabled: bool) -> Tuple[str, bool, str]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return f"<could not read: {exc}>", False, "error"
    if is_probably_binary(raw):
        return "<binary file omitted>", False, "binary"
    truncated = len(raw) > max_bytes
    raw = raw[:max_bytes]
    text = raw.decode("utf-8", errors="replace")
    text = redact(text, redact_enabled)
    if truncated:
        text += f"\n\n<TRUNCATED after {max_bytes} bytes>"
    return text, truncated, "text"


def with_line_numbers(text: str) -> str:
    lines = text.splitlines()
    width = max(4, len(str(len(lines))))
    return "\n".join(f"{idx:0{width}d}: {line}" for idx, line in enumerate(lines, start=1))


def fenced(content: str, lang: str = "") -> str:
    return f"````{lang}\n{content.rstrip()}\n````"


def guess_lang(path: Path) -> str:
    return LANG_BY_SUFFIX.get(path.suffix.lower(), "")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def resolve_existing_files(values: Iterable[str], root: Path, allow_outside: bool) -> Tuple[List[Path], List[str]]:
    files: List[Path] = []
    warnings: List[str] = []
    for value in values:
        p = Path(value).expanduser()
        if not p.is_absolute():
            p = root / p
        try:
            p = p.resolve()
        except OSError:
            warnings.append(f"skipped unresolved path: {value}")
            continue
        if not allow_outside:
            try:
                p.relative_to(root.resolve())
            except ValueError:
                warnings.append(f"skipped outside repo: {value}")
                continue
        if not p.exists():
            warnings.append(f"skipped missing path: {value}")
            continue
        if p.is_dir():
            for child in sorted(p.rglob("*")):
                if child.is_file() and not is_excluded(child):
                    files.append(child)
        elif p.is_file() and not is_excluded(p):
            files.append(p)
    return unique_paths(files), warnings


def unique_paths(paths: Iterable[Path]) -> List[Path]:
    seen = set()
    result: List[Path] = []
    for p in paths:
        key = str(p.resolve())
        if key not in seen:
            seen.add(key)
            result.append(p)
    return result


def expand_globs(patterns: Iterable[str], root: Path) -> List[Path]:
    matches: List[Path] = []
    for pattern in patterns:
        for value in _glob.glob(str(root / pattern), recursive=True):
            p = Path(value)
            if p.is_file() and not is_excluded(p):
                matches.append(p.resolve())
    return unique_paths(matches)


def changed_files(root: Path, max_files: int) -> List[Path]:
    names: List[str] = []
    for cmd in (["git", "diff", "--name-only", "HEAD"], ["git", "ls-files", "--others", "--exclude-standard"]):
        output = run(cmd, root)
        if output and not output.startswith("[stderr]"):
            names.extend(line.strip() for line in output.splitlines() if line.strip())
    paths = []
    for name in names:
        p = (root / name).resolve()
        if p.exists() and p.is_file() and not is_excluded(p):
            paths.append(p)
    return unique_paths(paths)[:max_files]


def manifest_files(root: Path, limit: int = 20) -> List[Path]:
    found: List[Path] = []
    for p in sorted(root.rglob("*")):
        if len(found) >= limit:
            break
        if p.is_file() and p.name in MANIFEST_NAMES and not is_excluded(p.relative_to(root)):
            found.append(p.resolve())
    return found


def repo_map(root: Path, max_lines: int) -> str:
    output = run(["git", "ls-files"], root)
    if not output or output.startswith("[stderr]"):
        lines = []
        for p in sorted(root.rglob("*")):
            try:
                rp = p.relative_to(root)
            except ValueError:
                continue
            if is_excluded(rp):
                continue
            if p.is_file():
                lines.append(str(rp))
            if len(lines) >= max_lines:
                break
    else:
        lines = [line for line in output.splitlines() if line and not is_excluded(Path(line))]
    truncated = len(lines) > max_lines
    lines = lines[:max_lines]
    if truncated:
        lines.append(f"<TRUNCATED: showing first {max_lines} files>")
    return "\n".join(lines)


def cap_text(text: str, max_bytes: int, redact_enabled: bool) -> str:
    text = redact(text, redact_enabled)
    data = text.encode("utf-8", errors="replace")
    if len(data) <= max_bytes:
        return text
    return data[:max_bytes].decode("utf-8", errors="replace") + f"\n\n<TRUNCATED after {max_bytes} bytes>"


def append_section(parts: List[str], title: str, body: str) -> None:
    parts.append(f"## {title}\n\n{body.strip() if body.strip() else '_No data captured._'}\n")


def build_packet(args: argparse.Namespace) -> str:
    cwd = Path(args.cwd or os.getcwd()).expanduser().resolve()
    root = Path(args.repo_root).expanduser().resolve() if args.repo_root else detect_repo_root(cwd)
    git_repo = is_git_repo(root)
    redact_enabled = not args.no_redact

    explicit_files, file_warnings = resolve_existing_files(args.files or [], root, args.allow_outside_repo)
    glob_files = expand_globs(args.glob or [], root)
    include_repo_map = args.deep or args.include_repo_map
    include_manifests = args.deep or args.include_manifests
    include_changed_content = args.deep or args.include_changed_file_content
    include_diff = args.deep or args.include_diff
    if args.no_repo_map:
        include_repo_map = False
    if args.no_manifests:
        include_manifests = False
    if args.no_changed_file_content:
        include_changed_content = False
    if args.no_diff:
        include_diff = False

    if args.deep:
        args.max_file_bytes = max(args.max_file_bytes, 30000)
        args.max_log_bytes = max(args.max_log_bytes, 60000)
        args.max_diff_bytes = max(args.max_diff_bytes, 80000)
        args.max_repo_map_lines = max(args.max_repo_map_lines, 350)
        args.max_total_bytes = max(args.max_total_bytes, 220000)

    auto_changed = changed_files(root, args.max_changed_files) if include_changed_content and git_repo else []
    manifests = manifest_files(root) if include_manifests else []
    files = unique_paths([*explicit_files, *glob_files, *auto_changed, *manifests])

    now = _dt.datetime.now().astimezone().isoformat(timespec="seconds")
    parts: List[str] = []
    parts.append("# GPT Consult Packet\n")
    parts.append(
        "You are advising a coding agent. Use the packet as scoped evidence, ask for missing context only if it blocks the answer, "
        "and give concrete recommendations the local agent can verify in the repo. If current framework/library/API behavior matters, use web search and cite sources.\n"
    )
    parts.append(f"- Generated: `{now}`")
    parts.append(f"- Working directory: `{cwd}`")
    parts.append(f"- Repository root: `{root}`")
    if args.question:
        parts.append(f"- Consult question: {args.question}")
    parts.append("")

    append_section(
        parts,
        "Consult request",
        f"""
Question: {args.question or '<write the main question here>'}

답변은 한국어 보고서로 작성해 주세요. 문제에 맞는 구조와 표현을 자유롭게 선택하되, 자연스럽고 읽기 쉽게 설명해 주세요. 기술 용어와 영문 표현은 도움이 될 때 자유롭게 쓰셔도 됩니다. 권고와 그 근거, 확인 방법, 그리고 답을 뒤집을 만한 가정이나 빠진 정보는 어떤 형식으로든 반드시 담아 주세요.
""",
    )

    append_section(
        parts,
        "Current state",
        """
- Original user goal:
- Current implementation state:
- Blocker or decision needed:
- Acceptance criteria:
- Constraints / non-goals:
- Attempts already tried:
""",
    )

    if git_repo:
        git_facts = []
        for label, cmd, cap in [
            ("branch", ["git", "branch", "--show-current"], 2000),
            ("HEAD", ["git", "rev-parse", "--short", "HEAD"], 2000),
            ("status", ["git", "status", "--short"], 12000),
            ("changed files", ["git", "diff", "--name-only", "HEAD"], 12000),
        ]:
            git_facts.append(f"### {label}\n{fenced(cap_text(run(cmd, root), cap, redact_enabled))}")
        append_section(parts, "Git state", "\n\n".join(git_facts))
    else:
        append_section(parts, "Git state", "No git repository detected for this packet root.")

    if include_repo_map:
        append_section(parts, "Repository map", fenced(repo_map(root, args.max_repo_map_lines)))

    if file_warnings:
        append_section(parts, "File collection warnings", "\n".join(f"- {w}" for w in file_warnings))

    if files:
        file_sections = []
        for p in files:
            text, _truncated, kind = read_text_file(p, args.max_file_bytes, redact_enabled)
            heading = f"### {rel(p, root)}"
            if kind == "text":
                file_sections.append(f"{heading}\n{fenced(with_line_numbers(text), guess_lang(p))}")
            else:
                file_sections.append(f"{heading}\n{fenced(text)}")
        append_section(parts, "Relevant files and manifests", "\n\n".join(file_sections))
    else:
        append_section(parts, "Relevant files and manifests", "No files were provided. Add --files or --glob, then rerun, or paste exact excerpts manually.")

    if git_repo and include_diff:
        diff_stat = cap_text(run(["git", "diff", "--stat", "HEAD"], root), 20000, redact_enabled)
        diff = cap_text(run(["git", "diff", "HEAD"], root), args.max_diff_bytes, redact_enabled)
        append_section(parts, "Current diff", f"### diff stat\n{fenced(diff_stat)}\n\n### diff\n{fenced(diff, 'diff')}")

    log_files, log_warnings = resolve_existing_files(args.log_file or [], root, args.allow_outside_repo)
    log_sections = []
    for p in log_files:
        text, _truncated, kind = read_text_file(p, args.max_log_bytes, redact_enabled)
        log_sections.append(f"### {rel(p, root)}\n{fenced(text)}")
    if log_warnings:
        log_sections.append("### warnings\n" + "\n".join(f"- {w}" for w in log_warnings))
    append_section(parts, "Command outputs, errors, and logs", "\n\n".join(log_sections) or "TODO: Paste failing command, full stack trace, test output, browser console output, server logs, or CI logs here.")

    append_section(
        parts,
        "Specific questions for the consultant",
        f"""
1. {args.question or '<main question>'}
2. What assumptions should be verified before implementing the recommendation?
3. What is the smallest safe next step and test plan?
""",
    )

    append_section(
        parts,
        "Redactions and sharing notes",
        """
- Secrets were redacted using simple pattern matching; verify manually before sharing.
- Do not include private credentials, customer data, or proprietary context beyond what is approved for the consultant.
- Any omitted context should be listed explicitly here.
""",
    )

    packet = "\n".join(parts).rstrip() + "\n"
    data = packet.encode("utf-8", errors="replace")
    if args.max_total_bytes and len(data) > args.max_total_bytes:
        packet = data[: args.max_total_bytes].decode("utf-8", errors="replace")
        packet += f"\n\n<PACKET TRUNCATED after {args.max_total_bytes} bytes. Rerun with narrower --files/--glob or larger --max-total-bytes.>\n"
    return packet


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a self-contained GPT consult packet from repo context.")
    parser.add_argument("--question", "-q", default="", help="Main consult question to include in the packet.")
    parser.add_argument("--files", "-f", nargs="*", default=[], help="Relevant files or directories to include.")
    parser.add_argument("--glob", action="append", default=[], help="Glob pattern relative to repo root. Can be repeated.")
    parser.add_argument("--log-file", action="append", default=[], help="Failing command output, test log, stack trace, or CI log file. Can be repeated.")
    parser.add_argument("--output", "-o", default="", help="Output Markdown path. Defaults to stdout.")
    parser.add_argument("--cwd", default="", help="Working directory to inspect. Defaults to current directory.")
    parser.add_argument("--repo-root", default="", help="Repository root. Defaults to git root or current directory.")
    parser.add_argument("--allow-outside-repo", action="store_true", help="Allow explicitly listed files outside repo root.")
    parser.add_argument("--no-redact", action="store_true", help="Disable simple secret redaction. Use only for trusted local review.")
    parser.add_argument("--no-diff", action="store_true", help="Do not include git diff. Compatibility alias; diff is off by default unless --include-diff or --deep is used.")
    parser.add_argument("--no-repo-map", action="store_true", help="Do not include repository file map.")
    parser.add_argument("--no-manifests", action="store_true", help="Do not auto-include dependency/runtime manifest files.")
    parser.add_argument("--no-changed-file-content", action="store_true", help="Do not auto-include contents of changed files.")
    parser.add_argument("--include-diff", action="store_true", help="Include git diff body and diff stat. Off by default to keep packets focused.")
    parser.add_argument("--include-repo-map", action="store_true", help="Include a repository file map. Off by default to keep packets focused.")
    parser.add_argument("--include-manifests", action="store_true", help="Auto-include dependency/runtime manifest file contents. Off by default.")
    parser.add_argument("--include-changed-file-content", action="store_true", help="Auto-include changed/untracked file contents. Off by default; prefer explicit --files.")
    parser.add_argument("--deep", action="store_true", help="Build a broad packet: repo map, manifests, changed file contents, and larger caps.")
    parser.add_argument("--max-changed-files", type=int, default=12, help="Maximum changed/untracked files to auto-include.")
    parser.add_argument("--max-file-bytes", type=int, default=12000, help="Maximum bytes per included source file.")
    parser.add_argument("--max-log-bytes", type=int, default=24000, help="Maximum bytes per log file.")
    parser.add_argument("--max-diff-bytes", type=int, default=30000, help="Maximum bytes of git diff.")
    parser.add_argument("--max-repo-map-lines", type=int, default=120, help="Maximum lines in repository map.")
    parser.add_argument("--max-total-bytes", type=int, default=90000, help="Maximum total packet bytes. 0 disables total cap.")
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    packet = build_packet(args)
    if args.output:
        out = Path(args.output).expanduser()
        if not out.is_absolute():
            out = Path(os.getcwd()) / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(packet, encoding="utf-8")
        print(f"wrote consult packet: {out}")
    else:
        sys.stdout.write(packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
