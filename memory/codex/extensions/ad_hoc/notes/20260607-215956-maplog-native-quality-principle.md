# Maplog quality principle

우진님은 앱 개발에서 "조금 나아진 타협안"보다 사용자가 요구한 핵심 품질을 만족하는 정석 구현을 선호한다.

Maplog live map QA에서 SwiftUI overlay 라벨을 60fps로 튜닝했지만, 우진님은 네이버 지도 앱 같은 완전한 marker 위치 동기화를 원했다. 최종적으로 Naver SDK `NMFMarker` native overlay로 계층을 바꾸자 사용자가 "이거야"라고 확인했다.

앞으로 비슷한 상황에서는 먼저 다음을 검토한다:

- 사용자가 요구한 품질 수준이 현재 구현 계층에서 구조적으로 가능한가?
- 더 적합한 native SDK, platform layer, first-party API, proven engine이 있는가?
- 튜닝으로 타협하기 전에 구현 계층을 바꾸는 정석 해법이 있는가?
- QA는 회사식으로 scenario / expected / actual / verdict / evidence / follow-up을 남긴다.

원칙: 핵심 조작감, 지도/캔버스/미디어/실시간 UI처럼 품질 체감이 중요한 영역에서는 "충분히 괜찮음"으로 멈추지 말고, 가능한 가장 정석적인 계층을 먼저 검토한다.
