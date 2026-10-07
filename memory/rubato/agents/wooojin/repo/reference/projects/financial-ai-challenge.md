---
description: Result of the 2026 Financial AI Challenge (Financial Security Institute, Woojin + his older brother Wooyong) — did not advance — and the product decisions that survive.
---
## Result

- Submitted at 10:00 on 2026-09-07. Service name **"온전"** ("소명" → "풀림" → "온전", his brother confirmed it in the early morning of 9/7). Team Woobrothers (Jeong Wooyong, Jeong Woojin, Yoo Suchan).
- Did not advance. Woojin: "온전 떨어졌어."
- Deploy: https://daker-hackaton.keepitmello.workers.dev (Cloudflare Containers, deploy forbidden after 10:00 on 9/7). Repository `keepitmello/daker-hackaton`. Working copy `/Users/wooojin/App/daker-hackaton`.
- Submission: a 4-page plan PDF (3 implementation screens in section 7), an 11-page functional-spec PDF (7 implementation screens + an architecture figure). Drafts, research, and architecture originals of the submission documents are in the repository `docs/research/somyeong-r5/`.
- Contest facts: 1,371 participating teams, 781 submissions, top 11 teams by 100% internal closed judging → presentation judging on 10/13. Official board answers: no length or page limit, visual materials OK, an appendix is one file merged after the plan, commercial APIs and synthetic data allowed, only the submission URL counts.
- Final structure: browser (Next.js screens, transaction-history parser, localStorage 30 days) → Cloudflare Worker+Container → harness (session: Claude Opus 5 loop, 6 tools / case: pure TS incident file, form assembly, evidence search of 17 embedded items) → Anthropic, OpenAI (STT, embeddings), Fish Audio (TTS). No server storage.

## Product decisions that survive (user confirmed, apply to the next product too)

- **Conversation is the AI, confirmation is the user, assembly is code.** The AI only proposes fact candidates and has no confirm tool. Statement sentences are placed by code, in form order, from confirmed facts only. Woojin, 9/6: "사용자 발화로만 구성하게 되어있고 … 에이전트가 안붙였으면 해". Grounds: a document submitted to a bank must not give an AI-slop impression.
- **The service is not a place that gives an AI-completed statement.** Draft + blanks + the person's own edits. AI copy-editing (expression suggestions) is not done; it is a legal boundary. Woojin, 9/5: "우리가 직접 ai소명서를 제공하는 사이트는 아니야."
- **The panel is a memo slip that does not block progress even if unread** (the brother's view). Progress-rate numbers and remaining counts forbidden; only a current-step indicator allowed. Woojin: "패널이 사용자를 독려할지 압박할지 기존 회의가 맞아."
- **The safety-value gate is checked deterministically by code** (when a re-transfer or providing an authentication method is confirmed, automatic assembly stops; writing directly is still possible; it is not an accomplice judgment). Entering an empty writing room or the closing screen has no condition.
- **Citing a case goes only as far as "이런 사례가 있었다".** Do not write it like an official bank answer, no promise of outcome or period, and separate what was submitted from the result. Woojin: "겁먹지 않게. 귀찮지도 않게. 우린 도와주는 서비스니까."
- Forbidden phrases: "당신은 ○○유형" / "풀려요" / "N개 남음" / "공고 기다리세요" / "소액이면" / "유리·불리" / "제7조 ○호" / "필수". The marks `·` `—` `→`, emoji, and English are forbidden on screen. All service screens and documents.
- Terms: "명의인" (account nominee; our user; "피해자" forbidden), "송금인" (sender), "문제 입금" (problem deposit), "소명서" (statement; the "이의제기 사유" field of attached Form No. 4, "별지 제4호서식"). Incident hypotheses A~G are an internal classification, forbidden on screen.

## Lessons

- **Writing the submission first, and making that not a lie, is the development.** This time implementation came first (9/3~5) → all of 9/6 was spent redesigning the narrative, the copy, and the demo → documents in the early morning of 9/7. The order should have been reversed. The detailed procedure is `system/working-rules.md` "공모전·해커톤을 시작할 때".
- **The last half-day is contrasting code ↔ document ↔ figure.** Figure 8 of the functional spec went in as an old version (sonnet-5, 5 tools) and was caught 30 minutes before submission. The same cause was the lead not looking at main and wrongly pointing out "RAG 아니다", when his brother had pushed evidence search (RAG) and Opus 5 to main overnight.
- **Screen-work agents:** At the time, both Grok high and Sol sometimes only read, more than 30 times, on screen work and did not write. Specifying an edit-start call order in the brief then was a one-off prescription, and now, per `system/working-rules.md`, check the blocked cause and the allowed scope first. Given only research + file writing, Grok succeeded. Aside browser work failed twice in a row in a child agent → the lead did it directly.
- **"안 눌려" is a gate without an explanation.** If the user says a button does not press, it is not a bug; a condition is not shown on screen. Remove the condition or show it.
- Transition screens: after all three rounds of sheet tuning were discarded, it worked in one pass with the flow that had passed on the home (role sentence → lock the criterion → reference "가져올1/버릴1" → imagegen, 3 images, one variable → Woojin's choice → implementation). Two tuning failures on the same surface → evidence for the suspect-the-layer rule.
- Architecture figure: a box gets only a name + one line of technology (AWS, C4, Hama portfolio density). Reason sentences, paths, and safety-gate explanations belong in the body. Ratio 2.3~2.7:1 against an A4 body width of 170mm, with no outer margin.
- Delivery of document fragments and images worked well via the Telegram bot (`~/.claude/channels/telegram/.env`, chat 7389033218). `sendMessage` is `text@file`, and images are `sendDocument`.
