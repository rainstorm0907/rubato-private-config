---
name: hama-portfolio-pdf-pipeline
description: Hama 포트폴리오 md→PDF 재생성 파이프라인과 자산 파일 위치
metadata: 
  node_type: memory
  type: project
  originSessionId: ae0c8b0a-2042-441b-bedc-4786dfa2b6f8
---

Hama 포트폴리오 제출물 빌드 체계 (2026-06-12 구축):

- 원본: `/Users/wooojin/Downloads/portfolio.md` (내부용 "## 첨부 체크리스트" 섹션은 변환 시 자동 제외됨)
- 빌드: `python3 /tmp/hama_pdf_job/build.py` (python-markdown, 인쇄 CSS 포함) → `/tmp/hama_pdf_job/portfolio.html`
- 렌더: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --print-to-pdf="/Users/wooojin/Downloads/Hama_포트폴리오_draft.pdf" --no-pdf-header-footer "file:///tmp/hama_pdf_job/portfolio.html"`
- 이미지 자산(전부 Downloads, md와 같은 폴더 필수): hama_logo.png(표지), Hama_시스템_아키텍처.png, Hama_ERD.png(운영 21테이블, SVG 원본 `/tmp/hama_pdf_job/erd.svg`), screen_home/product_detail/price_compare/admin/chatbot/mypage.png
- 주의: 코덱스 샌드박스에서 Chrome headless 실행 불가(CHROME_BLOCKED) — 렌더는 메인 세션에서 실행. `/tmp`는 재부팅 시 삭제될 수 있으니 장기 보관 필요하면 build.py·erd.svg를 Downloads로 백업.
- 표 CSS는 `overflow-wrap: break-word; word-break: keep-all` 유지 (anywhere로 바꾸면 좁은 칸에서 "Situati on" 단어 쪼개짐 재발).
