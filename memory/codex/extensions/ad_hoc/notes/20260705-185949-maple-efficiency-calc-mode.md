# MapleStory equipment efficiency calculation mode

When Woojin asks for exact meso-per-efficiency calculations in MapleStory gear consulting, use the precise mode:

- Refresh or use the current character snapshot when available.
- Prefer API before/after deltas and the user's screenshots as the concrete source of changed stats.
- Break the upgrade into stat components when possible, such as attack/magic attack, boss damage, main stat, all stat %, potential, starforce, set effect, and symbol effect.
- Convert each component into main-stat-equivalent using the character's current Maplescouter/spec-efficiency coefficients when available.
- Report total combat power increase, approximate damage/final-damage increase, cost, and efficiency per 100m/1b mesos.
- Mark decomposition as approximate when Maplescouter's internal formula is not directly available, while treating API deltas and screenshot tooltip increases as the hard evidence.

When Woojin explicitly asks for a fast or rough answer, use the rough mode:

- Do not over-research or fully decompose each stat.
- Reuse the most recent calculation ratio for that character when reasonably current.
- Estimate quickly from prior combat power/damage ratio, screenshot tooltip increase, or known recent upgrade efficiency.
- Clearly label it as rough and give the actionable buy/skip/order recommendation first.
