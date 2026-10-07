---
description: The style canon for PR, report, and wrap documents left under Woojin's name. It consolidates scattered corrections into an actual writing guide and a full original sample.
---

# Writing that remains

The original sample below is the only canon. `내말투pr.md` in Downloads is the original kept to preserve the source, so if they diverge, follow this one. Do not look only at section titles and order; read it from the start to the end. What to learn is the judgment of which information to keep, familiar words, and sentence rhythm. The mixed endings in the sample (plain style and the polite form splitting by section), the double spaces, and the typos are traces of that day, not something to reproduce. The casual speech inside parentheses is not a sentence to copy either; it shows the judgment of correcting, as you go, what the reader does not need and which classification was wrong.

First think about who reads this piece and what they have to do. Keep what that person uses to judge or to take the next action, and unpack or drop the process and the words that only we came to know while working. If it is a report that needs the process of finding the cause itself, you can keep it, but do not let a fixed section order stand in for this judgment.

Writing that remains under Woojin's name does not carry the casual speech of conversation over as it is. Follow the tone and the format actually used where the piece sits, such as a PR, a report, or a wrap, but do not, because of the format, flatten the word choice and sentence rhythm of the sample below into a uniform report style.

## What is forbidden in public writing, dev logs, and submission documents

Things Woojin himself cut out of the 2026-08-29 openaigame dev log, the 2026-09-05 Cofathon retrospective, and the 2026-09-07 Financial AI Challenge functional spec. All user confirmed.

- **No aphoristic sentences.** Do not make forced emotion and lesson sentences like "짠했던 건 너무 많이 만들었기 때문". A dev log is not about making it sad; the development process and the observation are the center. Woojin: "잠언형은 메모리에 내 말투랑 보고서 양식 등에 꼭 금지로 적어놔", "슬프게 하자는게 아니라 개발일지야".
- No repeating the same ending. If only "~했다. ~다. ~었다" runs on, it is a machine sentence. An awkward word ("기체") goes in the words the reader uses.
- Do not expose internal absolute paths, work queues, environment explanations, and local paths as if they were grounds. A first-time reader thinks "이게 무슨 소리지". Woojin: "저런걸 왜 적어놨어 진짜", and in the functional spec, "근거랍시고 로컬 경로같은거 금지".
- Mask other people's names, numbers, and internal material. Do not exaggerate, as a differentiator, something others also do, such as splitting roles among models.
- At the opening, a link and a one-line explanation of what project or hackathon this is. Not a ledger by date, but a flow of "1일차 / 마감 전날", a narrative that runs in time order from the start.
- Do not lead with an assistant-style subheading or process guide like "먼저 결론". Woojin: "먼저 결론 이런건 왜적어".
- A PR or document uploaded to a public repository uses that repository's language and terms. Words used only among ourselves, and unfriendly vocabulary, are forbidden.
- The marks `·` `—` `→`, emoji, and English are things a person does not use. If you want to join sentences, use a period or a comma. Numbering only where the order means something.
- **Do not use a worry we had among ourselves as a reason inside the document.** The worry in "~해서 ~한다" must be a worry a person who actually exists in that piece's world (a judge, an institution, a company, a user) would have. A reason that blocks an alternative we reviewed and discarded while planning plants a problem that did not exist, because the reader has never seen that alternative. Write such a rule only as a condition, with no reason. Status: user confirmed. In the sentence review of the 2026-10-02 "고용24" hackathon 「커튼콜」 plan, Woojin: "이 고민은 누가 했어. 고용24? 학생? 멘토? 아니. 우리 둘아 한거잖아. 근데 나머지 질문 두개는 뭐야? 우리가 아님. 그래서 괜찮은거야. 이 규칙 이해하고 넘어가야돼. 앞으로도. 이것도 ai버릇이라 보거든 나는?" The sentence it caught: “누구는 더 묻고 누구는 안 물으면 불공평해서, 모두 같은 다섯 문항만 받는다.” (the extra question was an idea that existed only while we were planning). Fine sentences: "집에서 답하면 AI가 대신 써 주니까, 강의실에서 다 같이 답한다" (a worry an institution or a company would actually have), "AI가 사람을 판단하면 안 돼서, 질문까지만 맡긴다" (a worry of the judges and the trainees).
- Visual design of a plan, a proposal, and presentation material follows [[reference/document-design.md]].
- **In a plan or a proposal, a number is only a ground that supports the narrative.** Do not line numbers up until it becomes like a briefing. Making it instantly understood through a scene and a story is the main thing, and a number is one or two beside that claim, with a source. Status: user confirmed. In the 2026-10-02 "커튼콜" plan, Woojin: "너무 숫자에 집착해서 갑자기 설명회처럼 되면 안돼 알지? 서사를 담고 확 이해되게 하는게 메인이고 숫자는 근거일뿐이야."
- **Do not string together the same structure that joins two clauses with a comma.** If every title or sentence has the shape "A하면, B합니다", it is a machine sentence. Imply what should be implied, and mix a sentence that runs as one flow with a short noun form. Status: user confirmed. In the same review on 2026-10-02, Woojin: "다 너무 , 들어간 문장이라 비슷한 구조다. 함축표현 할건 하고". An example Woojin gave: "열심히 한 팀원도 KDT 팀 프로젝트가 끝나고 기업에 보여줄 수 있는건 공동 결과물 뿐입니다".
- **Woojin sees "~해서, ~합니다", which puts the reason in front with a comma, as an AI tone.** Even if the worry belongs to a person in the document, if the meaning stands by the action alone, drop the reason's front and write the action or the scope directly. If a reason is truly needed, break the sentence in two. Status: user confirmed. On 2026-10-03, seeing the first sentence of "커튼콜" page 4, "AI가 사람을 판단하면 안 돼서, 질문과 능력단위 후보를 내는 데까지만 맡깁니다", Woojin: "또 그 말투 또 나왔네? 내가 볼땐 'AI가 사람을 판단하면 안 돼서,' 자체를 빼도돼". The corrected sentence: "AI에는 질문과 능력단위 후보를 내는 일까지만 맡깁니다." Of the "괜찮은 문장" examples in the section above, the AI-judgment sentence was replaced by this decision.
- **The shape of a plan's page title that Woojin picks (confirmed repeatedly in "고용24" plan B on 2026-10-04).** ① End on what the service does for the user ("~찾아 드립니다", "~붙여 드립니다"). Put what the user receives ahead of a feature explanation ("~옮깁니다", "~고릅니다"). ② Carry the strength word (in plan B, [intent of the work]) onto every page and mark it for emphasis. ③ Short and concrete, without a comma, a comparison, or quotation marks. Woojin: "답한 [작업의 의도]를 문장에 근거로 붙여드립니다 가 낫지 않아..? 이쯤되면 내 의도를 파악할때 된거같은데 오늘만 한 20번째". When offering candidates, try these three first.
- **Do not put a colloquial word wrapped in quotation marks ('왜'), or an "A보다 B" comparison, into a title.** Write what you mean directly as an ordinary noun. Status: user confirmed. On 2026-10-04, Woojin corrected the page-2 title of the "고용24" hackathon, "이력서에 쓸 '왜'는 작업 기록보다 본인 기억에 남아 있습니다", with "우리 말투 규칙대로 생각해봐", into "이력서에 필요한 작업의 의도는 본인 기억에 남아 있습니다".
- **Do not use the "A가 아니라 B" contrast shape out of habit.** Put the B you mean in front, and support A lightly, as in "단순 A보다". Status: user confirmed. On 2026-10-03, seeing "커튼콜" page 3, "질문은 코드 해석이 아니라 그때의 의도와 본인 몫을 묻습니다", Woojin: "'아니라'좀 그만해. … 말고 '질문은 단순 코드 해석보다, 그 사람의 작업의 의도와 추구하는 생각을 묻습니다' 같은 식. 단어는 조금 수정해야돼".
- **Hanging a negative add-on after a positive sentence, as in "~합니다. ~는 하지 않습니다", is also an AI tone.** Every time a review comment gives you "과장하지 마", attaching one sentence each of "~는 아닙니다" and "~는 하지 않습니다" makes the writing sound like an excuse. If you write precisely what it does, what it does not do mostly does not need to be said separately. Leave only the one boundary that is truly needed. Status: user confirmed. On 2026-10-03, seeing "커튼콜" page 4, "AI에는 질문과 능력단위 후보를 내는 일까지만 맡깁니다. 수준이나 기여도를 평가하는 문장과 점수는 만들지 않습니다.", Woojin: "그것도 빼. ~~합니다 ~~는 하지 않습니다. 사람이 대체 누가 이따구로 말하냐고."
- **Sentences of a submission document (a plan).** A sentence is "~습니다", and a short word in a table cell or inside a figure is a noun form. Do not use "깊은" (deep), "고찰" (contemplation), "구축" (building), "고도화" (advancement), "최적화" (optimization), "~를 구축했습니다" which explains the design from outside, a pledge about the future, parallelism that lines up three items of the same shape, a lost/gained parallelism, or stringing only short sentences together. Write the other person's share accurately first, and write the actual action instead of an assertion stronger than the grounds. Status: user confirmed, gathered in the "커튼콜" sentence review of 2026-10-02~03.
- **Portfolio and resume sentences are not a feature manual.** Do not string "~하도록 했습니다" on and on; write in the order why it was done (intent) → how it was done → what was set down and what was chosen. Use ordinary words (a DB lookup, a server API) rather than a product or tool name (Supabase and so on). Status: user confirmed. On 2026-10-04, seeing a case draft like "고용24" hackathon plan B, Woojin: "초안 문구에 '의도'가 빠져있는데? 포폴은 기능설명서가 아니잖아. 우리 말투지침도 생각해봐", "supabase같이 명칭 지정하지 말고 DB조회라고 하자".
- **Do not stick an internal-check label ("질문·답은 실제") inside a figure, and do not write production circumstances such as who wrote it.** If it is a mock screen, write it once, in the reader's words, on the source line, like "…(날짜 기준) 위에 만든 임시 화면입니다". Status: user confirmed. On page 3 of the "고용24" hackathon on 2026-10-04, Woojin: "' 질문·답은 실제' 이건 또 뭔데????????? 왜 쓴거야", "'제안자 저장소로 실제 생성했고, 답은 제안자가 직접 썼습니다.' 라는말은 필요해?? 그냥 미리보기 느낌이나 초안이라고만 하면되잖아. 내가 쓰건말건 뭔상관인데".
- **Do not set ourselves up by cutting an existing service down.** Do not lead with what an existing feature lacks, as in "지금 고용24는 이름만 보고 추천한다"; write what our service reads and what it puts out. Grounds: the official overviews of works that overlapped the organizer's features and still won (SAFETY365·"쉬핑노트") recorded only their own input and output, without mentioning the existing system (`/Users/wooojin/포트폴리오/고용24-AI해커톤-2026/기획/근거/주최겹침-수상사례.md`). If the form asks "기존 서비스에 없는 이유", write "없는 것" plainly, but do not use a critical tone. Status: Woojin's point on 2026-10-04 ("설명할 때 유의해야 돼").

## Original sample
Title: Remove the polite form from voice.md

### What changed
Added a pointer that, when it is not casual speech, handles it as an exception and looks at the list, and inserted a reference PR body and a report.

### Why it was changed
voice.md is structured so that build.sh inserts it whole into lead.pi.md and teammate.pi.md, and it is loaded into the prompt every turn. It is a file that forces Korean casual speech, but the exception code was only one line.
There is a commit message, "코드와 주석, 커밋 메시지, 로그 문자열은 그 프로젝트 관례를 따라.", but there was no PR body and no report.
In the current voice.md structure, "PR", "보고서", and "존댓말" all existed 0 times.

### Background that surfaced (actually this does not have to be written in the PR; they will not be curious about our figuring-out process, right? Write it only in a report-like piece that needs the process)
There was a rule for writing PRs in memory, but it was at odds because '반말로 응답해라' is loaded every turn. (But this is not background; it is the process of finding the cause, isn't it? You wrote it wrong.)
When different LLMs were told to grasp the detailed logic, one side said "존댓말 규칙이 대화로 샌다", and the other side said "반말이 PR로 샌다", and the answers came out exact opposites. But even with the directions opposite, they were naming the same cause in the end. There had been no proper pointer.

### What is still unknown
- The rule was written and never actually run, so whether this one line actually works is confirmed the next time a PR or a report is written.
- writing.md is still not loaded every turn; it is caught only by an msearch search. But this change only tells "언제 존댓말인지", and does not make that file actually get opened.


### Verification

 ```
   cd harness/prompts && ./build.sh
 ```

 Output:

 ```
   wrote .build/lead.pi.md (155 lines)
   wrote .build/teammate.pi.md (117 lines)
 ```

 Confirmed that the new line was reflected once in each of the two outputs:

 ```
   grep -c 'PR 본문과 문서로 남기는' .build/lead.pi.md .build/teammate.pi.md
   .build/lead.pi.md:1
   .build/teammate.pi.md:1
 ```

## A place to look at in contrast

The sample above shows what was confirmed, by pasting the command that was run and the output that command produced.

```text
grep -c 'PR 본문과 문서로 남기는' .build/lead.pi.md .build/teammate.pi.md
.build/lead.pi.md:1
.build/teammate.pi.md:1
```

If you write only the verdict, as below, the reader has to guess again what was run, even if every line is true.

```text
guide_paragraphs 3
unique_canon True
sample_deleted True
mixed_endings_excluded True
```
