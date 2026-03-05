# Memory decision table

![Badge](https://img.shields.io/badge/Decision%20Guide-Memory-2563eb) ![Badge](https://img.shields.io/badge/Format-Decision%20Table-0f172a)

## Decision table

| Need | Use (short-term checkpoint vs long-term store) | Keying strategy (thread_id / namespace) | Retention strategy | Common mistakes |
|---|---|---|---|---|
| Resume an in-progress run after retries/restarts | Short-term checkpointing | `thread_id` (one per conversation) | TTL by age, max size, and/or delete by `thread_id` | Storing huge tool payloads; no cleanup plan |
| Keep “where are we in the graph?” across turns | Short-term checkpointing | `thread_id` | Same as above | Changing `thread_id` between requests |
| Remember user preferences across days/weeks | Long-term store | `user_id` + `namespace` (example: `prefs`, `profile`) | Retention policy + deletion path | Storing raw transcripts instead of compact facts |
| Very long conversations without prompt bloat | Long-term store + trim/summarize | `user_id` for facts; `thread_id` for short-term run state | Summary refresh cadence + bounded last `N` | Summaries drift; “memory” accumulates contradictions |
| Human escalation handoff context | Long-term store (optional) + handoff package | `thread_id` for the ticket; `user_id` for stable facts | Keep only what support needs; redact sensitive data | Saving PII without policy; storing too much context |

## What to store
- Stable user preferences (“prefers short answers”, “timezone”, “role”).
- Compact summaries of ongoing projects/goals (factual, short).
- Verified identifiers you need to operate (account ID, org, plan tier) if policy allows.
- “Decisions already made” (so you don’t re-ask every time).

## What NOT to store
- Raw full transcripts by default (too large and not “memory”).
- Unbounded tool outputs (HTML, logs, huge JSON blobs).
- Secrets or credentials (API keys, passwords, tokens).
- Sensitive data unless you have a clear policy, consent, and deletion story.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-Deterministic%20vs%20LLM-64748b)](deterministic-vs-llm-decision-table.md)
[![Next](https://img.shields.io/badge/Next-Router%20Decision%20Table-2563eb)](router-decision-table.md)
