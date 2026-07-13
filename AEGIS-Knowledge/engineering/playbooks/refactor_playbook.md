# Playbook — Refactor

1. Confirm test coverage exists for the code being refactored; add characterization tests if not.
2. Make one mechanical change at a time (extract, rename, inline, move) — run tests after each.
3. Never combine refactor commits with behavior-change commits.
4. Stop at the task boundary — resist "while I'm here" expansion.
5. Re-run the full suite once at the end, not just the tests for the touched file.
