const NEEDLE =
  "    const liveContextTokens = hasExistingSession\n" +
  "        ? existingSession.messages.reduce((total, message) => total + estimateTokens(message), 0)\n" +
  "        : 0;\n" +
  "    session.assertModelUsable(undefined, liveContextTokens);";

const REPLACEMENT =
  "    const liveContextTokens = hasExistingSession\n" +
  "        ? existingSession.messages.reduce((total, message) => total + estimateTokens(message), 0)\n" +
  "        : 0;\n" +
  "    try {\n" +
  "        session.assertModelUsable(undefined, liveContextTokens);\n" +
  "    }\n" +
  "    catch (error) {\n" +
  "        if (!hasExistingSession || liveContextTokens <= 0)\n" +
  "            throw error;\n" +
  "        session.assertModelUsable(undefined, 0);\n" +
  "        const recoveryMessage = \"Session history exceeds this model's safe context budget. Opened in recovery mode; run /compact before sending or switching models.\";\n" +
  "        modelFallbackMessage = modelFallbackMessage ? `${modelFallbackMessage}. ${recoveryMessage}` : recoveryMessage;\n" +
  "    }";

export function injectResumeRecovery(source) {
  if (source.includes("Opened in recovery mode; run /compact")) return source;
  const first = source.indexOf(NEEDLE);
  if (first < 0 || source.indexOf(NEEDLE, first + NEEDLE.length) >= 0) {
    throw new Error("Rubato private resume-recovery transform drift");
  }
  return source.slice(0, first) + REPLACEMENT + source.slice(first + NEEDLE.length);
}

export async function load(url, context, nextLoad) {
  const result = await nextLoad(url, context);
  if (!url.includes("@code-yeongyu/senpi/dist/core/sdk.js") || result.source == null) return result;
  return { ...result, source: injectResumeRecovery(String(result.source)) };
}
