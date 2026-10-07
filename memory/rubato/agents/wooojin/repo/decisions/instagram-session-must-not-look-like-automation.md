---
description: Do not call Instagram with Woojin's logged-in session in a way that looks like automation. Stories go through a real browser page, and the keychain stays untouched.
---

## Conclusion

- Do not fetch Instagram media by calling private endpoints with Woojin's logged-in session, and do not pull Chrome cookies or the keychain to do it. That pattern nearly locked the account `wuujeans`.
- Posts may be received logged-out from the public page. Stories and highlights, if tried again, go through a real browser page inside Scriptable, with the requests sent from that page, and only after he asks. Do not resume the private-API shortcut.

## Rationale

- Chose a real browser page over a half-fake client that lifts a token and then calls the API itself. He picked Scriptable and told the session to be careful with calls and with the keychain.
- Rejected: a lightweight shortcut that reused a saved login and polled the API. The warning screen came after that design, and the session treated the bot-like call pattern as the cause worth not repeating.
- The account recovery itself was his. Do not treat a later "fix my Instagram" request as permission to log in, change the linked email, or hammer the API again.

## Symptom

야 내 인스타 정지먹을뻔 했는데 너 때문이야..?

그럼 진짜 브라우저 식으로 쓰는 방식으로 해보는게 어때..?

Scriptable 로 ㄱㄱ 이번엔 과정에서도 호출 조심해서 완성해

키체인같은거 접근 조심해서 ㄱㄱ
