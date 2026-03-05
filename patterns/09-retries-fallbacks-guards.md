# Retries, fallbacks, and guards

![Badge](https://img.shields.io/badge/Pattern-Reliability-2563eb) ![Badge](https://img.shields.io/badge/Goal-Survive%20Failures-0f172a)

## Quick take
Tools and models fail sometimes; your app shouldn’t crash or hallucinate because of it.
Add small guardrails: validate outputs, retry safely, and define a fallback.

## When to use
- You call external tools (HTTP APIs, retrievers, scrapers).
- You parse structured outputs (schemas/enums) and sometimes get invalid data.
- You need predictable behavior under partial failure.

## Avoid when
- Retries could cause harmful side effects (non-idempotent actions).
- A failure is fine to show directly to the user.

## Minimal flow
- Classify failures (timeout vs validation vs upstream error).
- Retry only safe/idempotent operations (small count + backoff).
- Validate route/tool outputs before branching (reject free text).
- Provide a clear fallback (clarify question, safe default, or escalation).
- Log structured error info (step, type, retry count, duration).

```text
Retry policy (starter):
- max_attempts: 2
- retry_on: timeouts + transient 5xx
- never_retry: validation errors, non-idempotent writes
```

## Failure modes
- Blind retries amplify outages (symptom: p95 becomes terrible).
- No validation (symptom: bad tool output poisons downstream nodes).
- Fallback is vague (symptom: model hallucinates instead of admitting failure).

## Checklist (copy/paste)
- [ ] Retries are limited and only for safe/idempotent calls.
- [ ] Outputs are validated before branching (enums/schemas).
- [ ] Fallback behavior is explicit (what the user sees).
- [ ] Errors are structured and logged per step.
- [ ] You can disable flaky tool paths quickly (guard/flag).

## Links
- Official docs:
  - https://langchain-ai.github.io/langgraph/
- Internal:
  - `patterns/03-tool-calling-contracts-and-reliability.md`

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-08%20Budgeting-64748b)](08-latency-token-budgeting.md)
[![Next](https://img.shields.io/badge/Next-10%20Orchestration-2563eb)](10-multi-node-orchestration.md)
