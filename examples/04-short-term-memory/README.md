# 04 — Short-term memory (threads + checkpointing)

Progress: ★★★★★★☆☆☆

![Badge](https://img.shields.io/badge/Concept-Checkpointing-0f172a) ![Badge](https://img.shields.io/badge/Memory-Short--term%20(thread)-2563eb)

## Goal
Learn “short-term memory” in LangGraph:
- you keep conversation state in the graph
- you use a **checkpointer** so runs can be resumed per `thread_id`

## Key idea
Short-term memory is for *resumable runs* and *debuggable state*, not for durable user facts.

## Flow
```mermaid
flowchart TD
  START --> chat --> END
```

## How the caller passes `thread_id`
```python
app = build_graph()

# Thread 1
config = {"configurable": {"thread_id": "thread-1"}}
app.invoke({"messages": [...]}, config=config)

# Same thread later (resumes state)
app.invoke({"messages": [...]}, config=config)
```

## Unlocked
- You understand “thread = short-term memory boundary”.

## File walkthrough order
1) `state.py`
2) `llm.py`
3) `nodes.py`
4) `graph.py`

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../../README.md)
[![Prev](https://img.shields.io/badge/Prev-03b%20RAG%20branch-64748b)](../03b-rag-branch/README.md)
[![Next](https://img.shields.io/badge/Next-05%20Long--term%20store-2563eb)](../05-long-term-memory-store/README.md)
