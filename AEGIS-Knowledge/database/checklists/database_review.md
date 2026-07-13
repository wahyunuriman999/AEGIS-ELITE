# Database Review Checklist

- [ ] Multi-table mutation wrapped in a transaction, kept short (no network calls inside)
- [ ] New/changed query has an index backing it (`EXPLAIN` checked)
- [ ] Migration is additive-first (nullable/default before required) and reversible
- [ ] No `SELECT *` in new production queries
- [ ] Large-table changes avoid locking the table (backfill pattern used)
