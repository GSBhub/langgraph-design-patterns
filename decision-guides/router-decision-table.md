# Router decision table

![Badge](https://img.shields.io/badge/Decision%20Guide-Routing-2563eb) ![Badge](https://img.shields.io/badge/Format-Decision%20Table-0f172a)

<p align="center">
  <img alt="Router split hero diagram" src="../assets/hero.svg" width="860" />
</p>

## Decision table

| User query signal | Route | Why | Cost/latency impact | Notes |
|---|---|---|---|---|
| Explicit dissatisfaction or request to talk to a person (“talk to an agent”, “not happy”, “complaint”) | `escalate_human` | Support UX must be predictable; don’t “chat it away” | Low (skip RAG/tools) | Build a handoff package: summary, intent, key facts, contact info, timestamps |
| URL present and your product supports “analyze this link” | `normal_chat` | Deterministic URL tool-first is more reliable than hoping the LLM calls the tool | Medium (tool step), but controlled | Run URL tool-first pre-check → store extraction in state → then answer using that extraction |
| Asks for information that must be grounded in your docs/KB (“what does the policy say…”, “according to the docs…”) | `rag_chat` | Retrieval is required to be correct | Higher (retrieval + synthesis) | Bound retrieval: `top_k`, chunk size, max tokens |
| Mentions “my account/order/billing” but you don’t have the data locally | `escalate_human` | You can’t safely answer without an integration | Low | If you do have an internal tool, route to `normal_chat` and use the tool |
| Brainstorming, writing help, small talk, general Q&A | `normal_chat` | RAG is wasted work and slows UX | Lowest | Default route if uncertain; ask one clarifying question if needed |
| Ambiguous intent (“help me with this”) with no doc signal | `normal_chat` | Safer default; use a clarifier instead of guessing RAG | Low | Ask one targeted question (“Do you want docs/policy info or general advice?”) |

## Minimal router prompt rules
- Output must be exactly one of: `normal_chat`, `rag_chat`, `escalate_human`.
- Prefer `normal_chat` unless retrieval is clearly required.
- Choose `escalate_human` only for explicit human asks, dissatisfaction, or missing-required data.
- Do not answer the user; only choose a route and a short reason (1 sentence).
- If unsure, pick `normal_chat` and let the chat node ask one clarifying question.

## How much context to pass?

| Option | Pros | Cons |
|---|---|---|
| Current query only | Fast and cheap; less chance of “overthinking” | Can misroute follow-ups that depend on prior turns |
| Last `N` messages (usually 1–3) | Better for follow-ups and implicit references | Slightly slower; must trim/summarize to stay bounded |

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Next](https://img.shields.io/badge/Next-Deterministic%20vs%20LLM-2563eb)](deterministic-vs-llm-decision-table.md)
