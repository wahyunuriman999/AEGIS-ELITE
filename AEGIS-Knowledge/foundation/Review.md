# Review

Reviewing a diff (yours or someone else's), in order:
1. Does it solve the stated problem, and only that problem?
2. Correctness — trace the actual logic, don't skim.
3. Security — any new untrusted input path?
4. Tests — do they cover the new behavior and the edge cases, or just the happy path?
5. Compatibility — anything a caller could break on?
6. Style/convention — last, and least important.
