# 06 — Context window (trim + summarize)

Progress: ★★★★★★★★☆

![Badge](https://img.shields.io/badge/Concept-Context%20Window-0f172a) ![Badge](https://img.shields.io/badge/Pattern-Trim%20%2B%20Summarize-2563eb)

## Goal
Keep prompts small as conversations grow:
- keep a rolling window of recent messages
- store an evolving `summary`

## Flow
```mermaid
flowchart TD
  START --> maybe_summarize --> chat --> END
```

## Unlocked
- You know where “summary” belongs (state) and when to update it.

## File walkthrough order
1) `state.py`
2) `llm.py`
3) `nodes.py`
4) `graph.py`

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../../README.md)
[![Prev](https://img.shields.io/badge/Prev-05%20Long--term%20store-64748b)](../05-long-term-memory-store/README.md)
[![Next](https://img.shields.io/badge/Next-07%20Capstone-2563eb)](../07-capstone-support-agent/README.md)
