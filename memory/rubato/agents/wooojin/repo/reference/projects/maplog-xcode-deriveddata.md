---
description: Maplog Xcode 빌드가 고정 DerivedData 경로를 재사용해야 하는 용량 관리 규칙.
---
# Maplog Xcode DerivedData 재사용

- 상태: 사용자 확정·인수인계 구현됨
- 날짜: 2026-09-02
- 맥락: result-first Place 실험을 반복 빌드하며 Xcode 캐시가 실행마다 늘어난 문제.

우진 원문:

> “빌드마다 0.8~1GB짜리 별도 캐시를 만드는 방식이야. 앞으로는 /Users/wooojin/Library/Developer/Xcode/DerivedData/MaplogResultFirstPlace 재사용하게 해달라고도 해줘. xcode 용량 관리차원”

적용:

- Maplog result-first 관련 `xcodebuild`에는 `-derivedDataPath /Users/wooojin/Library/Developer/Xcode/DerivedData/MaplogResultFirstPlace`를 명시한다.
- 빌드·테스트마다 별도 DerivedData 디렉터리나 `/tmp/maplog-*` 캐시를 만들지 않는다.
- 이 규칙은 빌드마다 약 0.8~1GB가 중복되는 것을 막기 위한 용량 관리 경계다.
- 정본 인수인계: `/Users/wooojin/App/maplog/record/plans/2026-09-02_result_first_place_map_session_handoff.md`