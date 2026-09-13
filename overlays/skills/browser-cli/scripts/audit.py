# Audit a gbrowse stream from the stream itself, never from what the model claims.
# Prints: <browser_calls> <errored_calls> <forbidden_calls> <last_url_the_browser_reported>
import json, re, sys

calls = errs = forbidden = 0
observed = "-"
for line in open(sys.argv[1], encoding="utf-8"):
    try:
        o = json.loads(line)
    except Exception:
        continue
    t = o.get("type")
    if t == "tool_call":
        if o.get("toolName") not in ("search_tool", "use_tool"):
            forbidden += 1
        if "aside" in (o.get("rawInput") or {}).get("tool_name", ""):
            calls += 1
    elif t == "tool_call_update":
        ro = o.get("rawOutput") or {}
        if ro.get("type") == "MCP":
            if ro.get("is_error"):
                errs += 1
            out = json.dumps(ro.get("output", ""), ensure_ascii=False)
            for u in re.findall(r'https?://[^\s"\\,)\]]+|about:blank|chrome-error://\S*', out):
                observed = u
print(calls, errs, forbidden, observed)
