# After Advice Workflow

Use this after receiving a response from the external consultant.

1. Extract concrete claims from the advice.
2. Verify each claim against repository facts, docs, tests, or current web sources if needed.
3. Classify recommendations:
   - Apply now
   - Investigate with a small experiment
   - Reject because it conflicts with repo constraints
   - Needs more context or follow-up
4. Make the smallest safe change first.
5. Run the relevant tests and commands.
6. Summarize:
   - what advice was used
   - what was changed
   - what was rejected and why
   - test results
   - remaining risks

Do not treat the consultant as authoritative when its assumptions conflict with the codebase. Repo facts, user constraints, and passing tests win.
