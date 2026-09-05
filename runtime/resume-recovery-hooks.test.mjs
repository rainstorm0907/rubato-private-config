import assert from "node:assert/strict";
import test from "node:test";
import { injectResumeRecovery } from "./resume-recovery-hooks.mjs";

const source =
  "before\n" +
  "    const liveContextTokens = hasExistingSession\n" +
  "        ? existingSession.messages.reduce((total, message) => total + estimateTokens(message), 0)\n" +
  "        : 0;\n" +
  "    session.assertModelUsable(undefined, liveContextTokens);\n" +
  "after";

test("large persisted sessions retain a fixed-budget recovery gate", () => {
  const next = injectResumeRecovery(source);
  assert.match(next, /session\.assertModelUsable\(undefined, liveContextTokens\)/);
  assert.match(next, /session\.assertModelUsable\(undefined, 0\)/);
  assert.match(next, /Opened in recovery mode; run \/compact/);
  assert.equal(injectResumeRecovery(next), next);
});

test("unexpected Senpi source fails closed", () => {
  assert.throws(() => injectResumeRecovery("changed upstream"));
});
