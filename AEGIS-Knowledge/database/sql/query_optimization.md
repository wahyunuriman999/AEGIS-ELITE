# Query Optimization

1. Measure with `EXPLAIN ANALYZE` — don't guess which query is slow or why.
2. Look for sequential scans on large tables, nested loop joins on unindexed columns, and sort operations spilling to disk.
3. Fix N+1 query patterns with eager loading, batching, or a single JOIN.
4. Always bound result sets (`LIMIT`/pagination) on user-facing or growing-data queries.
5. Re-measure after the fix — confirm the plan actually changed, not just that the query "feels" faster.
