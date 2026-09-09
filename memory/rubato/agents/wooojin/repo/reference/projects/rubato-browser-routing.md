---
description: Rubato의 browser-cli 단일 정본, Aside abrowse/gbrowse, insane-search 공개 조회 경계를 확정한 결정과 검증 기록.
---
# Rubato 브라우저 라우팅

## 사용자 결정

- 2026-09-02, Fable Medium 제안과 로컬 실측을 비교한 뒤 우진: “오 좋아 그렇게 해보자.”
- 상태: 사용자 확정 / 구현됨 / 로컬 검증됨.

## 확정한 경계

- `browser-cli`가 브라우저 백엔드 선택의 단일 owner다.
- 이미 위치와 추출값을 아는 결정적 한 단계는 `abrowse`, 페이지를 읽고 판단해야 하는 탐색은 `gbrowse`로 간다.
- 로그인, 클릭·폼, 렌더링, 스크린샷, 브라우저 상태 증거는 Aside가 맡는다.
- `insane-search`는 공개 페이지 전체가 아니라 개별 글·정확한 메타데이터·이미 아는 셀렉터처럼 결과가 작고 목표가 정해진 비브라우저 조회만 먼저 맡는다.
- 일반 공개 URL이 403/WAF에 막혔을 때는 `isearch`가 `--no-playwright --max-attempts 3`으로 싼 전송 경로만 확인한다. 이 라우팅에서는 raw `python3 -m engine` R1/R6를 우회하지 못한다. 성공 출력은 4KB로 강제 제한하고, 과대 출력은 exit 5, 탐색 실패는 R6·Playwright 지시를 숨긴 exit 7로 바꿔 `gbrowse`로 돌린다. 404·인증·페이월은 exit 8로 끝내 브라우저를 헛돌지 않는다.
- 넓은 피드·검색 결과·읽어봐야 중요도를 알 수 있는 페이지는 원문이 리드 컨텍스트에 쏟아지지 않도록 `gbrowse`로 보낸다.
- `aside exec`은 Aside 메모리·히스토리가 반드시 필요한 희귀 예외로만 남긴다.

## 정본과 설치

- 정본: `/Users/wooojin/.agents/skills/browser-cli`.
- 배포 사본: `/Users/wooojin/dev/Rubato/harness/skills/browser-cli`.
- Claude와 Codex의 동명 사본은 설치기가 백업한 뒤 공통 정본 심볼릭 링크로 바꾼다.
- `aside-browser`는 라우팅하지 않고 REPL API와 SPA 실제 URL 확인 지식만 소유한다.

## 검증 기록

- `gbrowse`는 `example.com`에서 실제 브라우저 호출 1회 후 `Example Domain`을 반환했다. 예전의 “example.com은 항상 차단됨” 카나리 전제는 폐기하고 브라우저 호출 수를 판정 기준으로 바꿨다.
- `abrowse`는 `https://example.org/ | Example Domain`을 반환하고 같은 호출에서 탭을 닫았다.
- X 개별 글 Phase 0의 원문은 920바이트였고, 최종 `isearch` 출력은 1,371바이트로 4KB 상한 안에서 성공했다.
- Reddit 넓은 피드는 `isearch` 출력이 30,827바이트라 exit 5로 막혔고 stdout에는 0바이트만 건넸다. 속도만 보고 프로토콜 우선으로 보내면 컨텍스트 비용이 커진다는 근거가 됐다.
- 실제 `example.org` 404는 exit 8, stdout 0바이트로 끝났고 `gbrowse`로 확대하지 않았다.
- 설치기 단위 테스트 5개, skill-picker 단위 테스트 1개, 릴리스·패키지 테스트 13개가 통과했다.
