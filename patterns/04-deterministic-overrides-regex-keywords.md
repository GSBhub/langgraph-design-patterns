# Deterministic overrides (regex + keywords)

![Badge](https://img.shields.io/badge/Pattern-Prechecks-2563eb) ![Badge](https://img.shields.io/badge/Goal-Deterministic%20Overrides-0f172a)

## Quick take
Some behaviors should never be “maybe” (URL enrichment, explicit human handoff).
Add cheap deterministic pre-checks before the router/LLM to guarantee them.

## When to use
- Missing a tool call creates a wrong answer (“analyze this link” must work).
- Escalation must be consistent (“talk to a human” should never be ignored).
- You want lower latency on obvious cases (skip router).

## Avoid when
- The signal is ambiguous (keywords create lots of false positives).
- You can’t measure/maintain the rules (they will rot).

## What to gate deterministically (starter)
| Signal | Deterministic check | What to do |
|---|---|---|
| URL present | regex + normalize | run URL tool-first, then answer using extraction |
| Explicit human ask | keyword/phrase list | route to `escalate_human` and build handoff package |

```python
URL_RE = r"https?://\\S+"
ESCALATE = ["talk to a human", "talk to an agent", "representative", "not happy"]
MAX_URLS = 3
```

## Minimal flow
- Run URL detection on the raw message (normalize, cap `MAX_URLS`).
- If URL present: run URL tool-first and store structured extraction in state.
- Run escalation keyword check on the raw message.
- If escalation hits: route to `escalate_human` (handoff package).
- Otherwise: fall back to router (`normal_chat` vs `rag_chat`).

## Failure modes
- Rules are too broad (symptom: tool-first fires on “example.com)” with punctuation).
- Keyword list grows forever (symptom: random false escalations).
- Overrides are invisible (symptom: “why did it do that?” with no logs).

## Checklist (copy/paste)
- [ ] URL detection runs before routing (and is normalized).
- [ ] Escalation keywords are narrow and reviewed (false positives measured).
- [ ] Tool output is structured (no raw HTML in state by default).
- [ ] Every override logs a short reason.
- [ ] You have a simple test set of messages for the rules (URL + escalation).

## Links
- Official docs:
  - https://langchain-ai.github.io/langgraph/
- Internal:
  - `examples/03-router/README.md`

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-03%20Tools-64748b)](03-tool-calling-contracts-and-reliability.md)
[![Next](https://img.shields.io/badge/Next-05%20Short--term%20Memory-2563eb)](05-short-term-memory-checkpointers-thread-id.md)
