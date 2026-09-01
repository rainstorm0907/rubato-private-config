---
name: consult
description: >-
  Use the logged-in ChatGPT web UI through Aside for public-web research,
  current source checks, implementation strategy, architecture validation,
  debugging, and second opinions. Run it directly with one command in the
  configured Woojin project. Quick is GPT-5.6 Sol at 매우 높음; deep is Sol Pro.
---

# Consult through Aside

ChatGPT web as an outside consultant, driven from the middle of a work session. Aside supplies the logged-in browser; this session owns the question, the packet, the verification, and the synthesis.

The consultant sees nothing but the packet — no repository, terminal, prior messages, or local files.

## Mode

- `quick` (default): GPT-5.6 Sol, `매우 높음`. Every ordinary consult.
- `deep`: GPT-5.6 Sol, `Pro`. Only for precise search — when the answer depends on finding and weighing current external sources. `Pro` is the only tier `deep` may use; never substitute another level to save time.

Do not rerun the same packet hoping for a nicer answer.

These settings were verified against the live ChatGPT UI on 2026-09-01:
`매우 높음` is performance step 4 of 5 and `Pro` is step 5 of 5. Do not copy the
public portable skill's `중간` fallback into this installation.

## Rules the runner cannot enforce for you

- Read the finished packet once for secrets, credentials, and unrelated private content before sending. Include what changes the answer, nothing more.
- The answer is provisional. A decision-critical claim becomes fact only after this session checks the primary source, repository evidence, or a test.
- Ask for the report in Korean, leaving structure and depth to the consultant:
  > 답변은 한국어 보고서로 작성해 주세요. 문제에 맞는 구조와 표현을 자유롭게 선택하되, 자연스럽고 읽기 쉽게 설명해 주세요. 기술 용어와 영문 표현은 도움이 될 때 자유롭게 사용해도 됩니다.

Everything else — personal `Chat` surface, Pro account, model and reasoning level, the configured Woojin project, one owned tab, tab baseline restore, no duplicate submission — is enforced by `run_aside_consult.py`, which fails closed before sending.

## Direct command

Always start here. Run from the repository root:

```bash
S=~/.agents/skills/consult/scripts

python3 $S/consult.py \
  --question "<one exact question>" \
  --files <relevant-files>
```

Launch this command in the harness background terminal from the start
(`run_in_background:true`). Once it has started, do not poll it, keep the turn
open, or schedule wakeups. If no independent work remains, end the turn and let
the background completion notification wake the session. The background process
owns submission, all collection retries, and response persistence.

Use `--deep` only for source-heavy precise research. Use `--dry-run` to verify the
Woojin project, model, and reasoning level without sending. The command builds the
packet, prepares the prompt, runs Aside, saves the answer and evidence under
`.consult/`, and preserves the stable per-account checkpoint under
`~/.config/consult/sessions/`.

The direct command submits once in a short Aside connection, then collects through
fresh 30-second connections. A collector disconnect never resends the prompt.
Quick allows 20 collection attempts; deep allows 120. Override these only with
`--collect-window` and `--collect-attempts`.

Successful packet preparation, submission, and intermediate collection attempts
stay silent. The background job emits only the final response path or the final
failure, so waiting does not add retry chatter to the parent session context.

Do not call `aside exec`, `aside repl`, `agbrowse`, or the three lower-level
scripts directly for an ordinary consult. They are implementation details and
recovery tools.

The low-level runner still defaults to 600s (quick) and 3600s (deep);
`--timeout` overrides it for advanced recovery.

## Recovery and continuation (advanced)

The direct command above is the only ordinary entry point. Use the lower-level
runner below only after a submitted consult needs recovery, delayed collection,
or a narrow follow-up.

A `deep` consult can be submitted now and collected later:

```bash
python3 $S/run_aside_consult.py --mode deep ... --send-only   # sends, records, exits
python3 $S/run_aside_consult.py --resume                      # collects the saved conversation
```

After an accepted `--send-only`, or when collection fails after submission, the runner intentionally leaves its owned tab open so generation can finish. The checkpoint records `ownedTabLeftOpen` and `ownedTabTargetId`; `--resume` reuses that tab when it is still present and closes it after successful collection.

`--dry-run` walks the whole pre-send gate — project, account, model, reasoning level — and stops without sending. Use it after a ChatGPT UI change, or whenever a run failed and you want to know whether the gate or the send broke.

## Follow-up

Only when the original packet is still accurate and the question is narrow:

```bash
python3 $S/run_aside_consult.py --mode quick \
  --follow-up "<narrow question about the previous answer>" \
  --response-output .consult/consult-followup-response.md
```

Follow-up always uses the conversation URL already stored in the session checkpoint. `--session` may only repeat that same URL; it cannot redirect a follow-up to another conversation. Material change in the facts means a new packet, not a follow-up.

## Exit codes

`0` complete · `1` failed with nothing usable · `2` invalid input or missing project config · `3` partial response saved · `4` **already submitted — resume it, do not resend** · `5` another run holds this session file.

`4` usually means an **earlier consult — often from another session — was never collected**, not
that your question is a duplicate. The checkpoint is one file per account under
`~/.config/consult/sessions/`, and any unfinished record in it blocks every new consult until it is
closed out. Read the recorded `conversationUrl` before acting: it is likely someone else's question.

Recovery, in this order:

1. `--resume --response-output <scratch path>` — collects **that earlier question's** answer, not
   yours, so send it somewhere disposable. This marks the record `complete` and closes the owned tab.
2. Re-run your own consult normally. The gate is now clear.

If the status is `sending` with no URL, stop: the send may have gone through without the URL being
captured. Look at the ChatGPT project in a browser before doing anything, and never resend
automatically. `--new` starts a second conversation alongside the blocked one; it is for when you
deliberately want both, not for unblocking yourself — step 1 is the way to unblock.

`5` means a second consult tried to use the same session file while the first was still
running. Wait for the first to finish; never work around it by pointing `--session-file`
somewhere else, because the duplicate-submission guard lives in that one file.

## Setup

The runner starts Aside Browser itself when it is closed and waits for its daemon, so no consult depends on the browser already being open. It only asks for help when Aside cannot be reached at all.

New conversations are born inside a configured ChatGPT project; without it the runner refuses to send. One key in `~/.config/consult/consult.env`:

```
CONSULT_PROJECT_URL=https://chatgpt.com/g/g-p-<id>/project
```

## References

[references/web-automation-boundaries.md](references/web-automation-boundaries.md) for what the browser side may and may not do. [references/after-advice.md](references/after-advice.md) once the answer is in hand. The `aside-browser` skill documents the REPL itself.
