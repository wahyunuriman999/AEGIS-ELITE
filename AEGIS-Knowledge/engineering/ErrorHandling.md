# Error Handling

- Fail loud and specific, not silent and generic — a swallowed exception is a future debugging session for someone else.
- Handle errors at the layer that has enough context to make a decision about them; don't catch-and-rethrow without adding value.
- Distinguish recoverable errors (retry, fallback) from unrecoverable ones (fail fast, alert).
- Every external call (network, disk, DB) needs an explicit failure path — "it won't fail" is never true in production.
