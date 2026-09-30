---
description: Rubato 브라우저 작업은 공식 browser-cli·aside 스킬을 따른다. 개인판(abrowse/gbrowse/isearch)은 2026-09-29에 걷었다.
---
# Rubato 브라우저 라우팅

- 2026-09-29 우진: "브라우저는 공식으로 가보자." 개인 browser-cli 오버레이(abrowse/gbrowse/isearch, 종료 코드 판정)를 걷고 공식 `browser-cli`·`aside` 스킬을 쓴다.
- 근거: Opus·Astra xhigh 검토. 둘 다 로컬 도구의 쓸모는 인정했지만, Astra는 종료 코드 판정이 실제 방문을 증명하지 못하고(도구 이름을 셈) 래퍼가 권한 확인을 끈 채 도는 점을 짚었다.
- 스크립트는 `~/.agents/skill-backups/20260929T070651Z-personal-overlays/browser-cli/scripts/`와 rubato-private-config git 기록(3b82cf3 이전)에 남아 있다. 다시 쓰려면 공식 라우터 아래의 선택형 어댑터로 붙인다.
- 공식 browser-cli 는 cloak(9333/9334)·chrome-devtools 를 폴백으로 드는데 이 맥엔 없다. 실제로 막히면 그때 폴백을 정한다.
