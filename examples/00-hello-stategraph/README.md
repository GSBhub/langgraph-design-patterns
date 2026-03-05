# 00 — Hello StateGraph (smallest possible graph)

Progress: ★☆☆☆☆☆☆☆☆

![Badge](https://img.shields.io/badge/LangGraph-StateGraph-2563eb) ![Badge](https://img.shields.io/badge/Concept-State%20%2B%20Nodes-0f172a)

## Goal
Learn the three building blocks of a LangGraph workflow:
1) a **state contract** (what data exists),
2) **nodes** (functions that read/write state),
3) **edges** (the order of execution).

## Flow
```mermaid
flowchart TD
  START --> normalize_query --> draft_answer --> END
```

## Files
| File | What it contains |
|---|---|
| `state.py` | the state keys (your contract) |
| `nodes.py` | two tiny node functions |
| `graph.py` | the wiring + `compile()` |

## File walkthrough order
1) `state.py`
2) `nodes.py`
3) `graph.py`

## Unlocked
- You can read a `StateGraph` top-to-bottom.
- You understand “nodes return partial state updates”.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../../README.md)
[![Next](https://img.shields.io/badge/Next-01%20One%20LLM%20call-2563eb)](../01-llm-call/README.md)
