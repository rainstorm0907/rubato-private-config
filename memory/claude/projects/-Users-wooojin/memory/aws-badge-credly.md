---
name: aws-badge-credly
description: "AWS Skill Builder AI-DLC 뱃지 진행 중(8/14 등록 완료) — 평가 80% 통과 시 Credly 발급, CDP 크롬으로 조작"
metadata: 
  node_type: memory
  type: project
  originSessionId: a87a3b3d-2107-4dc7-b8cd-e29491a12b20
  modified: 2026-08-13T15:22:45.505Z
---

디지털 뱃지 수집 ([[cofathon-application]] 원티드 뱃지 종결 후 확장, 2026-08-14 시작):

- **계정**: AWS Builder ID = rainstorm0907@gmail.com **구글 연동 가입** — 로그인 시 구글 패스키 확인 필요. Skill Builder 무료 계정.
- **등록 완료(8/14)**: "AI Driven Development Lifecycle Knowledge Badge Readiness Path (한국어)" — 9개 AI-DLC 모듈(4h19m) + 뱃지 평가 1h. 62개 뱃지 과정 중 유일한 AI 도메인, 우진님 AI 오케스트레이션 서사와 정합. URL: https://skillbuilder.aws/learning-plan/G9T931Z4W2/ai-driven-development-lifecycle-knowledge-badge-readiness-path--/BSDR7RJ68E
- **남은 것**: ① 수강+평가(80% 이상)는 본인 몫 — 시험 대리 금지, 요약노트 지원은 가능 ② 통과 시 Credly 메일 도착 → Credly 계정 생성(본인)·뱃지 수령·링크드인 연동. Credly 메일 감시는 Gmail API로 가능.
- **조작 경로**: CDP 크롬([[agent-browser-headed-when-user-facing]]) — `~/.config/agent-real-chrome` 프로필, 포트 9222, `agent-browser --cdp 9222 --session realchrome <cmd>`. Skill Builder 로그인 세션 유지됨.
- 주의: AWS 정식 계정 가입(signin.aws.amazon.com/signup, 카드 필요)과 혼동 금지 — 뱃지는 Builder ID로 충분. 유료 자격증(Certified Developer 등)은 기각, 필요 시 별도 판단.
