# Repo structure & separation of concerns

![Badge](https://img.shields.io/badge/Pattern-Architecture-2563eb) ![Badge](https://img.shields.io/badge/Goal-Separation%20of%20Concerns-0f172a)

## Quick take
When routing, tools, prompts, and HTTP routes live in the same file, every change breaks something else.
Split the graph code into small modules so you can change one layer without touching the others.

## Recommended layout (starter)
```text
agent/
  state.py     # AgentState (shared contract)
  nodes.py     # node functions (read state -> write state)
  tools.py     # tool contracts + implementations
  workflow.py  # edges + conditional edges (routing rules)
  graph.py     # build/compile the graph (one public entrypoint)
  memory.py    # checkpoint + long-term store helpers

routes/
  chat.py      # HTTP route -> calls agent.graph.run()
main.py        # server bootstrap
```

## Minimal flow
- Define `AgentState` first (messages, route, tool outputs, etc.).
- Implement nodes as small functions that only read/write `AgentState`.
- Implement tools as pure functions (inputs → outputs), with stable schemas.
- Wire edges/conditions in `workflow.py` (keep policy out of routes).
- Expose one “public entrypoint” in `graph.py` (`run()` / `invoke()`).
- Keep `routes/*` thin: parse request → call graph → return response.

## When to use
- You have more than a couple nodes/tools.
- You want to add RAG, escalation, or memory without rewriting everything.
- You need fast debugging (“where is the router?” should be obvious).

## Avoid when
- You’re doing a one-file prototype.
- You don’t yet know which nodes/tools will exist (sketch first).

## Failure modes
- Circular imports because modules aren’t layered (symptom: import errors).
- Tools mutate state (symptom: “who changed this key?” debugging).
- State becomes an unbounded dump (symptom: prompts/tool outputs explode).

## Checklist (copy/paste)
- [ ] `AgentState` is explicit and documented in `agent/state.py`.
- [ ] Nodes are small and single-purpose (1 job each).
- [ ] Tool inputs/outputs are validated (schema-first).
- [ ] Graph wiring lives in one place (`workflow.py` / `graph.py`).
- [ ] Routes contain no graph policy (only I/O + graph call).

## Links
- Official docs:
  - https://langchain-ai.github.io/langgraph/
- Internal:
  - `patterns/10-multi-node-orchestration.md`

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Next](https://img.shields.io/badge/Next-02%20Routing-2563eb)](02-routing-chat-vs-rag-vs-escalation.md)
