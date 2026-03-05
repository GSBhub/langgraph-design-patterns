# 02 — Tools basics (define a tool, call it, then answer)

Progress: ★★★☆☆☆☆☆☆

![Badge](https://img.shields.io/badge/Concept-Tools-0f172a) ![Badge](https://img.shields.io/badge/Pattern-Tool%20Result%20in%20State-2563eb)

## Goal
Learn the simplest “tools” pattern:
- define a tool in `tools.py`
- call it from a node
- store the result in state
- use the result when drafting an answer

## Flow
```mermaid
flowchart TD
  START --> extract_order_id --> need_tool{Order ID found?}
  need_tool -->|Yes| call_tool --> draft_answer --> END
  need_tool -->|No| draft_answer --> END
```

## Files
| File | What it contains |
|---|---|
| `tools.py` | a single tool: `lookup_order` |
| `llm.py` | `get_llm()` (OpenAI) |
| `state.py` | state keys (`user_query`, `order_id`, `order_info`, `answer`) |
| `nodes.py` | extract → call tool → draft |
| `graph.py` | conditional edge to skip tool when not needed |

## File walkthrough order
1) `state.py`
2) `tools.py`
3) `llm.py`
4) `nodes.py`
5) `graph.py`

## Production note (keep it simple here)
In real apps you’ll typically call tools via an agent loop.
For learning, explicit tool calls are easier to read.

## Unlocked
- “Tool definition” vs “tool invocation” vs “LLM drafting”.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../../README.md)
[![Prev](https://img.shields.io/badge/Prev-01%20One%20LLM%20call-64748b)](../01-llm-call/README.md)
[![Next](https://img.shields.io/badge/Next-03%20Router-2563eb)](../03-router/README.md)
