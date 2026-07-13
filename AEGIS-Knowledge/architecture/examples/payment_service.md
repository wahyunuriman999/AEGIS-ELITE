# Example — Payment Service Boundary

A `Payments` service owns its own ledger table; no other service queries it directly. Other services call a versioned `POST /payments` API and subscribe to a `PaymentCompleted` event rather than polling. Idempotency keys are required on every write (`backend/patterns/idempotency.md`) since payment retries must never double-charge.
