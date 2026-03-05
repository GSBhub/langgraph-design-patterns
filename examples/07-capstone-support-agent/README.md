# 07 — Capstone: Support agent (router + tools + short-term + long-term + summary)

Progress: ★★★★★★★★★

![Badge](https://img.shields.io/badge/Capstone-All%20Pieces%20Together-16a34a) ![Badge](https://img.shields.io/badge/Pattern-Graph%20%2B%20Memory%20%2B%20Store-0f172a)

## Goal
Combine the previous examples into one small “support agent” layout that feels like a real project:
- `state.py`: the contract
- `tools.py`: side-effectful utilities
- `nodes.py`: pure-ish steps that read/write state
- `graph.py`: routing + wiring + compile

## Flow (high level)
```mermaid
flowchart TD
  START --> precheck --> decided{Route decided?}
  decided -->|No| router_llm --> route{route}
  decided -->|Yes| route

  route -->|tool_order_lookup| tool_order_lookup --> maybe_summarize --> recall_facts --> draft_answer --> END
  route -->|normal_chat| normal_chat --> maybe_summarize --> recall_facts --> draft_answer --> END
  route -->|escalate_human| escalate_human --> END
```

## “ReAct-like loop” note
This capstone is a *graph-first* implementation (explicit nodes + edges).
If you want a ReAct-style tool loop, use the modern `create_agent` approach (not deprecated `create_react_agent`)
and call it inside a node.

## How the caller passes `thread_id` (short-term) + `user_id` (long-term context)
```python
from langchain_core.messages import HumanMessage

app = build_graph()
config = {"configurable": {"thread_id": "thread-1", "user_id": "user-123"}}

app.invoke({"messages": [HumanMessage(content="Where is my order 12345?")]}, config=config)
```

## Unlocked (what you can now build)
- A readable “glue” layout users can reuse in `agents/`.
- A router that avoids unnecessary LLM calls.
- Short-term conversation memory (threads/checkpointing).
- Long-term facts (store) + recall.
- Context-window summarization.

## File walkthrough order
1) `state.py`
2) `tools.py`
3) `llm.py`
4) `nodes.py`
5) `graph.py`

---
[![Home](https://img.shields.io/badge/Home-Cookbook-0f172a)](../../README.md#cookbook-example-milestones)
[![Prev](https://img.shields.io/badge/Prev-06%20Context%20window-64748b)](../06-context-window-summarize/README.md)
[![Complete](https://img.shields.io/badge/Complete-9%2F9-16a34a)](../../README.md#cookbook-example-milestones)
