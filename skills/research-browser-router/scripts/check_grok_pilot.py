#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate one terminal Grok harness run.")
    parser.add_argument("--output-dir", default=".research/grok")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--mission-id", default=None)
    parser.add_argument("--expect", action="append", default=[])
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    if args.run_id:
        run_dir = output_dir / "runs" / args.run_id
    else:
        latest_path = output_dir / "latest.json"
        if not latest_path.exists():
            print(json.dumps({"ok": False, "errors": ["latest.json missing"]}, ensure_ascii=False))
            return 1
        latest = read_json(latest_path)
        run_dir = Path(str(latest.get("runDir") or ""))
    done_path = run_dir / "done.json"
    run_path = run_dir / "grok-run.json"
    report_path = run_dir / "grok-report.md"
    errors: list[str] = []
    if not done_path.exists() or not run_path.exists():
        errors.append("terminal artifacts missing")
        print(json.dumps({"ok": False, "runDir": str(run_dir), "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    done = read_json(done_path)
    run = read_json(run_path)
    if done.get("state") != "complete":
        errors.append(f"state is {done.get('state')!r}, not 'complete'")
    if args.mission_id and run.get("missionId") != args.mission_id:
        errors.append(f"missionId mismatch: {run.get('missionId')!r}")
    if done.get("forbiddenTools"):
        errors.append(f"forbidden tools: {done.get('forbiddenTools')}")
    if done.get("protocolViolations"):
        errors.append(f"protocol violations: {done.get('protocolViolations')}")
    if done.get("orphanCheck") != "gone":
        errors.append(f"orphanCheck is {done.get('orphanCheck')!r}")
    if done.get("remoteAgentState") != "cli_exited":
        errors.append(f"remoteAgentState is {done.get('remoteAgentState')!r}")
    invariants = done.get("browserInvariants") or {}
    if not invariants.get("ok"):
        errors.append("browser invariants failed")
    report = report_path.read_text(encoding="utf-8", errors="replace") if report_path.exists() else ""
    if not report:
        errors.append("report missing")
    for pattern in args.expect:
        if not re.search(pattern, report, flags=re.MULTILINE):
            errors.append(f"missing expected report pattern: {pattern}")
    result = {
        "ok": not errors,
        "runId": done.get("runId"),
        "missionId": run.get("missionId"),
        "state": done.get("state"),
        "runDir": str(run_dir),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
