---
description: Woojin's lasting preference that a background or other session keep going safely instead of stopping because of a network error.
---
## Session continuity after a network error

- Status: user-confirmed preference, implemented and verified in Rubato.
- Implementation: a transport error after text/thinking/an ordinary agent toolCall is handed to the engine's existing limited retry, and `rubato:no-turn-retry:` is kept only when the provider has already run the tool, as with the Cursor exec-channel. **After the engine replacement, this marker's prefix changed from `senpi:` to `rubato:`** (`harness/rubato-pi/src/rubato-stream.mjs`, `pi-runtime/features/providers/auth-pool/classify.mjs`).
- Symptom: On 2026-09-01, after reporting that `senpi:no-turn-retry:WebSocket error` was stopping other sessions, Woojin: "이건 자꾸 왜 써서 다른 세션 멈추는거야?"
- Reading: Does not want an internal safety marker to end the session as a terminal error as it stands. Even if the network drops after partial output, duplicate tool runs must be blocked, while a safe session must continue or recover without parent intervention.
