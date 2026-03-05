# Cookbook (examples)

![Badge](https://img.shields.io/badge/Track-Python-3776AB?logo=python&logoColor=fff) ![Badge](https://img.shields.io/badge/Style-Graph--first-2563eb)

This folder contains the example milestones. Start from 00 and move forward.

| Progress | Example | Covers |
|---|---|---|
| ![Progress](https://img.shields.io/badge/Progress-1%2F9-0f172a) ![Badge](https://img.shields.io/badge/StateGraph-2563eb) | [00 — Hello StateGraph](00-hello-stategraph/README.md) | state → nodes → edges → compile |
| ![Progress](https://img.shields.io/badge/Progress-2%2F9-0f172a) ![Badge](https://img.shields.io/badge/LLM%20Node-0f172a) ![Badge](https://img.shields.io/badge/OpenAI-111827?logo=openai&logoColor=fff) | [01 — One LLM call](01-llm-call/README.md) | `get_llm()` + one clean LLM node |
| ![Progress](https://img.shields.io/badge/Progress-3%2F9-0f172a) ![Badge](https://img.shields.io/badge/Tools-0f172a) | [02 — Tools basics](02-tools-basics/README.md) | tool definition → tool call → answer with tool output |
| ![Progress](https://img.shields.io/badge/Progress-4%2F9-0f172a) ![Badge](https://img.shields.io/badge/Routing-0f172a) ![Badge](https://img.shields.io/badge/Prechecks-2563eb) | [03 — Router](03-router/README.md) | deterministic checks → router LLM → conditional edges |
| ![Progress](https://img.shields.io/badge/Progress-5%2F9-0f172a) ![Badge](https://img.shields.io/badge/Conditional%20RAG-0f172a) | [03b — RAG branch](03b-rag-branch/README.md) | retrieve only when the route is `rag_chat` |
| ![Progress](https://img.shields.io/badge/Progress-6%2F9-0f172a) ![Badge](https://img.shields.io/badge/Short--term%20Memory-2563eb) | [04 — Short-term memory](04-short-term-memory/README.md) | `InMemorySaver` + `thread_id` |
| ![Progress](https://img.shields.io/badge/Progress-7%2F9-0f172a) ![Badge](https://img.shields.io/badge/Long--term%20Memory-2563eb) | [05 — Long-term memory store](05-long-term-memory-store/README.md) | `InMemoryStore` facts + recall (prod note included) |
| ![Progress](https://img.shields.io/badge/Progress-8%2F9-0f172a) ![Badge](https://img.shields.io/badge/Context%20Window-0f172a) | [06 — Context window summarize](06-context-window-summarize/README.md) | trim + summarize |
| ![Progress](https://img.shields.io/badge/Progress-9%2F9-0f172a) ![Badge](https://img.shields.io/badge/Capstone-16a34a) | [07 — Capstone support agent](07-capstone-support-agent/README.md) | router + tools + short-term + long-term + summary |

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md#cookbook-example-milestones)
