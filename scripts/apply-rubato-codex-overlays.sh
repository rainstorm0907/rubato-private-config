#!/usr/bin/env bash
# 개인 스킬 오버레이(overlays/skills)를 rubato-codex 플러그인 캐시와 격리 프로필 AGENTS.md에 얹는다.
# apply-rubato-overlays.sh의 Codex 짝. rubato-codex를 다시 설치하면 캐시가 지워지므로 그 뒤 다시 돌린다.
# 원본(저장소·~/.agents/skills·공개 Rubato)은 읽기만 한다.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
codex_home="${RUBATO_CODEX_HOME:-$HOME/.codex}"
cache="$(find "$codex_home/plugins/cache" -type d -path '*/rubato-codex/*/skills' 2>/dev/null | head -1)"
[[ -n "$cache" && -d "$cache" ]] || { echo "rubato-codex plugin cache not found under $codex_home" >&2; exit 2; }

[[ "${1-}" == "--apply" ]] || { echo "dry run; pass --apply to write. target: $cache"; }

# 통째로 덮는 스킬: 원본 폴더 → 플러그인 이름. 본문의 metaFrame 참조는 Codex 스킬 이름 metaframe으로.
whole=(
  "codex-discusser:codex-discusser"
  "metaFrame:metaframe"
  "product-framing:product-framing"
  "product-reframing:product-reframing"
  "frontend-ux-router:frontend-ux-router"
)

rewrite() {  # $1 파일: 이름 필드와 백틱 참조만 바꾼다
  local f="$1"
  python3 - "$f" <<'EOF'
import re, sys, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text(encoding="utf-8")
t = t.replace("name: metaFrame\n", "name: metaframe\n").replace("`metaFrame`", "`metaframe`")
p.write_text(t, encoding="utf-8")
EOF
}

for pair in "${whole[@]}"; do
  src="$root/overlays/skills/${pair%%:*}"; dst="$cache/${pair##*:}"
  [[ -f "$src/SKILL.md" ]] || { echo "missing overlay: $src" >&2; exit 2; }
  if [[ "${1-}" == "--apply" ]]; then
    rsync -a --delete --exclude .rubato-private-overlay "$src/" "$dst/"
    while IFS= read -r -d '' f; do rewrite "$f"; done < <(find "$dst" -name '*.md' -print0)
    printf 'managed by rubato-private-config (codex overlay)\n' > "$dst/.rubato-private-overlay"
    echo "overlaid $dst"
  else
    rsync -ani --delete --exclude .rubato-private-overlay "$src/" "$dst/" | grep -v '^\.d' | sed "s|^|${pair##*:}: |" || true
  fi
done

# dispatching: 플러그인 판(Codex 런타임 줄 포함)을 유지하고 Open variables 항목·회신 칸만 얹는다.
dispatch="$cache/dispatching/SKILL.md"
if [[ "${1-}" == "--apply" ]]; then
  python3 - "$dispatch" "$root/overlays/skills/dispatching/SKILL.md" <<'EOF'
import sys, pathlib, re
dst = pathlib.Path(sys.argv[1]); src = pathlib.Path(sys.argv[2])
t = dst.read_text(encoding="utf-8"); s = src.read_text(encoding="utf-8")
if "- Open variables:" in t:
    print("dispatching: already has Open variables"); sys.exit(0)
ov = next(l for l in s.splitlines() if l.startswith("- Open variables:"))
ret = next(l for l in s.splitlines() if l.startswith("If the brief contains Open variables"))
lines = t.split("\n"); out = []
for l in lines:
    out.append(l)
    if l.startswith("- Frozen items:"): out.append(ov)
t2 = "\n".join(out)
anchor = next(l for l in lines if l.startswith("The return contract has a fixed column"))
t2 = t2.replace(anchor, anchor + "\n\n" + ret, 1)
dst.write_text(t2, encoding="utf-8"); print("dispatching: Open variables added")
EOF
else
  grep -q "^- Open variables:" "$dispatch" && echo "dispatching: up to date" || echo "dispatching: would add Open variables"
fi

# AGENTS.md: 기존 담당 연결·스탠스 줄의 스킬 이름을 Codex 이름(metaframe)으로 맞추고, 관리 표식 밖에 개인 블록을 한 번만 둔다.
agents="$codex_home/AGENTS.md"; block="$root/global/codex/rubato-codex-personal-block.md"
start="<!-- >>> rubato-private-config personal block >>> -->"; end="<!-- <<< rubato-private-config personal block <<< -->"
if [[ "${1-}" == "--apply" ]]; then
  python3 - "$agents" "$block" "$start" "$end" <<'EOF'
import sys, pathlib
a = pathlib.Path(sys.argv[1]); b = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8").rstrip("\n")
start, end = sys.argv[3], sys.argv[4]
t = a.read_text(encoding="utf-8") if a.exists() else ""
t = t.replace("`metaFrame`", "`metaframe`")
new = f"{start}\n{b}\n{end}\n"
if start in t and end in t:
    pre, rest = t.split(start, 1); _, post = rest.split(end, 1)
    t = pre + new.rstrip("\n") + post
else:
    t = t.rstrip("\n") + "\n\n" + new
a.write_text(t, encoding="utf-8"); print("AGENTS.md: personal block written")
EOF
else
  grep -q "$start" "$agents" 2>/dev/null && echo "AGENTS.md: block present" || echo "AGENTS.md: would add block"
fi
