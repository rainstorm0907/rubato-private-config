---
description: The context-restoration scope and quality bar Woojin requires when handing a long session over to a new session.
---
# Handoff bar for a long session

- Status: user confirmed
- Date: 2026-09-02
- Context: A long Maplog session hit the session-lifetime compaction cap and is moving to a new session.

Woojin, original wording:

> “알겠어 일단 그렇게해주는데 진짜 빠짐없이 해줘. 원문을 다 넣으라는개 아니라 전전전전 컴팩션 전부터 가짘 핵심 컨택스트들 유지해야돼 우리 감성과 내가 계속해서 강조한부분들”

Applied bar:

- Do not hand over a single last compaction summary as it stands.
- Go back at least to before the most recent four compactions, and restore core decisions that later summaries dropped.
- Instead of dumping the full original, preserve the reasons for decisions, the discarded directions, the product feel, and the parts the user kept emphasizing, so the next session can make the same judgments.
- If the direction changed after the last compaction, do not treat the summary from before that as the source of truth.
- Hand over code, verification, and agent state together with the product judgment, and check that the new session actually understood.
