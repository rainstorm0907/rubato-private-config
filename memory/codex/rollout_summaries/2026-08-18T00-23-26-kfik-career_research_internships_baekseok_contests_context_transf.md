thread_id: 01a01240-6ac7-7db1-8c62-4dcdf522026c
updated_at: 2026-08-18T01:32:38+00:00
rollout_path: /Users/wooojin/.codex/sessions/2026/08/18/rollout-2026-08-18T09-23-26-01a01240-6ac7-7db1-8c62-4dcdf522026c.jsonl
cwd: /Users/wooojin

# 취업 가능성 판단, 재학생 인턴 및 백석대 공모전 조사, 사용자 컨텍스트 요약

Rollout context: 사용자는 카카오뱅크 AI Native 서비스 기획자 채용연계형 인턴 지원 가능성, 휴학 우회 가능성, 재학생 인턴 대안, 백석대 교내 공모전 및 상금·개인 참가 가능 여부를 연속적으로 조사했다. 마지막에는 다른 AI 어시스턴트로 옮길 수 있는 사용자 컨텍스트 요약을 특정 형식으로 요청했다.

## Task 1: 카카오뱅크 인턴 자격 및 휴학 가능성 판단

Outcome: success

Preference signals:
- 사용자는 “지원 버튼은 절대 누르지 마”라고 반복 지시했다 -> 채용 조사에서는 읽기·검증만 하고 지원이나 제출은 실행하지 않아야 한다.
- 사용자는 “원문 근거로만 판정”을 요구했다 -> 자격 판단은 공식 공고의 문구와 학교 규정, 확인된 학점 자료를 분리해 제시해야 한다.

Key steps:
- 로컬 포트폴리오, Claude 메모리, Aside 메모리, 이력서 PDF, 경험정리 파일을 확인했다.
- 카카오뱅크 공식 공고 `https://recruit.kakaobank.com/jobs/263159`를 확인했다.
- 공고의 핵심 자격은 “기졸업자 또는 졸업 요건을 모두 갖춘 수료자”, “수업(온라인 포함), 시험 등 인턴 기간 중 학업 병행이 필요한 분은 지원이 불가합니다.”였다.
- 로컬 졸업요건 파일에서 120학점 중 84.5학점 취득, 35.5학점 부족, 전공 54학점 중 33학점 취득을 확인했다.
- 백석대 휴학은 학업 중단을 의미하며 졸업요건을 충족한 수료 상태를 만들지 않으므로, 긴급휴학으로 해당 공고 자격을 우회할 수 없다고 판단했다.

Failures and how to do differently:
- LinkedIn 원본 URL이 처음에는 깨져 “페이지 없음”이 나왔다. `kr.linkedin.com` 링크로 재탐색해 게시물과 공식 공고를 확인했다.
- Aside REPL에서 stale ref, 중복 `const` 선언, 잘못된 selector, `waitForTimeout` 미지원 등이 반복됐다. 다음에는 매 액션 후 새 snapshot, 새 변수명, Aside 지원 API만 사용해야 한다.

Reusable knowledge:
- 카카오뱅크 AI Native 서비스 기획자 공고는 2026-11-02 시작, 3개월, 판교, 포트폴리오 PDF 표지 제외 10장 이내, 기획·AI 관련 경험만 요구했다.
- 카카오뱅크 체험형 어시스턴트 공고는 별도 학력 제한 문구 없이 풀타임 근무 가능 여부를 핵심으로 삼는다.

References:
- 공식 공고: `https://recruit.kakaobank.com/jobs/263159`
- 확인 문구: `기졸업자 또는 졸업 요건을 모두 갖춘 수료자`
- 확인 문구: `수업(온라인 포함), 시험 등 인턴 기간 중 학업 병행이 필요한 분은 지원이 불가합니다.`
- 학점 파일: `/Users/wooojin/Downloads/2022학년도 입학자 졸업소요 취득학점.xlsx`

## Task 2: 재학생 인턴 및 취업 루트 조사

Outcome: partial

Preference signals:
- 사용자는 “많이많이 찾아줘”라고 요청했지만 이후 “지금 열린 재학생 가능 공고와 백석대 교내 대회만 원문으로 다시 걸러볼게요”라는 방향을 수용했다 -> 넓은 후보 수집 후 실제 열림 상태와 자격 원문으로 재검증하는 2단계 조사를 선호한다.

Key steps:
- Wanted, 자소설닷컴, 네이버·카카오·우아한형제들·무신사·삼성·카카오뱅크 채용 사이트를 조사했다.
- 재학생 가능으로 확인된 대표 공고는 딥오토 AI Engineer, 피치에이아이 AI/ML Engineer, 컷백 AI Engineer, 카카오뱅크 AI 운영 어시스턴트와 대출비교서비스 운영 어시스턴트였다.
- 네이버에는 2026-08-18 기준 네이버웹툰 체험형 인턴 1건이 있었고, 삼성은 인턴 0건, 카카오와 우아한형제들·무신사는 인턴 공고가 없었다.
- 초기 조사에는 상시채용·시즌 패턴·추정 자격이 섞였고, 후속 검증에서 일부 공고가 마감 또는 URL 변경 상태임을 확인했다.

Failures and how to do differently:
- “최소 20개” 수집은 일부 항목이 공식 원문 검증 전 추정에 의존했다. 향후에는 처음부터 `현재 열림 / 마감 / 시즌 추정`을 분리하고, 검증되지 않은 자격을 재학생 가능으로 단정하지 않아야 한다.
- 회사별 채용 사이트를 한 번에 넓게 훑기보다 사용자의 직무와 학기 일정에 맞는 5~10개를 먼저 원문 검증하는 편이 효율적이다.

Reusable knowledge:
- 딥오토 공고에는 “재학/휴학/졸업생 모두 가능”이 명시됐다.
- 피치에이아이 공고에는 “방학 중인 재학생, 휴학생, 졸업예정자 또는 기졸업자”, “정규학기 수업을 병행하지 않고 주 5일, 주 40시간 근무”가 명시됐다.
- 카카오뱅크 체험형 어시스턴트는 학력 제한보다 6개월 풀타임 조건이 중요하다.

References:
- `https://www.wanted.co.kr/wd/379363`
- `https://www.wanted.co.kr/wd/376376`
- `https://www.wanted.co.kr/wd/324408`
- `https://recruit.kakaobank.com/jobs/262683`
- `https://recruit.kakaobank.com/jobs/262837`

## Task 3: 백석대 교내 공모전 조사 및 2026-2 예측

Outcome: partial

Preference signals:
- 사용자는 “가능하면 1인이 좋은데 안되면 친구 한명까진 ㄱㅊ”이라고 했다 -> 공모전 추천 시 개인 참가를 우선하고, 불가하면 2인 구성까지를 기본 대안으로 제시해야 한다.
- 사용자는 “현실적으로 내가 그렇게 3개정도 한다면”이라고 범위를 좁혔다 -> 대회별 상금·참가 형태·예상 일정·노력 배분을 함께 비교해야 한다.

Key steps:
- Smart IT, Hacking Festival, JAVA 프로그래밍 경진대회 최신 모집 공고를 공식 컴퓨터공학부 게시판에서 확인했다.
- Smart IT는 개인 또는 5인 이내 팀, 대상 100만 원, 금상 60만 원, 은상 40만 원, 동상 20만 원, 장려상 10만 원이었다.
- Hacking Festival은 참가 대상 백석대 재학생, 팀 단위 시상, 대상 50만 원, 금상 40만 원, 은상 20만 원, 장려상 10만 원이었다. 본문에 1인 금지나 팀 인원 제한은 없었다.
- JAVA는 개인 문제풀이 대회로 대상 20만 원, 금상 15만 원, 은상 10만 원, 동상 5만 원이었다.
- 2026-2 예측은 Smart IT 9~11월 모집, Hacking Festival 9~10월, JAVA 10~11월 모집 및 12월 진행으로 제시했다. 이는 과거 공지 월 기반 추정이며 2026 공고 확정 사실은 아니다.

Failures and how to do differently:
- Hacking Festival과 JAVA 검색 과정에서 게시판 URL·selector 오류가 여러 번 발생했다. 검색 결과 목록에서 정확한 게시물 링크를 먼저 추출한 뒤 직접 열어야 한다.
- Smart IT의 최근 공고는 확인됐지만 2026 공고는 아직 없었다. 과거 패턴을 확정 일정처럼 말하지 않고 반드시 “추정”으로 표시해야 한다.

Reusable knowledge:
- Smart IT는 사용자의 Hama/maplog 경험과 가장 잘 맞는 교내 대회로 판단됐지만, 교내 수상보다 회사 인턴 경험의 이력서 가치가 더 크다는 결론이 제시됐다.
- 3개를 모두 할 경우 제안된 노력 배분은 Smart IT 70%, Hacking Festival 20%, JAVA 10%였다.
- JAVA는 혼자, Smart IT는 혼자 또는 2인, Hacking Festival은 친구 1명과 구성하는 방식이 사용자 조건에 맞는다.

References:
- Smart IT: `https://community.bu.ac.kr/info/1788/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGaW5mbyUyRjg5NyUyRjUyNjYxJTJGYXJ0Y2xWaWV3LmRv`
- Hacking Festival: `https://community.bu.ac.kr/info/1788/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGaW5mbyUyRjg5NyUyRjUxNjk4JTJGYXJ0Y2xWaWV3LmRv`
- JAVA: `https://community.bu.ac.kr/info/1788/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGaW5mbyUyRjg5NyUyRjUxNzAzJTJGYXJ0Y2xWaWV3LmRv`
- Smart IT 원문: `신청대상 : 컴퓨터공학부 재학생(개인 또는 5인 이내 팀/ 타학부 참여 가능)`
- JAVA 원문: `참여대상 : 백석대학교 재학생`

## Task 4: Codex 토큰·사용량 질문

Outcome: success

Preference signals:
- 사용자는 조사 비용과 토큰 사용량을 별도로 물었다 -> 대규모 조사 전 예상 비용·범위·검증 수준을 먼저 알려주면 사용자 통제에 도움이 된다.

Key steps:
- 공식 OpenAI/Codex 가격 문서를 확인했다.
- Codex와 ChatGPT Work 사용량을 공유하며, 사용량은 모델·컨텍스트·추론·도구·검색·캐싱에 따라 달라져 프롬프트 길이만으로 정확히 예측할 수 없다는 점을 확인했다.
- 당시 답변은 이 조사 규모를 입력 80만~150만 토큰, 출력 8만~15만 토큰 정도로 추정했으나 실제 계정 사용량은 확인되지 않았다.

Reusable knowledge:
- 공식 문서상 GPT-5.4 API 가격은 입력 1M 토큰 $2.50, 캐시 입력 $0.25, 출력 $15.00이다.
- Codex 정액제는 직접 API 청구가 아니라 플랜별 사용량 한도와 크레딧 구조로 소비된다.
- 대규모 브라우저 조사에서는 처음부터 “현재 열린 것만 10개”, “백석대 교내만”처럼 범위를 잘라야 사용량을 줄일 수 있다.

References:
- `https://learn.chatgpt.com/docs/pricing.md`
- `https://developers.openai.com/api/docs/pricing.md`

## Task 5: 다른 AI 어시스턴트용 사용자 컨텍스트 요약

Outcome: success

Preference signals:
- 사용자는 “1인칭 대명사와 2인칭 대명사는 사용하지 말아 줘”, “사용자를 칭하거나 중립적인 표현”을 요구했다 -> 컨텍스트 이전 문서는 대명사 제한을 지키고 ‘사용자’ 중심으로 작성해야 한다.
- 사용자는 “가능하면, 특히 요청 사항 및 선호 사항의 경우에 해당 사용자의 문구를 그대로 유지해 줘”라고 했다 -> 선호와 규칙은 원문 인용을 보존해야 한다.
- 사용자는 “저장된 메모리에 있는 규칙만 포함해야 해”라고 했다 -> 추론이나 현재 대화의 임시 제안은 영속 규칙으로 승격하지 않아야 한다.
- 사용자는 마지막 텍스트를 “가져온 위치: <name>”으로 고정했다 -> 지정된 마이그레이션 요약 형식을 정확히 지키고 마지막 줄을 고정해야 한다.

Key steps:
- 저장된 Codex 메모리와 Aside 사용자 메모리를 검색했다.
- 인구통계, 관심분야, 인간관계, 날짜별 이벤트·프로젝트·계획, 요청 사항 순으로 요약했다.
- 실제 저장 규칙에는 shared checkout 보호, 오버엔지니어링 금지, 임계값 확정 전 사용자 확인, Maplog 시각 계약, OpenAI Game 구현 게이트, 구매 승인, 문서 서명 승인, 배달 주소 확인 등이 포함됐다.

Reusable knowledge:
- 사용자는 한국어 존댓말, 결과 먼저·원인 다음, 짧고 쉬운 문장을 선호한다.
- 본인 명의 취업 글은 담백한 평서문, 수치 중심, 가운뎃점과 과장된 격언조를 피하는 스타일을 선호한다.
- 파일·live state·정확한 오류·실제 검증 증거를 근거로 한 결론을 선호한다.

References:
- `/Users/wooojin/.codex/memories/MEMORY.md`
- `/Users/wooojin/.codex/memories/memory_summary.md`
- `/Users/wooojin/.aside/u/0/memory/users/jung-woojin.md`


