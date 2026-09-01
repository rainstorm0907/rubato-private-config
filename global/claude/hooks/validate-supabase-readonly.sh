#!/bin/bash
# PreToolUse gate for mcp__supabase__execute_sql — read-only enforcement.
#
# supabase-reader is meant to inspect a live database, and the MCP connection it
# uses has write capability. The agent prompt already says SELECT/WITH only, but
# a prompt is not a control: this hook is the one that actually holds when a
# brief is ambiguous or the model drifts. Blocks anything that is not a plain
# read, including reads with a writing CTE.
#
# Contract: stdin is the tool-call JSON. Exit 0 allows, exit 2 blocks with the
# stderr text shown to the agent.

set -uo pipefail

input=$(cat)

query=$(printf '%s' "$input" | python3 -c '
import json, sys
try:
    payload = json.load(sys.stdin)
except ValueError:
    sys.exit(0)
print((payload.get("tool_input") or {}).get("query") or "")
' 2>/dev/null)

[ -z "$query" ] && exit 0

# Strip line/block comments and string literals before matching, so a keyword
# inside a comment or a quoted value cannot trip the gate, and a real statement
# cannot hide behind one.
stripped=$(printf '%s' "$query" | python3 -c '
import re, sys
sql = sys.stdin.read()
sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
sql = re.sub(r"--[^\n]*", " ", sql)
sql = re.sub(r"\$\$.*?\$\$", " ", sql, flags=re.S)
sql = re.sub(r"'"'"'(?:[^'"'"']|'"'"''"'"')*'"'"'", " ", sql)
sql = re.sub(r"\s+", " ", sql)
print(sql.strip().upper())
')

first_word=${stripped%% *}
case "$first_word" in
  SELECT|WITH|EXPLAIN|SHOW|TABLE|VALUES) ;;
  *)
    echo "차단: execute_sql 은 읽기 전용이다. '$first_word' 로 시작하는 문장은 실행하지 않는다. 조회로 다시 쓰거나 오케스트레이터에 보고할 것." >&2
    exit 2
    ;;
esac

# A WITH/EXPLAIN prefix does not make a statement read-only — writing CTEs and
# EXPLAIN ANALYZE both execute for real.
if printf '%s' "$stripped" | grep -qE '\b(INSERT|UPDATE|DELETE|MERGE|UPSERT|TRUNCATE|CREATE|ALTER|DROP|RENAME|GRANT|REVOKE|COMMENT ON|CALL|DO|COPY|VACUUM|REINDEX|CLUSTER|LOCK|SET |RESET |SECURITY LABEL)\b'; then
  echo "차단: 조회문 안에 쓰기·DDL·권한 구문이 있다 (writing CTE 또는 EXPLAIN ANALYZE 포함). 운영 데이터라 실행하지 않는다. 오케스트레이터에 보고할 것." >&2
  exit 2
fi

if printf '%s' "$stripped" | grep -qE '\bPG_(READ_FILE|READ_BINARY_FILE|LS_DIR|SLEEP|TERMINATE_BACKEND|CANCEL_BACKEND)\b|\bDBLINK\b|\bLO_(IMPORT|EXPORT)\b'; then
  echo "차단: 파일 접근·연결 조작 함수는 조회 범위 밖이다. 오케스트레이터에 보고할 것." >&2
  exit 2
fi

exit 0
