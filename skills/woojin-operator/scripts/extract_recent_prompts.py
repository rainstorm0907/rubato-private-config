#!/usr/bin/env python3
"""Summarize recent Claude/Codex user prompt patterns with redaction."""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

HOME = Path.home()
DEFAULT_ROOTS = {
    "claude": HOME / ".claude" / "projects",
    "codex": HOME / ".codex" / "sessions",
}

PATTERNS = {
    "evidence_source_path": re.compile(r"exact|경로|source|cutoff|원문|근거|실제|artifact|파일", re.I),
    "read_first": re.compile(r"먼저|읽고|확인|파악|살펴|봐줘|검토", re.I),
    "do_not_implement_yet": re.compile(r"바로 구현|구현 들어가지 말고|작업 전에|먼저 .*제안|정하고 진행", re.I),
    "review": re.compile(r"리뷰|검토|결함|회귀|edge|P0|P1|P2|VERDICT", re.I),
    "handoff_continue": re.compile(r"이어|이전 세션|handoff|인계|compact|current-state|현재 목표", re.I),
    "research": re.compile(r"리서치|조사|출처|공식|커뮤니티|레딧|아카라이브|인벤|news\\.hada", re.I),
    "delegate_cross_model": re.compile(r"코덱스|클로드|meight|worker|subagent|리뷰어|크로스|위임", re.I),
    "ui_product_feel": re.compile(r"체감 품질|감성|느낌|자연스럽|하마 스타일|네이버지도|Maplog|지도|이쁘", re.I),
    "wrap_docs": re.compile(r"문서화|wrap|정리|마무리|기록|블로그|개발일지", re.I),
    "mood_sensitive": re.compile(r"상담|감정|예은|mood|관계|연애|멘헤라", re.I),
}

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password|pw)\s*[:=]\s*['\"]?[^\\s'\",]+"),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"),
    re.compile(r"\\b01[016789][-\\s]?\\d{3,4}[-\\s]?\\d{4}\\b"),
    re.compile(r"\\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\\b", re.I),
]


def redact(text: str) -> str:
    text = re.sub(r"\x1b\[[0-9;]*m", "", text)
    for pattern in SECRET_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    text = re.sub(r"\\s+", " ", text).strip()
    return text


def iter_files(root: Path, days: int, limit_files: int) -> Iterable[Path]:
    if not root.exists():
        return []
    cutoff = time.time() - days * 86400
    files = [p for p in root.rglob("*.jsonl") if p.stat().st_mtime >= cutoff]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files[:limit_files]


def text_from_content(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                parts.append(str(item.get("text") or item.get("content") or ""))
        return " ".join(parts)
    return ""


def user_texts_from_line(obj: dict) -> Iterable[str]:
    msg = obj.get("message")
    if isinstance(msg, dict) and msg.get("role") == "user":
        yield text_from_content(msg.get("content"))

    if obj.get("role") == "user":
        yield text_from_content(obj.get("content"))

    if obj.get("type") == "response_item":
        payload = obj.get("payload") or {}
        if payload.get("type") == "message" and payload.get("role") == "user":
            yield text_from_content(payload.get("content"))

    if obj.get("type") == "turn_context":
        payload = obj.get("payload") or {}
        if payload.get("user_message"):
            yield str(payload.get("user_message"))


def should_skip(text: str, include_sensitive: bool) -> bool:
    if not text:
        return True
    ignored = ("<local-command-caveat>", "<local-command-stdout>", "<task-notification>")
    if any(marker in text for marker in ignored):
        return True
    if not include_sensitive and PATTERNS["mood_sensitive"].search(text):
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", choices=["claude", "codex", "both"], default="both")
    parser.add_argument("--days", type=int, default=14)
    parser.add_argument("--limit-files", type=int, default=40)
    parser.add_argument("--examples-per-pattern", type=int, default=3)
    parser.add_argument("--include-sensitive", action="store_true")
    args = parser.parse_args()

    roots = ["claude", "codex"] if args.root == "both" else [args.root]
    counts: Counter[str] = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    scanned_files = 0
    scanned_prompts = 0

    for name in roots:
        for path in iter_files(DEFAULT_ROOTS[name], args.days, args.limit_files):
            scanned_files += 1
            try:
                lines = path.read_text(errors="ignore").splitlines()
            except OSError:
                continue
            for line in lines:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                for raw in user_texts_from_line(obj):
                    text = redact(raw)
                    if should_skip(text, args.include_sensitive):
                        continue
                    scanned_prompts += 1
                    for key, pattern in PATTERNS.items():
                        if key == "mood_sensitive" and not args.include_sensitive:
                            continue
                        if pattern.search(text):
                            counts[key] += 1
                            if len(examples[key]) < args.examples_per_pattern:
                                examples[key].append(text[:240])

    print(f"scope: root={args.root} days={args.days} files={scanned_files} prompts={scanned_prompts}")
    print("\npatterns:")
    for key, value in counts.most_common():
        print(f"- {key}: {value}")

    print("\nexamples:")
    for key, items in examples.items():
        print(f"\n## {key}")
        for item in items:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
