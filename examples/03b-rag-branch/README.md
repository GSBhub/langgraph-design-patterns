# 03b — RAG branch (retrieve only when route is `rag_chat`)

Progress: ★★★★★☆☆☆☆

![Badge](https://img.shields.io/badge/Concept-Conditional%20RAG-0f172a) ![Badge](https://img.shields.io/badge/Pattern-Retrieve%20Only%20When%20Needed-2563eb)

## Goal
Add a RAG branch without making your app slow-by-default:
- route first (`normal_chat` vs `rag_chat`)
- retrieve **only** on `rag_chat`
- draft using retrieved docs

## Flow
```mermaid
flowchart TD
  START --> router --> route{route}
  route -->|normal_chat| normal_chat --> END
  route -->|rag_chat| retrieve --> synthesize --> draft_answer --> END
```

## Files
| File | What it contains |
|---|---|
| `state.py` | state keys for RAG |
| `llm.py` | router model + drafting model |
| `nodes.py` | router → retrieve → synthesize → draft |
| `graph.py` | conditional edges for the RAG branch |

## File walkthrough order
1) `state.py`
2) `llm.py`
3) `nodes.py`
4) `graph.py`

## Unlocked
- You can keep retrieval off the “happy path”.
- You can design a RAG path as normal nodes (no magic).

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../../README.md)
[![Prev](https://img.shields.io/badge/Prev-03%20Router-64748b)](../03-router/README.md)
[![Next](https://img.shields.io/badge/Next-04%20Short--term%20memory-2563eb)](../04-short-term-memory/README.md)
