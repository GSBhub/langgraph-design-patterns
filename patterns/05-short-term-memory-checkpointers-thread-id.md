# Short-term memory (checkpointers + thread_id)

![Badge](https://img.shields.io/badge/Memory-Short--term%20(thread)-2563eb) ![Badge](https://img.shields.io/badge/Concept-Checkpointer-0f172a)

## Quick take
If a multi-step run restarts, you don’t want to redo tools or lose “where we were”.
Use a stable `thread_id` and checkpoint only the minimum state needed to resume.

## When to use
- Your workflow has multiple steps (router → tools → synthesis → draft).
- You care about resumability across retries/restarts.
- You want consistent “graph progress” per conversation.

## Avoid when
- Your workflow is single-step and always recomputable.
- You cannot store conversational state (policy constraints).

## Flow (minimal)
```mermaid
flowchart TD
  I[Invoke graph] --> K[config: thread_id]
  K --> L[checkpointer load]
  L --> N[run nodes/edges]
  N --> S[checkpointer save]
  S --> O[return output]
```

## What to checkpoint (keep it small)
- Bounded `messages` (last N turns, not the whole transcript).
- The last `route` + `reason` (for debugging and replay).
- Tool outputs needed for the next node (structured, size-capped).

```python
# Conceptual: a stable ID per conversation/session
config = {"configurable": {"thread_id": session_id}}
```

## Failure modes
- No retention plan (symptom: store grows forever).
- Checkpointing raw payloads (symptom: storage and prompts bloat).
- Unstable `thread_id` (symptom: “memory resets” between requests).

## Checklist (copy/paste)
- [ ] `thread_id` is stable per conversation.
- [ ] Checkpointed state is bounded (messages/tool outputs have caps).
- [ ] You can delete checkpoint data by `thread_id` (support + cleanup).
- [ ] Retention exists (age-based TTL and/or size limits).
- [ ] A replay path exists for debugging (same inputs + `thread_id`).

## Links
- Official docs:
  - https://langchain-ai.github.io/langgraph/
- Internal:
  - `decision-guides/memory-decision-table.md`

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-04%20Prechecks-64748b)](04-deterministic-overrides-regex-keywords.md)
[![Next](https://img.shields.io/badge/Next-06%20Long--term%20Memory-2563eb)](06-long-term-memory-store-namespace-key.md)
