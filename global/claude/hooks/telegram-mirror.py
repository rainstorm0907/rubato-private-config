#!/usr/bin/env python3
"""cmux 텔레그램 매핑 세션의 대화를 폰으로 미러링.

UserPromptSubmit: 노트북에서 친 프롬프트를 💻 접두어로 전송.
Stop: 턴의 마지막 어시스턴트 텍스트를 🤖 접두어로 전송.

TELEGRAM_STATE_DIR가 없는 세션(매핑 안 된 pane, 일반 터미널)은 아무것도 안 함.
세션이 reply 툴로 직접 답장한 턴은 중복 방지를 위해 건너뜀.
"""
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

CHAT_ID = "7389033218"
MAX_LEN = 3900


def send(token: str, text: str, parse_mode: str | None = None) -> None:
    if parse_mode is None and len(text) > MAX_LEN:
        text = text[:MAX_LEN] + "\n…(생략)"
    fields = {"chat_id": CHAT_ID, "text": text}
    if parse_mode:
        fields["parse_mode"] = parse_mode
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage", data=data
    )
    resp = urllib.request.urlopen(req, timeout=5)
    if os.environ.get("MIRROR_DEBUG"):
        print(f"sent: {resp.status}", file=sys.stderr)


def dedup_ok(state_dir: str, text: str) -> bool:
    """같은 텍스트 재전송 방지 (--resume 직후 Stop 재발화 등)."""
    marker = os.path.join(state_dir, "mirror.last")
    digest = hashlib.sha256(text.encode()).hexdigest()
    try:
        with open(marker) as f:
            if f.read().strip() == digest:
                return False
    except OSError:
        pass
    with open(marker, "w") as f:
        f.write(digest)
    return True


def last_turn_texts(transcript_path: str):
    """마지막 사용자 프롬프트 이후의 어시스턴트 텍스트와 reply 툴 사용 여부."""
    entries = []
    with open(transcript_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    last_user = -1
    for i, e in enumerate(entries):
        if e.get("type") != "user" or e.get("isMeta"):
            continue
        content = (e.get("message") or {}).get("content")
        is_prompt = isinstance(content, str) or (
            isinstance(content, list)
            and any(
                isinstance(b, dict) and b.get("type") == "text" for b in content
            )
        )
        if is_prompt:
            last_user = i

    texts, replied = [], False
    for e in entries[last_user + 1 :]:
        if e.get("type") != "assistant":
            continue
        for b in (e.get("message") or {}).get("content") or []:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "text" and b.get("text", "").strip():
                texts.append(b["text"])
            elif b.get("type") == "tool_use":
                name = b.get("name") or ""
                if "telegram" in name and "reply" in name:
                    replied = True
    return texts, replied


def main() -> None:
    payload = json.load(sys.stdin)
    state_dir = os.environ.get("TELEGRAM_STATE_DIR")
    if not state_dir:
        # cswap/플러그인 경로로 뜬 세션은 env가 없음 — 세션 ID 핀 매핑으로 폴백
        try:
            with open(os.path.expanduser("~/.claude/channels/mirror-map.json")) as f:
                state_dir = json.load(f).get(payload.get("session_id") or "")
        except (OSError, json.JSONDecodeError):
            return
    if not state_dir:
        return
    state_dir = os.path.expanduser(state_dir)
    env_path = os.path.join(state_dir, ".env")
    token = None
    try:
        with open(env_path) as f:
            for line in f:
                if line.startswith("TELEGRAM_BOT_TOKEN="):
                    token = line.strip().split("=", 1)[1]
                    break
    except OSError:
        return
    if not token:
        return

    event = payload.get("hook_event_name")

    if event == "UserPromptSubmit":
        prompt = (payload.get("prompt") or "").strip()
        if not prompt:
            return
        if prompt.startswith("/"):  # 로컬 슬래시 커맨드는 미러 안 함
            return
        if "<channel " in prompt and "source=" in prompt:  # 폰발 메시지 에코 방지
            return
        if prompt.startswith("<task-notification>"):
            # 백그라운드 작업 알림: XML 태그 노이즈 없이 요약 한 줄 + 접힌 결과만
            sm = re.search(r"<summary>(.*?)</summary>", prompt, re.S)
            rm = re.search(r"<result>(.*?)(?:</result>|$)", prompt, re.S)
            label = (sm.group(1) if sm else "백그라운드 작업 알림").strip()
            msg = f"<i>⚙️ {html.escape(label)}</i>"
            body = (rm.group(1) if rm else "").strip()
            if body:
                if len(body) > 3400:
                    body = body[:3400] + "\n…(생략)"
                msg += f"\n<blockquote expandable>{html.escape(body)}</blockquote>"
            send(token, msg, "HTML")
            return
        if re.match(r"<(system-reminder|command-name|local-command|teammate-message)\b", prompt):
            return  # 하네스가 주입한 시스템 텍스트는 미러 안 함
        if len(prompt) > 3500:
            prompt = prompt[:3500] + "\n…(생략)"
        # 노트북에서 친 프롬프트는 인용구 스타일로 구분 (이모지 대신)
        send(token, f"<blockquote>{html.escape(prompt)}</blockquote>", "HTML")
    elif event == "Stop":
        tp = payload.get("transcript_path")
        if not tp or not os.path.isfile(tp):
            return
        # 트랜스크립트 플러시 지연 대비: 두 번 연속 같은 내용이 읽힐 때까지 대기
        # (마지막 어시스턴트 텍스트가 아직 안 써진 시점에 읽으면 직전 텍스트를 오발송)
        texts, replied = last_turn_texts(tp)
        for _ in range(6):
            time.sleep(0.5)
            texts2, replied2 = last_turn_texts(tp)
            if (texts2, replied2) == (texts, replied):
                break
            texts, replied = texts2, replied2
        if replied or not texts:
            return
        text = "🤖 " + texts[-1]
        if dedup_ok(state_dir, text):
            send(token, text)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)  # 미러 실패가 세션을 방해하면 안 됨
