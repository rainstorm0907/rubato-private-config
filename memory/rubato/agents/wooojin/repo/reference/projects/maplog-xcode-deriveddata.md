---
description: Maplog 빌드 캐시 재사용과 중간 녹화·임시 QA 산출물의 용량 관리 규칙.
---
# Maplog 빌드와 QA 용량 관리

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

## QA 산출물에도 적용할 원칙

- 상태: 사용자 확정. 2026-09-17 Recap 제작 중 디스크 부족으로 중단한 뒤 재개하며, 우진: “앞으로 용량도 너무 막 쓰지 말고 잉여파일은 정리하면서 해.”
- 관련 작업은 고정 빌드 캐시를 재사용하고, 실행마다 별도 캐시·앱 사본·전체 영상을 누적하지 않는다. 위 result-first 전용 경로를 다른 프로젝트가 공유하라는 뜻은 아니다.
- 화면 판단에 필요한 후보는 녹화하되, 경계·데이터 검사를 매번 전체 녹화로 만들지 않는다. 원사진·비교 기준·최신 결과·실패 재현에 필요한 증거를 보호하고, 대체된 중간 촬영물·임시 프레임·재생성 가능한 중복 캐시는 쓰임을 확인해 정리한다. 다른 세션의 파일이나 근거의 유일한 사본을 잉여로 추정하지 않는다.
- 빌드·녹화 전에 여유 공간을 확인한다. 비교판의 기존 형식을 지키려고 불필요한 산출물을 유지하거나 분석 도구를 늘리지 않는다. 우진: “비교판도 기존 양식을 유지할 필요없고 너가 생각할때 최적의 구조로 효율적으로 바꿔.”