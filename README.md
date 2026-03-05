# langgraph-design-patterns

<p align="center">
  <img alt="Docs: Markdown-first" src="https://img.shields.io/badge/Docs-Markdown--first-0f172a?logo=markdown&logoColor=fff" />
  <img alt="LangGraph" src="https://img.shields.io/badge/LangGraph-Design%20Patterns-2563eb?logo=langgraph&logoColor=fff" />
  <img alt="Python: 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=fff" />
  <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-16a34a" />
  <img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-0ea5e9?logo=github&logoColor=fff" />
</p>

<p align="center"><br/></p>

<p align="center">
  <img alt="Jumping graph bot mascot" src="assets/mascot-jump.svg" width="150" />
</p>

> Practical LangGraph patterns for routing, reliable tool calling, memory, and cost-aware workflows.

<p align="center">
  <img alt="Router split hero diagram" src="assets/hero.svg" width="880" />
</p>

## What you’ll learn (fast)
![Badge](https://img.shields.io/badge/Style-Docs--first-0f172a) ![Badge](https://img.shields.io/badge/Approach-Graph--first-2563eb)

- Readable `StateGraph` fundamentals (state → nodes → edges → compile).
- Clean patterns for LLM nodes and tools (where each belongs in a project).
- Routing that avoids slow-by-default RAG (prechecks → router LLM → conditional edges).
- Conditional RAG branches (retrieve only when the route is `rag_chat`).
- Memory done right: short-term threads/checkpoints vs long-term user facts (store).
- Context window control (trim + summarize) to keep prompts small and stable.

## Architecture overview (mental model)
```mermaid
flowchart TD
  U[User message] --> P{Pre-checks}
  P -->|Escalation keywords| E[escalate_human]
  P -->|URL present| T[URL tool-first]
  P -->|No| R{Router}
  R -->|normal_chat| C[Chat]
  R -->|rag_chat| G[RAG]
  G --> S[Synthesize]
  T --> C
  S --> C
```

## Start here
![Badge](https://img.shields.io/badge/Path-Beginner%20Start-16a34a) ![Badge](https://img.shields.io/badge/Steps-4-0f172a)

1. ![Step](https://img.shields.io/badge/Start-1%2F4-0f172a) [00 — Hello StateGraph](examples/00-hello-stategraph/README.md) — Learn state → nodes → edges → compile
2. ![Step](https://img.shields.io/badge/Start-2%2F4-0f172a) [Router decision table](decision-guides/router-decision-table.md) — Pick routes consistently (chat vs RAG vs escalation)
3. ![Step](https://img.shields.io/badge/Start-3%2F4-0f172a) [Deterministic overrides](patterns/04-deterministic-overrides-regex-keywords.md) — Add URL + escalation prechecks before any LLM
4. ![Step](https://img.shields.io/badge/Start-4%2F4-0f172a) [Short-term memory](patterns/05-short-term-memory-checkpointers-thread-id.md) — Use `thread_id` + checkpoints to resume safely

## Quick navigation

### Decision guides (tell me what to do)
![Badge](https://img.shields.io/badge/Section-Decision%20Guides-2563eb) ![Badge](https://img.shields.io/badge/Format-Tables-0f172a)

- [Router decision table](decision-guides/router-decision-table.md) — pick routes fast and consistently.
- [Memory decision table](decision-guides/memory-decision-table.md) — choose checkpointing vs long-term store (keying + retention).
- [Deterministic vs LLM decision table](decision-guides/deterministic-vs-llm-decision-table.md) — decide what must be deterministic vs model-driven.

### Patterns (one idea per page)
![Badge](https://img.shields.io/badge/Section-Patterns-2563eb) ![Badge](https://img.shields.io/badge/Style-One%20idea%20per%20page-0f172a)

1. [Repo structure & separation of concerns](patterns/01-repo-structure-separation-of-concerns.md) — keep nodes/tools/routes decoupled.
2. [Routing: chat vs RAG vs escalation](patterns/02-routing-chat-vs-rag-vs-escalation.md) — route early, keep RAG off the happy path.
3. [Tool-calling contracts & reliability](patterns/03-tool-calling-contracts-and-reliability.md) — tool contracts that don’t break at runtime.
4. [Deterministic overrides (regex + keywords)](patterns/04-deterministic-overrides-regex-keywords.md) — guarantees for URLs and escalation.
5. [Short-term memory (checkpointers + thread_id)](patterns/05-short-term-memory-checkpointers-thread-id.md) — resumable runs with bounded state.
6. [Long-term memory (store + namespace + key)](patterns/06-long-term-memory-store-namespace-key.md) — durable facts with clean keying.
7. [Context window control (trim + summarize)](patterns/07-context-window-trim-summarize.md) — keep prompts small and accurate.
8. [Latency & token budgeting](patterns/08-latency-token-budgeting.md) — budgets per step (router/retrieval/draft).
9. [Retries, fallbacks, and guards](patterns/09-retries-fallbacks-guards.md) — survive flaky tools and invalid outputs.
10. [Multi-node orchestration (state + edges)](patterns/10-multi-node-orchestration.md) — orchestrate stages without spaghetti edges.

## Cookbook (example milestones)
Each example is a milestone. Open its README for a guided walkthrough.

| Progress | Example | Covers |
|---|---|---|
| ![Progress](https://img.shields.io/badge/Progress-1%2F9-0f172a) ![Badge](https://img.shields.io/badge/StateGraph-2563eb) | [00 — Hello StateGraph](examples/00-hello-stategraph/README.md) | state → nodes → edges → compile |
| ![Progress](https://img.shields.io/badge/Progress-2%2F9-0f172a) ![Badge](https://img.shields.io/badge/LLM%20Node-0f172a) ![Badge](https://img.shields.io/badge/OpenAI-111827?logo=openai&logoColor=fff) | [01 — One LLM call](examples/01-llm-call/README.md) | `get_llm()` + one clean LLM node |
| ![Progress](https://img.shields.io/badge/Progress-3%2F9-0f172a) ![Badge](https://img.shields.io/badge/Tools-0f172a) | [02 — Tools basics](examples/02-tools-basics/README.md) | tool definition → tool call → answer with tool output |
| ![Progress](https://img.shields.io/badge/Progress-4%2F9-0f172a) ![Badge](https://img.shields.io/badge/Routing-0f172a) ![Badge](https://img.shields.io/badge/Prechecks-2563eb) | [03 — Router](examples/03-router/README.md) | deterministic checks → router LLM → conditional edges |
| ![Progress](https://img.shields.io/badge/Progress-5%2F9-0f172a) ![Badge](https://img.shields.io/badge/Conditional%20RAG-0f172a) | [03b — RAG branch](examples/03b-rag-branch/README.md) | retrieve only when the route is `rag_chat` |
| ![Progress](https://img.shields.io/badge/Progress-6%2F9-0f172a) ![Badge](https://img.shields.io/badge/Short--term%20Memory-2563eb) | [04 — Short-term memory](examples/04-short-term-memory/README.md) | `InMemorySaver` + `thread_id` |
| ![Progress](https://img.shields.io/badge/Progress-7%2F9-0f172a) ![Badge](https://img.shields.io/badge/Long--term%20Memory-2563eb) | [05 — Long-term memory store](examples/05-long-term-memory-store/README.md) | `InMemoryStore` facts + recall (prod note included) |
| ![Progress](https://img.shields.io/badge/Progress-8%2F9-0f172a) ![Badge](https://img.shields.io/badge/Context%20Window-0f172a) | [06 — Context window summarize](examples/06-context-window-summarize/README.md) | trim + summarize |
| ![Progress](https://img.shields.io/badge/Progress-9%2F9-0f172a) ![Badge](https://img.shields.io/badge/Capstone-16a34a) | [07 — Capstone support agent](examples/07-capstone-support-agent/README.md) | router + tools + short-term + long-term + summary (ReAct-like note included) |

## Contributing
- See [CONTRIBUTING.md](CONTRIBUTING.md).

## License
MIT (see [LICENSE](LICENSE)).
