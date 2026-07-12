# Decision Engine

Evaluate alternatives before implementation — do not commit to the first idea that compiles in your head.

**Process:**
1. Name at least two real options (not a strawman vs. your favorite).
2. Score each against the priority order: Correctness → Security → Recoverability → Backward Compatibility → Minimal Diff → Performance → Maintainability → Convention.
3. State which objectives are in tension and why you picked the winner.
4. Write the decision down (see `templates/module_template.md` or `architecture/templates/adr.md` for larger decisions).

If two options tie on every objective above, prefer the one with less new surface area (fewer new files, fewer new dependencies, fewer new concepts).
