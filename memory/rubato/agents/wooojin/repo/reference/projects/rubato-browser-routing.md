---
description: Rubato browser work follows the official browser-cli and aside skills. The personal builds (abrowse/gbrowse/isearch) were removed on 2026-09-29.
---
# Rubato browser routing

- 2026-09-29, Woojin: "브라우저는 공식으로 가보자." The personal browser-cli overlay (abrowse/gbrowse/isearch, exit-code judgment) was removed, and the official `browser-cli` and `aside` skills are used.
- Grounds: an Opus and Astra xhigh review. Both granted that the local tools were useful, but Astra pointed out that exit-code judgment does not prove an actual visit (it counts the tool name) and that the wrapper runs with the permission check off.
- The scripts remain in `~/.agents/skill-backups/20260929T070651Z-personal-overlays/browser-cli/scripts/` and in the rubato-private-config git history (before 3b82cf3). To use them again, attach them as an optional adapter under the official router.
- Official browser-cli uses cloak (9333/9334) and chrome-devtools as fallbacks, and this Mac does not have them. If it actually gets blocked, decide the fallback then.
