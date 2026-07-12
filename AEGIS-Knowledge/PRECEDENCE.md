# Precedence & Conflict Resolution

Two domains will eventually give advice that trades off against each other (e.g.
`architecture/Microservices.md` favors service isolation; `engineering/Performance.md` favors
fewer network hops for the same call path). This file is the single place that decides which
wins — routing.json's `conflict_resolution` trigger points here.

## 1. Value precedence (from `foundation/knowledge/foundation.yaml`)

When two pieces of domain knowledge disagree, prefer the one that protects the value higher on
this list:

```
correctness > security > recoverability > backward_compatibility > minimal_diff
            > performance > maintainability > convention
```

This is a ranking, not a weighted score — do not average across levels. A change that is
faster but less recoverable loses to one that is slower but recoverable.

## 2. Override levels

Independent of the value ranking above, some instructions can override the domain knowledge
outright:

| Level | Can override | Cannot override |
|---|---|---|
| **Emergency override** (production incident, data-loss risk) | Minimal-diff, convention, style rules | AEGIS invariants (`SKILL.md` Part 1) — evidence-before-action and read-before-write still apply even mid-incident |
| **User override** (explicit instruction in-session) | Any domain default (e.g. "skip the ADR template for this one") | Security, correctness, and the AEGIS invariants — an explicit request to skip a security check is a signal to flag the tradeoff, not silently comply |
| **System override** (this file, `foundation/`, AEGIS invariants) | All domain-specific guidance | Nothing — this is the top of the stack |

## 3. Domain-vs-domain conflicts

If two domain plugins (see `plugins/PLUGIN_SCHEMA.json`) both claim ownership of a concept —
check each domain's `owns` list in its `MANIFEST.json` — the more specific domain wins for
implementation detail, the more foundational domain wins for the underlying principle.
Example: `architecture/patterns/repository.md` (interface shape) vs.
`database/patterns/repository.md` (query implementation) aren't actually in conflict — they're
cross-referenced views of the same pattern at different layers. A real conflict looks like
`backend/RateLimiting.md` suggesting per-IP limits while `architecture/ServiceBoundaries.md`
implies limits belong at the gateway, not the service — resolve using the value precedence in
§1 first (correctness/security of the limit itself) before defaulting to "backend wins because
it's more specific".

## 4. When precedence still doesn't resolve it

State the conflict and the two options explicitly instead of picking silently — this is
`foundation/Communication.md`'s "say what you're uncertain about" rule applied to
cross-domain conflicts. Log the resolution in `REFLECTION_LOG.md` so the next session doesn't
re-litigate the same tradeoff from scratch.
