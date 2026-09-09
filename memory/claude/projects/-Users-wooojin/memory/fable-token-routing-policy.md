---
name: fable-token-routing-policy
description: Fable 토큰 절약 — 잔바리·명세 확실한 작업은 GPT-5.6(Terra/Sol/Luna)로 보내고 생각 강도는 Claude가 정함 (2026-07-13 확정)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8ae86417-9c9e-4c07-964a-73b25e50fef8
---

우진님 확정(2026-07-13): "앞으로 fable에게 전부 작업을 시키기엔 토큰이 넉넉하지 않다. 잔바리 업무나 창의성이 떨어져도 확실한 업무는 codex 5.6 시켜도 된다. Terra나 Sol의 생각 강도도 네가 정해줘."

**Why:** Fable은 최고 성능이지만 가장 비싸다(Artificial Analysis Coding Agent Index 기준 GPT-5.6 Sol Ultra급 점수를 더 높은 비용으로). Terra Extra High가 Opus 4.8 Max급 성능을 약 1/3 비용으로 내는 최적점.

**How to apply:**
- Fable: 새 시각 인터랙션·물리 은유·모호한 제품 탐색 등 관문급 창의 작업만. 방향잡이/검증 판단 세션도 Fable 유지.
- Terra Extra High: 승인된 UX의 표준 구현·통합 (기본값).
- Terra Medium~High: 잔바리·절차 작업(재녹화, 회귀, 문서 교정, 스크립트).
- Luna High~Extra High: 아주 단순한 확인성 작업.
- Sol High~Extra High: 실패 비용 큰 넓은 변경·막힌 디버깅. Sol Ultra는 비용 급증이라 마지막 수단.
- **갱신(2026-07-14 우진님 확정):** meight 업스트림 v3(luna xhigh+fast를 기본 일꾼, terra는 폴백)에 대해 — **Maplog은 Terra 기본 유지**, 다른 프로젝트의 잔바리·bounded 구현부터 Luna xhigh(+fast)를 시험 투입해 실측 근거를 쌓은 뒤 기본값 교체 재논의. Sol effort 기본은 high(xhigh는 진짜 고난도만).
- 실행 프롬프트 상단에 모델+강도+이유를 명시. Codex는 Chrome 확장 불가라 브라우저 실검증은 제외.

관련: [[codex-meight-global-setup]]. Maplog에서는 저장소 상설 규칙으로 승격됨(2026-07-14): `/Users/wooojin/App/maplog/ops/OPERATIONS.md`(라우팅·검증 무결성·공개 게시·폴링 규칙), 방향잡이 프롬프트 정본은 `ops/prompts/fable-product-direction-guardian.md`(Downloads 사본은 구본).
