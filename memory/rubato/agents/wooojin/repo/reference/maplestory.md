---
description: MapleStory character benchmarks, measurement tools, and research workflow.
---
MapleStory project facts. Moved from `~/.codex/memories`. Benchmark numbers are as of the measurement time, so they need rechecking.

## "레공레" ("레테")

- As of 2026-06-26, Lv276, EMERALD 30000 Challenger.
- A Chaos Gloom ("카오스 더스크") clear was not the initial estimate of 15:02 but about 5~6 minutes after the correction. The center 4:58 is not the boss timer but the 5-minute end timer after the clear.
- Hard Will can be cleared without a guide, but it is slow and a learning type. Next comparison candidates: Hard Darknell, Chaos Guardian Angel Slime, Hard Lucid, Hard Verus Hilla.
- Experience: 1 "소재" (30 min) ≈ 0.545~0.581% EXP. A Momentum Pass ("메카베리" 10 + "상급EXP9000") is about 160~171 "소재" / 80~85 hours. Converting 49,800 won at 1,600 won per 100 million gives 31.125 hundred million meso. Up to 30 hundred million is clearly acceptable; up to 35 hundred million is allowed for the purpose of saving time.
- "메카베리" fever has only the effect of removing the "슈피겔버스트" (Spiegel Burst) cooldown, not an EXP multiplier.

## "오렌지솥밥"

- Lv.282, combat power 70,409,457 as of 2026-06-25.
- Rough boss-ratio rule: the 110% range near-cut, the 120% range a clear that can allow mistakes, the 170% range damage enough (only gimmicks and fatigue are variables), 200%+ stable farming.
- Kalos/Adversary need gimmick and downtime weighting. If they say they are tired, hold off recommending a new gimmick boss.

## Measurement tools

- If Maplescouter browser access is blocked, query `https://api.maplescouter.com/api/id?name=<캐릭>&preset=00000` directly with an `api-key` header.
- Prefer Maplescouter converted stats, HEXA conversion, and boss stats over Nexon in-game combat power as the SSOT. Because of "정축여축"-style combat-power distortion.
- 2026-07-08 measurement: Black Mage estimate 89.97% → 97.2% after HEXA → about 99~103% (center 101%) after the legendary "심연 결계" (abyss barrier).
- Equipment-efficiency calculation has two modes. exact = API before/after delta + screenshot tooltip as hard evidence, decomposing stat components. rough = reuse recent ratios + a rough label + conclusion first.
- HEXA/VI skill delta: compare the existing V/IV tooltip with the VI tooltip and remove duplicate text. Do not count the whole VI tooltip as the increase. A late hexaOrder rank does not automatically mean a bad core; judge by the relative opportunity cost of competing cores.

## Research workflow

- Challenger server prices and opinion: lock the current state with `item-equipment.json` + `kb/branchpoints` → `latest_digest.sh` + `rg` in parallel → Arca.live/DCInside quiet-browse only (raw curl forbidden) → separate the premises of newbie / low-meso / untradable sunk ("교불 매몰") / finished product → separate shell price ("깡통가") and finished-product price.
- YouTube: transcripts and subtitles first. Open the video only when visual evidence at a specific timestamp is needed. When playing, always mute (`--mute-audio`), and use an isolated browser profile (Woojin's actual Chrome profile forbidden).
- A snapshot can be reused for about 14 days after a refresh. But the auction house, events, and weekly progress are checked fresh every time.
- Force KST with `formatSeoulTimestamp()`. `latest_digest.sh` keeps exit 1 when the browser fails — do not mistake a partial result for success.
