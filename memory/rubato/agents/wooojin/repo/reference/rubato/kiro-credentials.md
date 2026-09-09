---
description: Rubato에 Kiro 구독을 붙일 때 자격증명 이전이 실패하는 구조적 원인과 올바른 이전 방법.
---
# Kiro 자격증명 이전

`harness/scripts/kiro-setup.sh`로 Kiro 구독을 rubato에 붙일 때, 기기 간 자격증명 이전이
실패하는 원인은 거의 항상 `clientId` 누락이다.

## 실측으로 확인한 제약 (2026-08-26)

IdC(`authMethod: idc`) 자격은 refreshToken 하나로는 못 쓴다. 갱신에 **그 토큰을 발급한
바로 그 clientId**가 필요하다.

- 새 public client를 `oidc.us-east-1.amazonaws.com/client/register`로 등록해서(200 OK)
  그 clientId로 refresh를 시도하면 `400 invalid_grant: Invalid refresh token provided`.
  AWS가 refreshToken과 clientId를 묶어놨다 — 우회 불가.
- 파일에 실려온 accessToken은 1시간짜리다. 만료 뒤 직접 호출하면
  `403 The bearer token included in the request is invalid`.

즉 clientId 없는 export 파일은 **받은 직후 한 시간만 살아있고** 그 뒤 죽는다.
검증할 때 "모델 뜨고 응답 왔다"가 나와도 이 결함을 못 잡는 이유다.

## clientId가 어디 있나

토큰 파일에는 `clientIdHash`만 있고, 실제 값은 **옆 파일**에 있다:

```
~/.aws/sso/cache/kiro-auth-token.json   ← clientIdHash만
~/.aws/sso/cache/<clientIdHash>.json    ← clientId, clientSecret
```

export가 이 짝을 못 찾으면 반쪽 파일이 나온다.

## 올바른 이전 방법

`export`로 단일 파일을 뽑는 것보다, 원본 기기에서 캐시 디렉토리를 통째로 옮기는 쪽이
짝을 깨뜨리지 않는다:

```bash
cd ~ && tar czf ~/Downloads/kiro-sso.tgz .aws/sso/cache
```

받는 기기에서 풀고 `kiro-setup.sh`(인자 없이)를 돌린다.

## 붙인 뒤 엔진 반영

브리지 소스를 pull 해도 **실행 엔진은 자동으로 안 바뀐다.** `~/.rubato-pi/engine/`이
낡아 있으면 `kiro/` 프로바이더가 없어서 모델이 안 뜬다.

- `rubato restart`는 **브리지(:8788)만** 다시 띄운다. 엔진은 안 건드린다.
- 엔진 재빌드는 `rubato-pi.sh`가 **세션 기동 때마다** 부른다. 새 세션이든 resume이든
  같은 경로를 타므로, 창을 닫았다 켜는 것으로 충분하다.
- 낡았는지 판정: `node harness/scripts/build-engine.mjs --check` (0 신선, 10 낡음).

## 만료 구조 (세 겹)

| | 수명 | 만료되면 |
|---|---|---|
| accessToken | 1시간 | kiro.rs가 자동 갱신 — 신경 안 써도 된다 |
| **clientId 등록** | **90일** | ⚠️ 진짜 시한. 갱신이 막힌다 |
| refreshToken | 만료 필드 없음 | 사실상 계속 |

90일이 지나면 원본 기기에서 Kiro IDE를 한 번 열면 재등록된다. 로그인은 다시 안 해도 된다.

**미확인 위험**: 두 기기가 같은 refreshToken을 공유하면, AWS가 rotation 방식일 때
한쪽 갱신이 다른 쪽을 무효화할 수 있다. 2026-08-26 시점 미검증.

## 걸리기 쉬운 함정

- **export를 받는 기기에서 돌리면 순환이다.** export는 `~/.rubato-pi/kiro/credentials.json`을
  먼저 읽으므로, 앞선 import가 만든 깨진 파일을 다시 읽고 같은 결함을 재생산한다.
- **OAuth 로그인 링크를 다른 기기 브라우저에서 열면 안 된다.** 콜백이 localhost로
  돌아오므로 링크를 만든 기기에서만 완결된다. 다른 기기에서 열면 `ERR_CONNECTION_REFUSED`.
- `kiro-cli login`은 OAuth 콜백 타임아웃이 잦다. Kiro IDE 쪽이 안전하다(스크립트 주석).
