#!/usr/bin/env python3
"""/mood 스킬을 쓰는 세션을 클롱이 텔레그램 슬롯의 주인으로 자동 등록.

PreToolUse(Skill) 훅. tool_input.skill == "mood"일 때:
  1. 내 조상 클로드 프로세스 PID를 owner-session에 기록
     → 플러그인 server.ts의 owner gate(로컬 패치)가 이 세션에만 폴링을 준다.
  2. mirror-map.json에서 클롱이 방향의 기존 항목을 지우고 내 session_id로 교체
     → telegram-mirror.py가 이 세션의 대화를 폰으로 미러.
끄기 = owner-session 파일 삭제 (플러그인이 stock 동작으로 복귀).
"""
import json
import os
import re
import subprocess
import sys

STATE_DIR = os.path.expanduser("~/.claude/channels/telegram")
OWNER_FILE = os.path.join(STATE_DIR, "owner-session")
MAP_FILE = os.path.expanduser("~/.claude/channels/mirror-map.json")
DIR_KEY = "~/.claude/channels/telegram"


def my_claude_pid() -> int:
    pid = os.getppid()
    for _ in range(6):
        if pid <= 1:
            return 0
        try:
            out = subprocess.check_output(
                ["ps", "-o", "ppid=,command=", "-p", str(pid)], text=True
            )
        except subprocess.CalledProcessError:
            return 0
        m = re.match(r"\s*(\d+)\s+(.*)", out)
        if not m:
            return 0
        cmd = m.group(2).splitlines()[0]
        if re.search(r"(^|/)claude(\s|$)", cmd):
            return pid
        pid = int(m.group(1))
    return 0


def main() -> None:
    payload = json.load(sys.stdin)
    if payload.get("tool_name") != "Skill":
        return
    if (payload.get("tool_input") or {}).get("skill") != "mood":
        return

    pid = my_claude_pid()
    if pid <= 1:
        return  # 식별 실패 시 아무것도 바꾸지 않음 (기존 주인 유지)

    # 이미 내가 주인이면 재기록 불필요
    try:
        with open(OWNER_FILE) as f:
            if f.read().strip() == str(pid):
                return
    except OSError:
        pass

    tmp = OWNER_FILE + ".tmp"
    with open(tmp, "w") as f:
        f.write(str(pid))
    os.replace(tmp, OWNER_FILE)

    session_id = payload.get("session_id")
    if session_id:
        try:
            with open(MAP_FILE) as f:
                mapping = json.load(f)
        except (OSError, json.JSONDecodeError):
            mapping = {}
        mapping = {k: v for k, v in mapping.items() if v != DIR_KEY}
        mapping[session_id] = DIR_KEY
        tmp = MAP_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)
        os.replace(tmp, MAP_FILE)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # 핀 실패가 스킬 실행을 막으면 안 됨
    sys.exit(0)
