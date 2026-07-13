# Debugging

`Symptom → Evidence Gathered → Root Cause Isolated → Proposed Fix → Regression Check` (Engine 3).

- Reproduce first. An unreproduced bug fix is a guess.
- Bisect: binary-search across time (git bisect) or across the call stack (add logging/breakpoints at the midpoint) rather than reading every line.
- Read the actual error/stack trace fully before theorizing — most root causes are stated plainly in the error, just not the first line of it.
- Once fixed, write the regression test *before* you consider the bug closed.
