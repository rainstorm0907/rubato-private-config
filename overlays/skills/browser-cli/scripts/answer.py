# The terminal answer is the text emitted after the last tool call; everything before it is
# inter-step narration, which is why the CLI's concatenated .text field cannot be trusted.
import json, sys

buf = []
for line in open(sys.argv[1], encoding="utf-8"):
    try:
        o = json.loads(line)
    except Exception:
        continue
    t = o.get("type")
    if t == "tool_call":
        buf = []
    elif t == "text":
        buf.append(o.get("data", ""))
print("".join(buf).strip())
