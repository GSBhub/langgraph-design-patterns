# Tool-calling contracts & reliability

![Badge](https://img.shields.io/badge/Pattern-Tools-2563eb) ![Badge](https://img.shields.io/badge/Goal-Reliable%20Tool%20Calls-0f172a)

## Quick take
Tool calls fail when the “contract” is vague (inputs/outputs/errors aren’t predictable).
Make tools boring: strict schemas, bounded outputs, validated branches.

## When to use
- You call APIs, retrievers, databases, scrapers, or internal services.
- Wrong args are costly (bad data, retries, user-visible errors).
- You want predictable orchestration (tools as nodes in the graph).

## Avoid when
- You don’t need tools (pure chat only).
- A deterministic function is enough (no model decision needed).

## The contract (what “good” looks like)
| Piece | Example | Why |
|---|---|---|
| Args | `{ "order_id": "A123" }` | Prevents “close enough” inputs |
| Success output | `{ "ok": true, "data": {...} }` | Nodes can branch on `ok` |
| Error output | `{ "ok": false, "error": "timeout" }` | No hallucinated “tool results” |

✅ Do
- Return data (small, structured), not prose.

❌ Don’t
- Store raw HTML/logs directly in state (you’ll blow up context and storage).

## Minimal flow
- Tool decision happens in an LLM node (or a deterministic gate).
- A tool node executes the tool (args validated).
- Tool output is stored in state (bounded, structured).
- Downstream nodes branch on validated fields (`ok`, enums, schemas).
- Failures produce a stable error shape and a fallback path.

## Async & timeouts (practical)
- Most tool calls are I/O. Use `async` where possible.
- Set timeouts and return a structured error (don’t hang forever).
- Limit concurrency (avoid “tool stampedes” when many requests arrive).

## Failure modes
- Free-text tool outputs (symptom: downstream parsing breaks).
- Silent tool failures (symptom: model “fills in” missing results).
- Unbounded outputs (symptom: context window/latency explodes).

## Checklist (copy/paste)
- [ ] Tool args and outputs are schema-first and validated.
- [ ] Tool outputs stored in state are bounded (size caps, strict fields).
- [ ] Errors use a stable shape (`ok=false`, `error=...`).
- [ ] Downstream nodes branch on validated data (not free text).
- [ ] Prompts include clear “call tool vs don’t call tool” rules.

## Links
- Official docs:
  - https://python.langchain.com/docs/how_to/tool_calling/
  - https://langchain-ai.github.io/langgraph/
- Internal:
  - `patterns/09-retries-fallbacks-guards.md`

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-02%20Routing-64748b)](02-routing-chat-vs-rag-vs-escalation.md)
[![Next](https://img.shields.io/badge/Next-04%20Prechecks-2563eb)](04-deterministic-overrides-regex-keywords.md)
