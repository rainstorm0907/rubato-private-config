# MapleStory Maplescouter tooling note - 2026-07-08

Context: During the `레공레` 2026-07-08 legendary `심연의 결계의 핵` check, browser-based Maplescouter measurement had tool friction. This note records the workaround so future MapleStory consulting does not repeat the same search path.

## Tool issues observed

- Chrome/extension browser was approved by the user, but the extension browser surface was unavailable with `Browser is not available: extension`.
- In-app/browser rendering of Maplescouter was slower/noisy enough that relying on visual page interaction was not the best path.
- The correct durable route was not UI scraping but direct Maplescouter API access.

## Working solution

- Download or inspect Maplescouter Next.js chunks from `https://maplescouter.com/ko/result?name=레공레&preset=00000`.
- The API base and key were found in a JS chunk:
  - base: `https://api.maplescouter.com`
  - endpoint: `/api/id`
  - query: `name=<character>&preset=00000`
  - header: `api-key: [redacted]`

Reusable command:

```bash
curl -s \
  -H 'api-key: [redacted]' \
  -H 'Content-Type: application/json' \
  'https://api.maplescouter.com/api/id?name=%EB%A0%88%EA%B3%B5%EB%A0%88&preset=00000' \
  -o /tmp/maplescouter_legongre.json
```

Useful JSON paths:

```bash
jq '{
  boss300_stat:.calculatedData.boss300_stat,
  boss380_stat:.calculatedData.boss380_stat,
  boss300_hexaStat:.calculatedData.boss300_hexaStat,
  boss380_hexaStat:.calculatedData.boss380_hexaStat,
  exchangePower:.calculatedData.exchangePower,
  exchangePowerHexa:.calculatedData.exchangePowerHexa,
  hexaUsed:.calculatedData.hexaUsed
}' /tmp/maplescouter_legongre.json
```

## 2026-07-08 measured anchor

- Character: `레공레`, Lv280 `레테`, Challenger World 2.
- Current Maplescouter API values:
  - `boss300_stat`: `39347`
  - `boss380_stat`: `38899`
  - `boss300_hexaStat`: `31624`
  - `boss380_hexaStat`: `31264`
  - `exchangePower`: `63243589.15541312`
  - `exchangePowerHexa`: `38886323.44397476`
  - `hexaUsed`: `[64,1428]`

## Interpretation rules to reuse

- For `레공레`, do not trust Nexon API/in-game combat power as the main SSOT because prior notes identify Lete/정축여축-style combat-power distortion. Use Maplescouter 환산/헥환/boss stat first.
- For same-boss updates, use the existing KB rule: `updated boss ratio ~= previous ratio * (1 + final damage/stat gain)` only when measurement conditions are comparable.
- For the 2026-07-08 check, the practical conclusion was: old Black Mage estimate `89.97%` -> after HEXA stat `~97.2%` -> after legendary abyss core and follow-up measured growth `~99-103%`, center around `~101%`.

## Workspace records created

- `/Users/wooojin/dev/maple/kb/branchpoints/2026-07-08-legongre-abyss-core-legend.md`
- `/Users/wooojin/dev/maple/kb/prediction-log.md`
