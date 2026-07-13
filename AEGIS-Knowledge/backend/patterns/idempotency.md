# Idempotency

Any mutating endpoint that a client might retry (network timeout, at-least-once queue delivery) must be safe to call more than once with the same effect as calling it once.

- Accept an `Idempotency-Key` header on writes; store `key → response` and return the stored response on a repeat.
- Natural idempotency also works: `PUT` with a full resource state, or a DB `UPSERT` keyed on a client-supplied unique ID.
- Expire idempotency keys after a reasonable window (e.g. 24h) rather than storing forever.
