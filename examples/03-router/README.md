# 03 — Router (deterministic checks → router LLM → conditional edges)

Progress: ★★★★☆☆☆☆☆

![Badge](https://img.shields.io/badge/Concept-Routing-0f172a) ![Badge](https://img.shields.io/badge/Pattern-Deterministic%20Prechecks-2563eb)

## Goal
Learn the clean “router” structure used in most real LangGraph apps:
1) cheap deterministic checks (URL + escalation keywords)
2) router LLM only when needed
3) `add_conditional_edges` to pick the next node

## Flow
```mermaid
flowchart TD
  START --> precheck --> decided{Route decided?}
  decided -->|Yes| route_edge
  decided -->|No| router_llm --> route_edge
  route_edge --> normal_chat --> END
  route_edge --> rag_chat --> END
  route_edge --> url_tool_first --> END
  route_edge --> escalate_human --> END
```

## What this example is (and isn’t)
- This is a router + wiring demo.
- The `rag_chat` node is intentionally a placeholder (we’ll build a full capstone later).

## File walkthrough order
1) `state.py`
2) `llm.py`
3) `nodes.py`
4) `graph.py`

## Unlocked
- You can save tokens by skipping the router LLM on obvious cases.
- You can keep route labels boring and stable.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../../README.md)
[![Prev](https://img.shields.io/badge/Prev-02%20Tools%20basics-64748b)](../02-tools-basics/README.md)
[![Next](https://img.shields.io/badge/Next-03b%20RAG%20branch-2563eb)](../03b-rag-branch/README.md)
