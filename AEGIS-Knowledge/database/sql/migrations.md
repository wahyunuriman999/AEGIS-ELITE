# Schema Migrations

- Every schema change is a versioned, checked-in migration file — never a manual change against production.
- Migrations must be idempotent (safe to re-run) and, where possible, reversible.
- Non-breaking first: add columns nullable or with a default before making them required; drop columns only after confirming nothing reads them.
- Large table changes: add nullable → backfill in batches → add constraint. Never take a long lock on a hot production table.
