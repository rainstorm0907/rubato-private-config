---
name: reflection-essay-writing-style
description: 우진님 성찰지·자기성찰형 과제 보조 방식(mood 소재+전문용어 제거+기존 문체 모방)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 186e3da6-2449-4148-88c5-cb3163f45be8
---

우진님의 학교 성찰지/자기성찰형 글쓰기 과제(예: 대인관계·의사소통 교양수업 주차별 성찰지)를 도울 때 적용하는 방식.

**Why:** 성찰지는 본인 경험이 진짜로 담겨야 하고, 제출용이라 상담 분석 톤이 드러나면 안 됨. 우진님은 mood 상담기록을 소재로 쓰되 본인 톤 유지를 중시함.

**How to apply:**
- 소재는 `/Users/wooojin/mood/counseling/woojin/`(logs.md, profile.md)에서 끌어오되, 상담/심리 전문용어(비폭력대화·NVC, I-메시지, 지성화, 핵심감정, 채점표 등)는 그대로 쓰지 말고 일반 학생 말로 풀어쓴다.
- 문체는 우진님이 직접 쓴 기존 작성본을 codex로 분석해 맞춘다: -습니다 평서문, 추정형 어미(~것 같습니다), 따옴표 최소, 연결어 사용, 감정은 솔직하되 인물·사건 디테일은 흐림, 소박한 다짐형 한 줄.
- 여러 과목 성찰지를 동시에 쓸 때 소재가 겹치지 않게 한다(대인관계에서 쓴 일화·영상을 의사소통에 재탕 금지).
- 작성 전/후 codex로 문체·중복·작위성 교차검증(우진님이 "코덱스랑 같이 해"라고 명시적으로 요청한 적 있음).
- hwpx 양식 채우기: 압축해제 → `Contents/section0.xml`에서 colSpan=3 빈 본문/한줄 셀의 subList 내부를 문단으로 교체 → 원본 zip에 section0.xml만 `zip -X`로 갱신(mimetype 첫 엔트리 유지). 날짜·소요시간·장소 칸은 실제 값이라 우진님이 직접 채우게 남긴다.

관련: [[hama-portfolio-pdf-pipeline]], [[user-profile]]
