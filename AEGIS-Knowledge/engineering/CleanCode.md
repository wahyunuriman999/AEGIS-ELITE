# Clean Code

Readable over clever.

- One function, one responsibility — if you need "and" to describe it, split it.
- Keep functions short enough to see the whole thing without scrolling; extract when it grows past that.
- Avoid deep nesting — use guard clauses (`patterns/guard_clauses.md`) instead of nested `if`.
- No dead code, no commented-out blocks — delete it, version control remembers it.
- Prefer pure functions where possible; isolate side effects at the edges.
