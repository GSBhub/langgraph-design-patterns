# Deterministic vs LLM decision table

![Badge](https://img.shields.io/badge/Decision%20Guide-Determinism-2563eb) ![Badge](https://img.shields.io/badge/Topic-Rules%20vs%20LLM-0f172a)

## Decision table

| Task type | Deterministic method (regex/keyword/rules) | LLM method | Recommended approach | Failure risk |
|---|---|---|---|---|
| URL detection | URL regex + normalization | LLM “notices” a URL | Deterministic pre-check | Low (rules are reliable) |
| Escalation triggers | Keyword/phrase list + small rules | LLM classifier | Deterministic first; LLM can add nuance later | Medium (keywords can be too broad) |
| Route selection (`normal_chat` vs `rag_chat` vs `escalate_human`) | Small rules for obvious cases | Small/fast router model | Hybrid: deterministic pre-checks → router | Medium (ambiguous language) |
| Tool argument validation | Type checks + schema validation | LLM tries to “format correctly” | LLM chooses tool; code validates/repairs/rejects | Medium (bad args break tools) |
| Extract structured fields from messy text | Simple regex for easy fields | Schema-bound extraction | LLM for hard cases; validate outputs | Medium–High |
| Safety/compliance gates | Allow/deny rules | LLM judgment | Deterministic baseline + LLM escalation for nuance | High (policy mistakes are costly) |

## Hybrid pattern
- Deterministic pre-check (URL/keywords/rules)
- Tool call (bounded, validated)
- LLM summarization (compress tool output into user-facing answer)

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-Router%20Decision%20Table-64748b)](router-decision-table.md)
[![Next](https://img.shields.io/badge/Next-Memory%20Decision%20Table-2563eb)](memory-decision-table.md)
