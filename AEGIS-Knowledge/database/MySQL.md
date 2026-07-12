# MySQL

- Use the `InnoDB` engine (row-level locking, transactions, foreign keys) — not `MyISAM`.
- `utf8mb4` charset always — plain `utf8` in MySQL doesn't support the full Unicode range (e.g. emoji).
- Enable `STRICT_TRANS_TABLES` so invalid data raises an error instead of being silently truncated/coerced.
- Avoid `ENUM` columns for anything that might grow — a lookup table or a `TINYINT` with an app-level mapping is easier to extend without a schema migration.
