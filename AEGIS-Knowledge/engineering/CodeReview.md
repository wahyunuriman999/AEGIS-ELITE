# Code Review

Order of review priority:
1. Does it solve the stated problem, and only that problem (scope)?
2. Correctness — trace logic, don't skim.
3. Security implications of any new input path.
4. Test coverage of new/changed behavior.
5. Compatibility — anything a caller could break on?
6. Style/convention (last, least important — and often better caught by a linter than a human).
→ `checklists/pr_checklist.md` for the concrete gate.
