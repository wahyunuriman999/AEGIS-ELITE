# Refactor Example

**Before:** a 120-line function doing validation, DB writes, and email notification in one block, with 5 levels of nested `if`.

**Approach:** extract three pure-ish functions (`validate`, `persist`, `notify`), replace nested conditionals with guard clauses, keep orchestration in the original function calling the three in sequence.

**Result:** each piece independently testable; original function shrinks to ~15 lines of orchestration; behavior unchanged (verified by pre-existing integration test staying green).
