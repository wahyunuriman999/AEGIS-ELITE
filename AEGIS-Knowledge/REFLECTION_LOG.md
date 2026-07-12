# Reflection Log

**What this actually is:** a plain append-only file, not a self-updating model. There is no
runtime that learns between sessions — the only way "lessons learned" persist across sessions
is if this file is committed to the repo and re-read at the start of the next one. Treat every
claim in this document about "learning" and "memory" with that constraint in mind: it works
exactly as well as a team's shared decision log works, no better.

Append one entry per T2/T3-tier task (see `SKILL.md` complexity tiers). Skip T0/T1 — the
overhead isn't worth it for trivial changes.

## Entry format

```
### YYYY-MM-DD — <short task name>
- Tier: T2|T3
- Domains touched: [list]
- Decision: <what was decided and why, one or two sentences>
- Precedence applied: <which PRECEDENCE.md rule broke the tie, if any>
- Confidence: verified | reasoned | assumed
- Weakness / open risk: <what wasn't fully validated>
- Follow-up: <concrete next action, or "none">
```

## Log

### Example — template, delete before first real entry
- Tier: T2
- Domains touched: [backend, database]
- Decision: Used cursor-based pagination instead of offset for `GET /orders` — offset pagination
  degrades under concurrent writes at this table's scale (see `database/Indexing.md`).
- Precedence applied: correctness > performance (offset pagination is faster to implement but
  returns duplicate/missing rows under write load).
- Confidence: reasoned
- Weakness / open risk: not load-tested against production write volume.
- Follow-up: add a load test before the next release playbook run.
