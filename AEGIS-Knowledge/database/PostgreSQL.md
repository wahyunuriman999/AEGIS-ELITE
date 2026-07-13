# PostgreSQL

- `BIGSERIAL`/`GENERATED ... AS IDENTITY` for simple surrogate primary keys; `UUID` when IDs must be generated client-side or across distributed systems without coordination.
- `JSONB` (indexed, queryable) for semi-structured data you'll actually filter/query on; plain `JSON` only for opaque blobs you'll never query into.
- A sequential scan (`Seq Scan`) on a large table in `EXPLAIN` output is always worth investigating — usually means a missing or unused index.
- Use a connection pooler (e.g. PgBouncer in transaction mode) under high concurrency — Postgres connections are relatively expensive.
