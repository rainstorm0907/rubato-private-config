# MapleStory HEXA skill delta workflow

When Woojin asks whether a new VI/HEXA skill should be opened or why it is late in `hexaOrder`, use `/Users/wooojin/dev/maple/kb/hexa-skill-workflow.md`.

Fast path:

1. Refresh the character snapshot when stale.
2. Run `node tools/growth-assistant.mjs skill <character> <skill>` to inspect the existing V core, active HEXA core, and recorded resources.
3. Compare the existing V/IV tooltip with the VI tooltip and remove repeated text. Never count the full VI tooltip as incremental damage.
4. Separate reprinted effects, true numerical additions, and structural interactions.
5. Verify class interactions with official notes plus focused class-board experiments.
6. Check the live Maplescouter `hexaOrder`; interpret a later rank as cheaper competing gains, not automatically as a bad core.
7. Give a conclusion first: open now, wait for order, or pull forward only for a specific burst/boss threshold.

Use current character resources and boss target for personalization. Stop once the existing-to-new delta, important interactions, live order, and resource constraint are known.
