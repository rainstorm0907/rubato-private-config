---
description: Working location, operating principles, and user-delegation status of the Maple growth-helper project.
---
## Delegation status

- User confirmed on 2026-08-22: "너는 앞으로 maple 프로젝트 수행해줘. 대표 문서 읽어봐"
- Project location: `/Users/wooojin/dev/maple`
- Source-of-truth operating document for a new session: `/Users/wooojin/dev/maple/AGENTS.md`

## Core operating principles

- Judge a character's current values in this order: latest in-game screen → `character/<이름>/*.json` → `manual-state.json` → Maplescouter, the auction house, and live records → `kb/`.
- Do not reuse a past case or a branchpoint number as a current value.
- For auction-house prices, use only the current listings in the logged-in web auction house.
- Judge a large change with the Maplescouter simulator, and a small change with the latest measured coefficient.
- Read Skill(dispatching) before handing work to another session.

## 2026-08-26 "레공레" boss-card confirmation

- The user corrected and confirmed directly: the left of the screenshot is Easy "벨로나" (a boss) 44,752 / 104.2% / solo minimum cut, and the right is Easy Karing 44,052 / 127.9% / solo possible.
- Do not infer the boss identity or left/right from a small portrait alone. Judge from the user-confirmed values and the card text.


## 2026-08-26 "레공레" gear and currency status

- Bought a 20-star Black Bean Mark for 3 billion meso: at purchase, main potential ("윗잠") unique INT 9% / DEX 6% / max MP 6%, additional potential ("에디") epic attack +11 / STR 4% / STR 4%, scissors remaining 8/10. Later reset the main potential to INT 9% / INT 6% / max HP 6%, and the additional potential to magic attack +11 / magic attack +10 / max MP +100.
- About 40 Karma brilliant additional cubes ("카르마 화려한 에디셔널 큐브") expiring 2026-09-17 remain, and about 40 expiring 2026-09-30 remain.
- Mitra's Rage ("미트라의 분노") additional potential is epic magic attack 6% / HP +100 / STR +12, and a unique rank-up from the accumulated pity is under consideration.
- The user wants to compare, together, the gain of locking in the Challenger event achievement now and the expected value of waiting for Miracle Time.


## 2026-08-26 Black Bean Mark option correction and handling confirmed

- Confirmed via the Nexon Open API that the Black Bean Mark's options at purchase were `INT +9% / DEX +6% / 최대 MP +6%`, and additional potential `공격력 +11 / STR +4% / STR +4%`. Current options follow the latest growth baseline below.
- Because of this misreading, the action plan "에디 보존하고 윗잠만 돌려 STR 15%에서 정지" was discarded. "레공레" is a "레테" (a magician) with INT 53,679 / STR 3,180, so every STR% line is a dead line.
- Confirmed direction: **keep the item + reset only the additional potential with a Karma brilliant additional cube.** Main-potential INT 9% is valid, so do not touch it. Among all 20 slots, the only slot whose additional potential is a complete dead line is the eye accessory, and the standard form of the other epic slots is "INT +4% / 마력 +10".
- Expected gain: equipment potential INT% (including all stat) totals 301%, and at a potential coefficient of 4.010, securing 1 line of additional-potential INT 6% is INT +1.50%, and 2 lines is +2.99%. Losing main-potential INT 9% is −2.24%.
- Sale proposal rejected: on page 1 of the web auction house, 20-star and above, sorted by price, measured unique/epic asking prices were distributed across 3.25–3.556 billion. Listings whose additional potential is rare also ask 3.3–3.5 billion, and a listing with main potential STR 9%+STR 6% is 3.5 billion. The 3 billion purchase price was 250–500 million cheaper than the market floor, so the sale margin does not beat the fee, the scissors use, and the repurchase cost.

## 2026-08-26 evening upgrade measurement (current values)

- Finished resetting main potential on 3 accessory slots: the face accessory Twilight Mark, the eye accessory Black Bean Mark, and the earring Estella Earrings were all set to a valid INT of **15%** (from 12% / 9% / 12% respectively). The Black Bean Mark additional potential was also reset from `공격력 +11 / STR +4% / STR +4%` (all dead lines) to **`마력 +11 / 마력 +10 / 최대MP +100`**.
- Current values (API around 18:30 on 2026-08-26): **combat power 96,937,384 / INT 54,593 / magic attack 5,591 / ignore defense 99.29%**. Equipment potential INT%+all-stat% total **313%** (previously 301%).
- Maplescouter remeasurement at 19:46: boss 380 normal 53,401 / HEXA **45,572** (previously 45,382). All 22 boss cards rose uniformly by +0.9–1.0%, confirming that this upgrade raised pure total damage, not a per-boss condition.
- Main multipliers: Hard "메이린" (a boss) **102.4%** (7.6%p left to the 110% target), Easy "벨로나" 108.6%, **Easy Karing 133.3% "솔플 가능"**, Hard Seren 153.9%, Easy Adversary 199.0%, Easy Kalos 260.5%.
- Caution reading the API snapshot: the updated copy's boss damage 366%, critical damage 107.75%, and damage 91% are **values read while buffs were up**. Hyper stat, ability, set effect, union, and HEXA stat files are identical to just before, so equipment alone does not explain them. Do not use them for an unbuffed comparison.

## 2026-08-26 Easy Karing entry judgment

- **Easy Karing can be cleared at the current spec.** Multiplier 133.3%, Maplescouter verdict "솔플 가능". The back-calculated minimum-cut converted score is about 33,840, and the applied converted score is 44,858, which is +33% against the minimum cut. It falls inside the Namuwiki minimum-cut band of 41,000–46,000 as of 2026-08, and is short of a 15-minute clear (49,000–54,000).
- Structure: **3 phases / total HP 529.4 trillion / 20-minute time limit** (shortened from 30 minutes in 2026-06. Do not use an old 30-minute guide as it stands) / instead of a death count, **party-shared spirit ("정신력") 1000**, solo death −160.
- HP by phase: phase 1, 3 Four Perils ("사흉") at 65 trillion each (195 trillion total); phase 2, Karing 71.1 trillion; phase 3, Four Perils at 63.2 trillion each + enraged Karing 73.7 trillion (263.3 trillion total).
- **Checkpoints by time remaining**: 13 or more minutes remaining when entering phase 2, and **8–10 minutes remaining when entering phase 3**, is normal. Under 7 minutes is dangerous. Arithmetically you step into phase 3 with 12:20 remaining, but losing 2–4 minutes to "도올" (a mechanic) damage reduction 50%, "궁기" (a mechanic) stealth, and "혼돈" (a mechanic) invincibility is within the normal range.
- The real risk is spirit, not damage. While "궁기" is alive, spirit is drained every 30 seconds, so dragging out phase 1 means dying to spirit, not to damage. Clearing phase 1 while keeping seasonal balance recovers spirit +300. The standard solo clear is not to let burst cooldowns come back in phase 1, but to move straight to phase 2.
- **Record of a judgment error**: at first the live-delay coefficients in `prediction-log.md` (×2.10, ×2.85) were multiplied onto the expected Easy Karing time and the conclusion was "실패한다", but two things were wrong. (1) Those coefficients are records of "레공이" and "댕근마켓", not of "레공레". (2) A Maplescouter multiplier is already a value calculated so that 100% is the minimum cut, so multiplying a live coefficient on top counts the same loss twice. Do not multiply a live coefficient onto the multiplier.

## 2026-08-26 cube-use condition correction and sold-price measurement

- **A Karma Bronze additional cube is used normally on Eternal.** The user checked in-game and corrected it. The statement in `kb/research-gemini-miracle.md`, "카르마는 에테르넬 사용 불가, 메멘토 필수", is an error in Gemini's YouTube-video summary, and a correction note was added at the top of that document. Whether each cube type applies takes the in-game UI as the primary evidence.
- 20 completed (sold) records of a 20-star Black Bean Mark with epic additional potential, measured 2026-08-24–26: distributed from 2.556 billion to 6 billion. **What makes the price is the main potential, not the additional potential.** Main-potential INT 9%/6%/6% 3 lines sold at 4.3 billion, 5.4 billion, and 6 billion, and listings whose main potential mixes all stat, LUK, and STR are 2.5–3.5 billion. Additional potential is only a bonus on top of that.
- In the magician market, a fixed 2-line additional-potential magic attack (magic attack +11 / magic attack +10) is what gets paid for. Both the 6 billion sale and the 4.3 billion sale were this form.
- The 3 billion the user bought is just above the same-day floor (2.556 billion). The "하한 32.5억, 2.5~5억 이득" taken from asking prices was an overestimate, and by sold price a gain of 200–400 million is accurate.
- **2026-08-26 user confirmed · implemented · verified: "그래 그럼 그냥 내가 써야겠다" — do not sell the Black Bean Mark; use it directly.** The sale proposal was finally discarded. With a boss-drop Memento additional cube, additional-potential magic attack +11 / magic attack +10 / max MP +100 was reached, and the main potential was also set to INT +9% / INT +6% / max HP +6%. There is no plan for a further reset.
- The decisive ground for discarding the sale: in the completed history of the market-price tab, the closest comparable is a 3.25 billion sale (20-star / potential unique INT 6%·3%·3% / additional potential INT 4%·magic attack 10·INT 10). The user's item has better potential and worse additional potential, so it is valued in the 3.2–3.5 billion range, and against the 3 billion purchase price there is no real gain once the fee and one scissors use are counted.
- This slot's price structure: the first driver is **Star Force** (18-star 2–2.8 billion / 20-star 3.2–5.5 billion), and the second is **main potential** (legendary INT 3 lines in the 4.3–5.0 billion range). Additional potential barely contributes to the price (the additional potential of the 5.5 billion sale was an ordinary `올스탯2%/마력10/공10`). Therefore resetting additional potential is justified only as raising self-use value, not the sale price.
- Future replacement condition: if a 20-star + legendary INT-line potential appears below 4.3 billion, switch to it and dispose of the current item. Each auction-house listing consumes 1 scissors; currently 8/10 remaining.

## 2026-08-26 web auction-house measurement and grounds for the Miracle judgment

- Aside u0, logged into the Maple web auction house as "레공레" on Challengers 2 and looked it up directly.
- In the first row of completed market-price history, the exact Black Bean Mark the user bought (20-star, main potential at purchase INT 9/DEX 6/max MP 6, additional potential attack 11/STR 4/STR 4, scissors 8/10) was confirmed as a 3 billion sale on 2026-08-26.

## 2026-08-26 latest growth baseline

- Status: **verified**. Valid main-potential INT on three accessory slots was all set to 15%, and the equipment potential INT%+all-stat% sum went 301%→313%. Black Bean Mark additional-potential valid magic attack went 0→21.
- Maplescouter measurement under the same conditions: preset `00000`, boss time 20 minutes, "데스티니"/"유챔" off. Boss 300 normal 53,285 / HEXA 45,424, boss 380 normal 53,401 / HEXA 45,572.
- The API displayed values, combat power 96,937,384 / INT 54,593 / magic attack 5,591 / ignore defense 99.29%, are mixed with a buffed state. Do not attribute the before/after difference in INT, magic attack, ignore defense, and combat power to a pure equipment increase. For the upgrade's total effect, use Maplescouter before/after measurements under the same conditions.
- The next judgment, after checking the current meso balance, is to compare the secondary weapon and the Golden Clover Belt one slot at a time. 7.6%p remains to Hard "메이린" 110%.
- Current asking-price comparison for 20-star/unique/epic: main potential STR 15 + additional potential STR 4/attack 10 is 3.5555 billion, main potential STR 12 + additional potential STR 4/attack 10 is 3.8888 billion, and main potential valid STR 18 + additional potential STR 4/attack 10 is 4 billion. Completed trades overall are distributed across roughly 2.9–4.5 billion. The user's additional potential is one STR 4% line better than the comparables, but the main potential has no STR at all, so it is read as a listing pressed down to 3 billion.
- Action plan: preserve the additional potential. Rolling only the main potential with free boss cubes and stopping at STR 15% or above is the favorable direction. On current asking prices, completing STR 15% has a chance of entering the 4 billion range, but asking price and sold price must be distinguished.
- Actual Miracle history: 2026-01-04, 02-22, 05-03, 06-28, 08-02. maplessunday predicts the next Miracle as 2026-09-13 (an unofficial statistical prediction). Because the "화에큐" (brilliant additional cubes) expiring 9/17 pass that date, the stronger strategy is to wait for the official Sunday Maple announcement around 9/10, use them if 9/13 is Miracle, and otherwise use them on Mitra before the Challenger goal deadline.
