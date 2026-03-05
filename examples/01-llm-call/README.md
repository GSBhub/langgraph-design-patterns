# 01 — One LLM call (the cleanest “LLM node”)

Progress: ★★☆☆☆☆☆☆☆

![Badge](https://img.shields.io/badge/Concept-LLM%20Node-0f172a) ![Badge](https://img.shields.io/badge/Provider-OpenAI-111827?logo=openai&logoColor=fff)

## Goal
Put *all* LLM setup in one place (`get_llm()`), then call it from a node.

## Flow
```mermaid
flowchart TD
  START --> answer_with_llm --> END
```

## Files
| File | What it contains |
|---|---|
| `llm.py` | `get_llm()` (OpenAI model config) |
| `state.py` | minimal state (`user_query`, `answer`) |
| `nodes.py` | one node that calls the LLM |
| `graph.py` | wiring + `compile()` |

## File walkthrough order
1) `state.py`
2) `llm.py`
3) `nodes.py`
4) `graph.py`

## Notes
- Set `OPENAI_API_KEY` in your environment.
- Optional: set `OPENAI_MODEL` (defaults to `gpt-4.1-mini`).

## Unlocked
- You know where to put “LLM configuration” vs “graph logic”.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../../README.md)
[![Prev](https://img.shields.io/badge/Prev-00%20Hello%20StateGraph-64748b)](../00-hello-stategraph/README.md)
[![Next](https://img.shields.io/badge/Next-02%20Tools%20basics-2563eb)](../02-tools-basics/README.md)
