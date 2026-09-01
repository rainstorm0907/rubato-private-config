# 구현 레퍼런스

## 시작 전

저장소 루트에 `AGENTS.md` 나 `CLAUDE.md` 가 있으면 먼저 읽는다. 거기 있는 규칙이 이 문서보다 우선한다.

## 확인 명령 — 스택별로 다르다

한 저장소 안에 여러 스택이 섞여 있다. **건드린 부분에 해당하는 것만** 돌린다.

| 대상 | 확인 |
|---|---|
| Swift / iOS 앱 (`code/Maplog/`) | `xcodebuild -project code/Maplog.xcodeproj -scheme Maplog -destination 'platform=iOS Simulator,name=iPhone 17 Pro' build` |
| Swift 로직 픽스처 테스트 | `sh code/scripts/<이름>/run.sh` — 앱 소스를 macOS 호스트에서 직접 컴파일해 돌린다 |
| Cloudflare Worker (`backend/cloudflare/*/`) | 해당 디렉터리에서 `pnpm check` (tsc --noEmit), 테스트는 `pnpm test` (vitest) |
| Supabase 마이그레이션·정책 | `backend/supabase/tests/` 의 `.sql` / `.mjs` 러너 |
| 그 밖의 TS 프로젝트 | `pnpm typecheck` / `pnpm lint` |

테스트는 태스크에 명시된 경우에만 돌린다.

## 작업 안전 — 공유 작업 트리

**이 저장소는 여러 세션이 같은 dirty working tree 를 공유한다.**

- `git commit` / `reset` / `checkout --` / `clean` / `revert` / `stash` 를 **하지 않는다.** 내 변경을 되돌리는 것도 포함이다
- 브리프에 없는 파일은 수정하지 않는다. 다른 세션의 미완성 변경일 수 있다
- `git status` 에 낯선 변경이 보여도 정리하지 않는다 — 보고만 한다

빌드가 내 변경과 무관한 파일에서 깨지면 그것도 보고 대상이다. 고치려 들지 않는다.

## 막혔을 때

고치고 다시 돌리는 건 **3회까지**. 그래도 안 되면 멈추고 보고한다 — 시도한 것, 실제 에러 원문, 추정 원인.

같은 접근으로 두 번 실패했으면 접근이 문제다. 세 번째는 다른 각도로 가거나, 그 판단 자체를 오케스트레이터에 돌린다.

## 보고에 넣을 것

돌린 확인 명령과 **그 출력**. "빌드 통과"라고 쓰지 말고 통과한 명령을 적는다. 안 돌린 확인이 있으면 안 돌렸다고 적는다 — 그게 오케스트레이터가 알아야 할 사실이다.
