# Latency & token budgeting

![Badge](https://img.shields.io/badge/Pattern-Budgeting-2563eb) ![Badge](https://img.shields.io/badge/Goal-Predictable%20Costs-0f172a)

## Quick take
If you don’t set budgets, RAG and tools quietly turn your app into a slow, expensive system.
Budget each step (router, retrieval, synthesis, draft) and enforce caps.

## When to use
- You care about chat UX (p95 matters).
- Retrieval or tool calls are a big part of your workload.
- Costs are creeping up and “why” is unclear.

## Avoid when
- You don’t measure latency/tokens yet (instrument first).
- Your app has fixed, tiny prompts and no tools/retrieval.

## Minimal flow
- Pick budgets (example: p95 target + max tokens per step).
- Route early so `rag_chat` is not the default.
- Bound retrieval (`top_k`, chunk size, max doc tokens).
- Synthesize before drafting (notes with a strict max size).
- Cap tool outputs and store only the fields you need.

## Starter budget table
| Step | Budget idea | Why |
|---|---|---|
| Router | tiny prompt, small/fast model tier | keeps decisions cheap |
| Retrieval | `top_k` + max tokens | avoids “context explosion” |
| Synthesis | strict max chars/tokens | protects the draft prompt |
| Draft | highest quality budget | where quality matters most |

## Failure modes
- You optimize averages but ignore p95 (symptom: “randomly slow” UX).
- Retrieval is unbounded (symptom: prompt grows until it breaks).
- Too many helper calls (symptom: 3 small calls cost more than 1 good call).

## Checklist (copy/paste)
- [ ] You track p50/p95 latency per step (router, tools, draft).
- [ ] Token budgets exist per step and are enforced.
- [ ] Retrieval is bounded and audited (top-k + max tokens).
- [ ] Router uses a smaller/faster tier than drafting (when using an LLM router).
- [ ] Tool outputs are summarized/structured before entering context.

## Links
- Official docs:
  - https://langchain-ai.github.io/langgraph/
- Internal:
  - `decision-guides/router-decision-table.md`

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-07%20Context%20Window-64748b)](07-context-window-trim-summarize.md)
[![Next](https://img.shields.io/badge/Next-09%20Reliability-2563eb)](09-retries-fallbacks-guards.md)
