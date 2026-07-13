# SQL Fundamentals

- Normalize to 3NF for OLTP by default; denormalize only in response to a measured read-performance bottleneck, not speculatively.
- Enforce data integrity at the database level (`NOT NULL`, `UNIQUE`, `CHECK`, foreign keys) — application-level validation alone can be bypassed by a second app, a script, or a bug.
- Never `SELECT *` in production code — list columns explicitly so schema changes don't silently break or bloat consumers.
- Paginate with keyset/cursor (`WHERE id > :last_id ORDER BY id LIMIT :n`) rather than `OFFSET` for large tables — offset pagination gets slower and can skip/duplicate rows under concurrent writes.
