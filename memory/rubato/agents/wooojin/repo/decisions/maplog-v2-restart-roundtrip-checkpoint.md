---
description: 2026-09-01 사용자 확정: 첫 로딩은 loading UI로 수용하고 평상시 지도·사진 감상 memory를 후속 핵심 최적화 관문으로 두며, 재시작 왕복 검증 뒤 resolver를 마무리하는 순서.
---
# Maplog V2 재시작 왕복 체크포인트

날짜: 2026-09-01

상태: **사용자 확정 / 구현 전**

## 첫 로딩과 평상시 memory의 우선순위

우진:

> “첫 로딩이나 세팅은 그냥 로딩중인 애니메이션 UI로 대체하면 큰 문제는 안돼.”

> “대신 메모리 관련은 평소에 사용하는 동작에 한해선 최대한 최적화 해야돼. 왜냐면 맵 조작하며 사진 돌아가면서 보는 그 과정의 느낌을 팍 죽일 수 있는 위험이 있어.”

결정:

- 첫 로딩·초기 설정 시간은 정직한 loading UI로 기다릴 수 있으므로 지금의 단독 제품 탈락 기준으로 두지 않는다.
- 평상시 지도 조작과 사진 감상 중 memory pressure, 반복 재로딩, 끊김은 Maplog의 조작감을 직접 훼손하므로 후속 최적화 단계의 실제 iPhone 핵심 관문으로 둔다.
- 지금 당장 성급하게 최적화하지는 않는다. 다만 후속 구현이 snapshot release, cache, 점진 loading 같은 선택지를 구조적으로 막지 않게 한다.
- host 100,000장 post-load RSS 273.1MB와 process peak 505.5MB는 출시 임계값이 아니다.

## 다음 순서

우진:

> “재시작 왕복 작업 체크포인트로 잡고 한번 내 검증-피드백 받고서 resolver도 마무리 하면 될거같아 천천히 해도 되잖아”

결정:

1. 검증 가능한 실제 사진을 persisted date occurrence로 만든다.
2. 실제 지도·사진 감상에서 해당 날짜 장면을 열고 Journey에 추가한다.
3. 앱 종료·재실행 뒤 같은 occurrence ID·membership·Journey 순서와 화면이 돌아오는지 확인한다.
4. 우진이 직접 검증하고 피드백한다.
5. 피드백을 반영한 뒤 production timezone resolver를 마무리한다.

이 체크포인트에 필요한 최소 지도·Journey 연결만 허용한다. 새 renderer, catalog/RTree, split/merge·alias/tombstone lifecycle, Stage 3은 별도 승인 전까지 잠근다.

프로젝트 정본:

- `/Users/wooojin/App/maplog/record/decisions/2026-07-12_product_direction_register.md` PD-63
- `/Users/wooojin/App/maplog/record/v2/PRODUCT.md`
- `/Users/wooojin/App/maplog/record/v2/CURRENT.md`
- `/Users/wooojin/App/maplog/record/v2/FOLLOWUPS.md`