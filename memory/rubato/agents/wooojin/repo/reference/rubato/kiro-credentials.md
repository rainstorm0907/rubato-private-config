---
description: The structural cause of credential-transfer failure when attaching a Kiro subscription to Rubato, and the correct transfer method.
---
# Transferring Kiro credentials

When attaching a Kiro subscription to rubato with `harness/scripts/kiro-setup.sh`, the reason a credential transfer between machines fails is almost always a missing `clientId`.

## Constraints confirmed by measurement (2026-08-26)

An IdC (`authMethod: idc`) credential cannot be used with a refreshToken alone. Refresh needs **the very clientId that issued that token**.

- Register a new public client at `oidc.us-east-1.amazonaws.com/client/register` (200 OK) and try a refresh with that clientId, and you get `400 invalid_grant: Invalid refresh token provided`. AWS has bound the refreshToken and the clientId together — no bypass.
- The accessToken carried in the file lasts 1 hour. Calling it directly after it expires gives `403 The bearer token included in the request is invalid`.

So an export file with no clientId **lives for only one hour right after it is received**, and then dies. That is why, even when verifying produces "모델 뜨고 응답 왔다", this defect is not caught.

## Where the clientId is

The token file has only `clientIdHash`, and the actual value is in **the file next to it**:

```
~/.aws/sso/cache/kiro-auth-token.json   ← clientIdHash만
~/.aws/sso/cache/<clientIdHash>.json    ← clientId, clientSecret
```

If export cannot find this pair, a half file comes out.

## The correct transfer method

Rather than pulling a single file with `export`, moving the cache directory whole from the source machine does not break the pair:

```bash
cd ~ && tar czf ~/Downloads/kiro-sso.tgz .aws/sso/cache
```

Unpack it on the receiving machine and run `kiro-setup.sh` (with no arguments).

## Reflecting it in the engine after attaching

Even if you pull the bridge source, **the running engine does not change on its own.** If `~/.rubato-pi/engine/` is stale, there is no `kiro/` provider and the model does not come up.

- `rubato restart` brings back **only the bridge (:8788)**. It does not touch the engine.
- The engine rebuild is what `rubato-pi.sh` calls **every time a session starts**. A new session and a resume take the same path, so closing the window and opening it again is enough.
- Judging whether it is stale: `node harness/scripts/build-engine.mjs --check` (0 fresh, 10 stale).

## Expiry structure (three layers)

| | Lifetime | When it expires |
|---|---|---|
| accessToken | 1 hour | kiro.rs refreshes it automatically — no need to worry |
| **clientId registration** | **90 days** | ⚠️ The real deadline. Refresh is blocked |
| refreshToken | no expiry field | effectively continues |

After 90 days, opening Kiro IDE once on the source machine re-registers it. You do not have to log in again.

**Unconfirmed risk**: if two machines share the same refreshToken, and AWS is using rotation, one side's refresh can invalidate the other. Unverified as of 2026-08-26.

## Traps easy to fall into

- **Running export on the receiving machine is a cycle.** export reads `~/.rubato-pi/kiro/credentials.json` first, so it reads again the broken file an earlier import made and reproduces the same defect.
- **Do not open the OAuth login link in a browser on another machine.** The callback returns to localhost, so it completes only on the machine that created the link. Opening it on another machine gives `ERR_CONNECTION_REFUSED`.
- `kiro-cli login` often times out on the OAuth callback. The Kiro IDE side is safer (a script comment).
