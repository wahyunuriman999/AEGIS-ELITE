# Playbook — Database Release

1. Write the migration as additive-first: new column nullable or with a default, never `NOT NULL` in the same step as adding it to a populated table.
2. For large tables: add nullable → backfill in batches → add constraint, to avoid a long table lock.
3. Never edit a migration that has already run in production — write a new one.
4. Confirm the migration is reversible (a working `down`/rollback), or explicitly document why it can't be.
5. Run `EXPLAIN ANALYZE` on any new query the release introduces before shipping.
