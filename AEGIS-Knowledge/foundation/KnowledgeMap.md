# Knowledge Map

- Judgment / trade-offs / communication → `foundation/`
- Code-level craft (naming, tests, debugging, review) → `engineering/`
- System structure (patterns, boundaries, DDD) → `architecture/`
- APIs/services/auth/caching → `backend/`
- Data modeling/storage/queries → `database/`

When a task spans domains (e.g. "add a rate-limited API endpoint backed by Postgres"), load Foundation once for the decision framing, then pull the specific Backend and Database files needed — don't load entire domains speculatively.
