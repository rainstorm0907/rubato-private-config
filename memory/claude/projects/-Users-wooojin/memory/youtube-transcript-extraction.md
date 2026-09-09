---
name: youtube-transcript-extraction
description: "유튜브 영상 내용이 필요할 때 WebFetch는 무용지물, uvx yt-dlp로 자막 받아 서브에이전트에 읽히는 경로"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4145efd8-cba9-47a1-8d9e-48aa99c8e627
  modified: 2026-08-08T11:37:07.572Z
---

유튜브 영상 내용을 알아야 할 때 WebFetch는 푸터 네비게이션만 반환해서 제목·설명·자막 어느 것도 못 가져온다. 대신:

- 메타데이터: `uvx yt-dlp --skip-download --print "%(title)s | %(channel)s | %(upload_date)s | %(duration)s"`
- 검색: `uvx yt-dlp --skip-download --flat-playlist --print "..." "ytsearch30:쿼리"` — 웹 검색보다 최신 영상을 훨씬 잘 잡는다
- 자막: `uvx yt-dlp --skip-download --write-auto-subs --sub-langs "en.*" --sub-format vtt`

yt-dlp는 설치돼 있지 않지만 `uvx`(`~/.local/bin/uv`)가 있어서 영구 설치 없이 바로 쓴다. "No supported JavaScript runtime" 경고는 자막 추출엔 영향 없다.

- 댓글: `--skip-download --write-comments --extractor-args "youtube:max_comments=150,all,50"` → info.json의 comments[]. 비인증 상태면 "Sign in to confirm you're not a bot"으로 전량 실패하는데, **`--cookies-from-browser chrome`을 붙이면 통과**한다(2026-08-08 확인, 28영상 4,223댓글). 이때 player client는 기본값(android_vr) 유지 — `player_client=web`이나 `tv`를 지정하면 오히려 실패. 실패가 반복되면 차단이 아니라 그 영상이 댓글을 꺼둔 경우도 있으니 구분할 것.

주의: 자동 자막 VTT는 롤링 중복 라인 때문에 원본의 3~4배로 부풀어 있다. 중복 제거 후 한 줄 텍스트로 만들면 1.4MB → 29k words 수준이 된다. 그 상태로도 크니 컨텍스트에 직접 올리지 말고 서브에이전트에 읽혀서 구조화된 보고만 받는다. 자동 자막은 고유명사를 음성적으로 뭉개므로(PEKKA→pecka) 에이전트 브리프에 "문맥으로 원래 이름을 추론하라"를 명시한다.

관련: [[browser-automation-policy]]
