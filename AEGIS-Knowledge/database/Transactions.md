# Transactions (ACID)

- Wrap any multi-statement/multi-table mutation that must succeed or fail together in a transaction.
- Keep transactions short — never hold one open across a network call (external API, queue publish); this holds locks and blocks other writers.
- Default to `READ COMMITTED` isolation; reach for `SERIALIZABLE` only when you've identified a specific anomaly (e.g. write skew) it actually prevents — it costs throughput.
- For concurrent updates to the same row, use `SELECT ... FOR UPDATE` (pessimistic) or a version column with optimistic locking, depending on contention level.
