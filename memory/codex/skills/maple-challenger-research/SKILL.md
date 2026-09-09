---
name: maple-challenger-research
description: MapleStory 챌섭 장비/주문서/보스컷/시세/커뮤 여론을 빠르게 조사해야 할 때, character snapshot과 로컬 KB를 먼저 고정하고 quiet-browse로 최소한의 커뮤니티 증거만 병렬 수집한다.
argument-hint: "[character] [keywords]"
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# When to use

- MapleStory 챌섭 장비, 주문서, 보스컷, 시세, 커뮤니티 여론을 빠르게 정리해야 할 때
- `카레잠`, `카헤잠`, `미트라`, `블랙보조`처럼 특정 품목/세팅 판단이 필요할 때
- 커뮤니티 탐색 전에 현재 캐릭터 상태와 로컬 KB 근거를 먼저 고정해야 할 때

쓰지 말 것:

- 이미 필요한 가격/판단 근거가 로컬 KB에 충분히 있고 외부 커뮤니티 확인이 불필요한 경우
- raw fetch/curl로 아카이브되지 않은 커뮤니티를 대량 스크랩하려는 경우

# Inputs / context to gather

1. 대상 캐릭터명과 질문 종류를 고정한다.
2. `character/<캐릭>/item-equipment.json`이 있는지 확인한다.
3. 관련 `kb/branchpoints/`와 `kb/latest-digest.md` 위치를 확인한다.
4. 사용자가 묻는 핵심 키워드 2~4개를 뽑는다.
5. 커뮤니티 확인이 필요한지, 로컬 KB만으로 결론 가능한지 먼저 판단한다.

# Procedure

1. 현재 상태를 먼저 고정한다.
   - `character/<캐릭>/item-equipment.json`
   - 관련 `kb/branchpoints/`
2. 동시에 로컬 KB를 훑는다.
   - `./scripts/latest_digest.sh`
   - 대상 키워드로 `kb/latest-digest.md`, `kb/branchpoints`, `kb/yt`에 `rg`
   - `latest_digest.sh`의 exit code와 failed browser sections를 함께 기록한다. exit code 1이면 부분 파일은 참고용으로만 쓰고, 공식·커뮤니티 최신 정찰 성공으로 말하지 않는다.
3. 외부 커뮤니티가 필요하면 최소 범위로만 본다.
   - 아카/디시는 raw fetch/curl을 쓰지 않는다.
   - `quiet-browse open`
   - `sleep 2~3`
   - `quiet-browse text`
   - 검색 목록 1개와 핵심 글 1~3개만 읽는다.
4. 커뮤니티 글은 제목 여론만 보지 말고 전제를 분리한다.
   - 뉴비
   - 저메소
   - 시즌용 교불 매몰
   - 완제품 구매 가능
   - 직업별 매물가
   - 보스컷
   - 후반 수요
5. 아이템 설명에서 거래 제약을 먼저 체크한다.
   - 교불/카르마/시즌 전용 장비는 회수 가능 장비처럼 설명하지 않는다.
6. 가격 판단은 `깡통가`와 `완성품가`를 분리한다.
   - 깡통에는 강화/잠재/에디/재설정 비용을 붙여 본다.
7. 답변은 결론 먼저로 정리한다.
   - 사라 / 기다려라 / 조건부
   - 숫자 매수선
   - 근거 2~3줄

# Efficiency plan

- 외부 검색 전에 character snapshot과 로컬 KB를 먼저 읽어 커뮤니티 탐색 범위를 줄인다.
- `latest_digest.sh`와 `rg`는 병렬로 돌려 로컬 근거를 먼저 확보한다.
- `latest_digest.sh`가 exit code 1이면 파일을 버리지 않되, 실패한 섹션만 최소 재시도하거나 그 최신성 한계를 답변에 남긴다.
- quiet-browse는 검색 목록 1개 + 핵심 글 1~3개까지만 읽고, 그 이상은 새 근거가 없으면 멈춘다.
- stop rule: 로컬 KB + 최소 커뮤니티 증거로 `사라/기다려라/조건부`와 숫자 매수선이 나오면 추가 탐색을 멈춘다.

# Pitfalls and fixes

- 증상: 커뮤니티 탐색이 길어지고 결론이 늦다.
  - 원인: 현재 캐릭터 상태와 로컬 KB를 먼저 고정하지 않았다.
  - 수정: `item-equipment.json`, `kb/branchpoints`, `latest_digest`를 먼저 본다.
- 증상: YouTube RSS가 남은 `kb/latest-digest.md`를 전체 정찰 성공으로 말한다.
  - 원인: `quiet-browse` 실패와 스크립트 exit code를 확인하지 않았다.
  - 수정: exit code 1 또는 failed browser sections가 있으면 부분 결과로 표시하고, 필요한 근거만 재시도한다.
- 증상: 제목 여론만 보고 잘못된 추천을 한다.
  - 원인: 뉴비/저메소/교불 매몰/완제품 구매 가능성 같은 전제를 분리하지 않았다.
  - 수정: 전제를 먼저 분리하고 사용자 상황에 맞는 줄기만 남긴다.
- 증상: 교불/카르마/시즌 전용 장비를 회수 가능한 장비처럼 설명한다.
  - 원인: 거래 제약 확인이 뒤로 밀렸다.
  - 수정: 거래 가능/회수 가능 여부를 답변 앞단에서 명시한다.
- 증상: 깡통가가 싸 보여도 실제론 비효율인데 추천이 나간다.
  - 원인: 강화/잠재/에디/재설정 비용을 붙이지 않았다.
  - 수정: 깡통가와 완성품가를 분리하고 추가 비용을 합산한다.

# Verification checklist

- 현재 캐릭터 snapshot과 `kb/branchpoints`를 먼저 확인했다.
- `latest_digest.sh`와 관련 `rg` 결과로 로컬 근거를 확보했고, exit code 및 failed browser sections를 확인했다.
- 외부 커뮤니티는 quiet-browse로 최소 범위만 읽었다.
- 거래 제약과 깡통/완성품 가격 차이를 분리했다.
- 최종 답변이 `사라/기다려라/조건부`, 숫자 매수선, 근거 2~3줄 구조를 따른다.
