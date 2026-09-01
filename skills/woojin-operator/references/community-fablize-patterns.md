# Community Fableize Patterns

Use this reference when Woojin asks to strengthen `woojin-operator` using public Fableize/fablize/Qwable-style community work, or when the goal is to make a non-Fable model work with less flailing through procedure, evidence, and escalation rather than persona imitation.

## Sources Checked

Refreshed 2026-07-10.

- `fivetaku/fablize` GitHub repo, README and plugin files: `https://github.com/fivetaku/fablize`
- `fablize` local clone inspected at `/tmp/fablize` during initial review.
- Anthropic Fable docs: `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5`
- Anthropic Fable product page: `https://www.anthropic.com/claude/fable`
- OpenAI Codex manual, especially multi-agent model choice, AGENTS.md, prompting, and skills: `https://developers.openai.com/codex/codex-manual.md`
- OpenAI GPT-5.6 Sol announcement: `https://openai.com/index/previewing-gpt-5-6-sol/`
- Hugging Face Qwable model cards/discussions, including `lordx64/Qwable-v1`, `lordx64/Qwable-v2`, and related Fable-trace contribution discussions.

## Core Finding

The useful community consensus is conservative:

- A harness should transfer the work loop first, then discover any capability ceiling through evidence.
- The transferable part is procedure: finish the task, ground claims in observed evidence, reproduce/debug systematically, and refuse completion without proof.
- The non-transferable part is autonomous depth: self-started implication chasing, open-ended creative detail, and out-of-spec defect discovery.

For Woojin's operator, this means: encode the work loop, not the persona.

For frontier models, keep even that loop proportional. Official Fable guidance says older skills can be too prescriptive, while the Codex manual recommends `gpt-5.6` for demanding agents and lighter models for bounded supporting work. Let the frontier model own the integrated task; use skills, subagents, and review for specialized knowledge, parallel evidence, or real risk rather than as universal ceremony.

## Capability-Adaptive Mode

Follow SKILL.md `Capability Principle` and `Proportional Scaffolding` as the SSOT. Procedure transfers better than persona, but no provider or model should be treated as a weaker imitation by default. Discover capability limits through observed results.

## Import Into Woojin Operator

### 1. Completion Integrity

Follow SKILL.md `Completion Integrity` as the SSOT. Do not redefine a mandatory output template here.

### 2. Verification Grounding

If the output can look or behave wrong only when run, run and observe it before calling it done:

- web/UI: browser screenshot, console check, responsive viewport if relevant
- iOS/macOS UI: simulator/device screenshot or video when practical
- chart/image/card: render the actual image/PDF/PNG and inspect it
- script/CLI: execute with representative input and capture output

Static syntax checks are not enough for visual or executable artifacts.

### 3. Investigation Options

When debugging or diagnosing an unknown or non-obvious cause, use as many of these moves as the evidence requires:

1. Reproduce or observe the failure first.
2. Name competing hypotheses when the cause is not already clear.
3. Gather evidence that confirms or rejects each.
4. Trace the full causal chain, not just the visible trigger.
5. Verify before and after the fix.
6. Report rejected hypotheses only when they help the user trust the fix.

If the root cause is obvious and low-risk, verify the direct fix without adding a hypothesis ritual.

### 4. Capability Ceiling Escalation

Escalate when evidence shows the current loop is no longer improving:

- repeated attempts produce the same failure without new evidence;
- the value is open-ended creative taste/detail and current outputs are flat;
- a review needs out-of-spec discovery that the current model is not finding;
- independent review contradicts the main agent and evidence is thin.

Possible escalation choices; select rather than mechanically following the list:

1. sharpen the evidence package;
2. increase reasoning effort or try a different model when task-specific evidence supports it;
3. ask a bounded independent reviewer/researcher;
4. hand off to a fresh-context solver or another model when the current approach has plateaued;
5. ask Woojin for taste/product judgment.

### 5. Personalization Layer

Woojin-specific additions beyond generic fablize:

- Preserve source-artifact boundaries and exact paths.
- Prefer Maplog product-gap reframing before code when the prompt uses feel/density/shareability language.
- Treat screenshots, videos, and local worklogs as first-class evidence.
- Keep mood/relationship sessions out of generic transcript analysis.
- Do not add always-on hooks from community plugins unless Woojin explicitly asks; use this as a skill-level routing discipline first.

## What Not To Import

Follow SKILL.md `External Pattern Guard` as the SSOT. In short: keep procedure-level learning open; keep leaked prompts, raw chain-of-thought, Fable traces, third-party transcript corpora, model distillation recipes/datasets, and "act as Fable" persona prompts out.

Hugging Face Qwable-style work is useful as a signal that agentic tool-use patterns may be teachable when the harness supplies an agent format, but the model cards themselves warn about narrow training distribution, benchmark uncertainty, provenance/licensing constraints, and system-prompt-conditioned behavior. Treat that as caution, not as a recipe for this personal operator.
