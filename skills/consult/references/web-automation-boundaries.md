# Aside Web Automation Boundaries

Consult uses the user's local logged-in Aside browser and `aside repl` only.

## Required

- Inventory open Aside tabs before opening ChatGPT.
- Open one task-owned ChatGPT tab and keep its target ID distinct from the baseline.
- Start every new conversation from the configured project URL, and confirm the unique project id in the live page URL — never the display name — before attaching any file.
- Verify personal `Chat`, the Pro account, `GPT-5.6 Sol`, and the requested reasoning level before sending.
- Copy the local packet into the ephemeral Aside session directory before browser upload. Do not expose arbitrary local filesystem paths to the page.
- Confirm upload and send through fresh snapshots.
- Publish the submission checkpoint the moment the conversation URL exists, before any waiting begins.
- Capture response text, visible response links, conversation URL, model evidence, and timestamps.
- Close only the task-owned tab, and only after completed collection, dry-run, or a pre-send failure. After accepted `--send-only`, failed collection, or partial collection, leave that tab open, record its target ID, and reuse it on `--resume` so in-flight generation is not interrupted.
- Treat cleanup as ownership-based: never close a baseline user tab, and consider a deliberately preserved owned tab valid rather than a baseline-restore failure.

## Forbidden

- Sending a second time for a conversation that is already on record. A failed capture is resumed, never resubmitted.
- Falling back to the personal chat root when the configured project cannot be confirmed.
- Deleting, moving, or archiving any existing ChatGPT conversation.
- Navigating or closing user-owned tabs.
- ChatGPT Work unless the user explicitly changes this skill's usage policy.
- Cookies, local storage, access-token, OAuth-token, or network credential extraction.
- API or private endpoint calls used as a substitute for the visible ChatGPT UI.
- CAPTCHA, MFA, login, rate-limit, or access-control bypass.
- Sending secrets or unrelated private content.
- Reporting an answer when the requested model or reasoning level was not verified.

Aside session files are ephemeral. The local runner must save the response and evidence under `.consult/` before the REPL exits.
