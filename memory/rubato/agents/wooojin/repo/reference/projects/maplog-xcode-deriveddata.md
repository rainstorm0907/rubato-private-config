---
description: Rules for reusing the Maplog build cache, and for disk management of intermediate recordings and temporary QA artifacts.
---
# Maplog build and QA disk management

- Status: user confirmed · handoff implemented
- Date: 2026-09-02
- Context: the problem of the Xcode cache growing on every run while repeatedly building the result-first Place experiment.

Woojin's original:

> “빌드마다 0.8~1GB짜리 별도 캐시를 만드는 방식이야. 앞으로는 /Users/wooojin/Library/Developer/Xcode/DerivedData/MaplogResultFirstPlace 재사용하게 해달라고도 해줘. xcode 용량 관리차원”

Application:

- On Maplog result-first `xcodebuild`, specify `-derivedDataPath /Users/wooojin/Library/Developer/Xcode/DerivedData/MaplogResultFirstPlace`.
- Do not make a separate DerivedData directory or a `/tmp/maplog-*` cache on every build and test.
- This rule is a disk-management boundary to stop about 0.8~1GB being duplicated every build.
- The handoff canonical sources are now `/Users/wooojin/App/maplog/record/CURRENT.md` and `record/PRODUCT.md` (the old `record/plans/` bundle was deleted in the 2026-09-29 cleanup, and past progress was summarized in `record/RETRO.md`).

## Principle to apply to QA artifacts too

- Status: user confirmed. While resuming after stopping for lack of disk during Recap production on 2026-09-17, Woojin: “앞으로 용량도 너무 막 쓰지 말고 잉여파일은 정리하면서 해.”
- Related work reuses a fixed build cache, and does not accumulate a separate cache, an app copy, or a full video on every run. This does not mean other projects should share the result-first-only path above.
- Record the candidates needed for a screen judgment, but do not make a boundary or data check a full recording every time. Protect original photos, comparison baselines, the latest result, and evidence needed to reproduce a failure, and after checking their use, clean up replaced intermediate recordings, temporary frames, and regenerable duplicate caches. Do not presume another session's file, or the only copy of grounds, to be surplus.
- Check free space before building and recording. Do not keep an unnecessary artifact, or add an analysis tool, in order to keep a comparison board's existing format. Woojin: “비교판도 기존 양식을 유지할 필요없고 너가 생각할때 최적의 구조로 효율적으로 바꿔.”
