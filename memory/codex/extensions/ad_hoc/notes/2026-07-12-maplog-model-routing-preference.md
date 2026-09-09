# Maplog prompt model routing preference

Woojin explicitly requested that future implementation prompts begin with a concrete recommendation for which available model and reasoning effort should run that task.

Current evidence-based default:

- Use Claude Fable first for high-ambiguity, product-defining visual interaction prototypes where user intent, convenience, motion, and feel must be discovered and demonstrated.
- Use GPT-5.6 Terra with very high reasoning for integrating an approved interaction into the real Maplog repository, including persistence, data contracts, edge cases, performance, regression tests, QA evidence, and documentation.
- Do not run both against the same writable repository simultaneously. Keep Fable read-only or isolated, approve its rendered result, then hand the chosen mechanics to Terra for production integration.
- Routine, already-specified UI edits and non-visual implementation work can go directly to Terra without a Fable prototype.

This is an operating preference, not a claim that either model is universally superior. Choose per task and state the recommendation at the top of each prompt.
