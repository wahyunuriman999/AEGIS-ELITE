# Indexing

- Always index foreign key columns — most engines don't do this automatically.
- Index columns used in `WHERE`, `ORDER BY`, and `JOIN ON` for frequently-run queries.
- Composite index column order matters: put the most selective/most-frequently-filtered column first.
- Don't over-index — every index slows down writes and costs storage; index for measured query patterns, not speculatively.
- After adding an index, confirm it's actually used with `EXPLAIN ANALYZE` — don't assume.
