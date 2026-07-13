# Concurrency

- Prefer immutability and message-passing over shared mutable state when possible.
- Every shared mutable resource needs an explicit synchronization strategy — "it probably won't race" is not a strategy.
- Watch for: race conditions, deadlocks (lock ordering), TOCTOU bugs, and blocking calls inside async/event-loop code.
- Idempotency matters more than raw locking for distributed concurrency — see `backend/patterns/idempotency.md`.
