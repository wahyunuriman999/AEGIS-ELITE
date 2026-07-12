# Anti-Patterns (Foundation-level)

- **Symptom patching** — fixing the error message instead of the root cause.
- **Silent scope creep** — "while I was in there" refactors that weren't asked for and weren't reported.
- **False confidence** — reporting something as verified when it was only reasoned about.
- **Big-bang diffs** — bundling an unrelated refactor with a bug fix, making both harder to review and revert.
- **Cargo-culting a pattern** — introducing DDD/microservices/etc. because it's popular, not because the problem needs it.
