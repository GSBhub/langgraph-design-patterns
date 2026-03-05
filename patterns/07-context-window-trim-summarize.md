# Context window control (trim + summarize)

![Badge](https://img.shields.io/badge/Pattern-Context%20Window-2563eb) ![Badge](https://img.shields.io/badge/Goal-Keep%20Prompts%20Small-0f172a)

## Quick take
More context is not always better: it increases latency/cost and can reduce instruction-following.
Keep prompts bounded with “last N turns + running summary + compact tool outputs”.

## When to use
- Sessions are long or multi-step (tools, retries, follow-ups).
- Token usage and latency grow over time per user.
- You see missed tool calls or instruction drift on long threads.

## Avoid when
- You need verbatim history for auditing/compliance.
- The task requires exact phrasing across many turns.

## A simple prompt packing recipe
```text
1) system rules
2) durable memory facts (optional)
3) running summary (short, factual)
4) last N turns (bounded)
5) newest tool outputs (structured + capped)
```

## Minimal flow
- Track token/message budget per request (hard cap).
- Keep last `N` messages (small and predictable).
- Maintain a running summary (refresh on threshold).
- Store stable facts separately (preferences, IDs, decisions).
- Build prompts using the packing recipe (and enforce caps).

## Failure modes
- Summary drift (symptom: model “remembers” wrong facts).
- You trim away the one instruction that matters (symptom: policy violations).
- Tool output dominates context (symptom: slow + unreliable turns).

## Checklist (copy/paste)
- [ ] Prompt size has a hard cap (tokens/messages) and is enforced.
- [ ] Summary is short, factual, and refreshed on a schedule/threshold.
- [ ] “Must keep” items are explicit (policies, IDs, goals).
- [ ] Tool outputs are structured and bounded before entering context.
- [ ] You track prompt size and latency over time (p50/p95).

## Links
- Official docs:
  - https://langchain-ai.github.io/langgraph/
- Internal:
  - `patterns/08-latency-token-budgeting.md`

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-06%20Long--term%20Memory-64748b)](06-long-term-memory-store-namespace-key.md)
[![Next](https://img.shields.io/badge/Next-08%20Budgeting-2563eb)](08-latency-token-budgeting.md)
