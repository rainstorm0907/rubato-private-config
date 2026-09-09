---
name: absolute-file-paths-output
description: 사용자에게 보여주는 파일 경로는 항상 절대 경로로 — cmux ⌘클릭으로 바로 열리게
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a87a3b3d-2107-4dc7-b8cd-e29491a12b20
  modified: 2026-08-13T09:40:14.703Z
---

우진님에게 파일을 언급할 때는 **항상 절대 경로**로 적는다 (`wanted-profile.png` ✗ → `/Users/wooojin/Downloads/원티드-프로필-뱃지없음.png` ✓). 한 줄에 경로만 단독으로 두면 클릭하기 더 좋다.

**Why:** 우진님 터미널은 cmux(0.64.5+)라 절대 경로는 ⌘클릭으로 미리보기가 바로 열리는데, 파일명만 적으면 위치를 못 찾아 클릭이 안 된다. 2026-08-13 파일명만 적었다가 "클릭으로 여는 법 없어?"를 받고 확정한 규칙.

**How to apply:**
- 스크린샷·산출물·다운로드 파일을 보고에 넣을 때 절대 경로 명시. 사용자용 산출물은 `~/Downloads`에 두는 관행([[hama-portfolio-pdf-pipeline]])과 결합.
- cmux 알려진 한계: tmux 세션 내부 클릭 불가.
- **file:// 링크는 OS로 넘어감** (issue #7104 수정, 2026-08-13 우진님 실측 확인): 폴더 `file:///.../` 링크 ⌘클릭 = Finder 열림. 파일 보고 기본 포맷 = 경로 한 줄(⌘클릭=미리보기) 끝에 ` [📂](file://폴더/)` 짧은 Finder 링크 덧붙이기. 폴백은 `open -R`.
