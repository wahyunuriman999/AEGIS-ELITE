# Refactoring

- Refactor and behavior-change are two different commits/PRs — never mix them; it makes both unreviewable.
- Refactor under an existing green test suite; if there's no coverage, add characterization tests first.
- Small, mechanical steps (extract function, rename, inline) beat one large rewrite — each step stays verifiable.
- Stop refactoring at the boundary of the task; "while I'm in here" scope creep is an anti-pattern (see `foundation/AntiPatterns.md`).
