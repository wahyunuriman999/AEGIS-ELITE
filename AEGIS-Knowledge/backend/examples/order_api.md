# Example — Order API

`POST /v1/orders` with header `Idempotency-Key: <uuid>`. Validates payload strictly, re-verifies the authenticated user owns the referenced cart, wraps the downstream payment call in a circuit breaker, and returns:
```json
{ "data": { "orderId": "...", "status": "pending" } }
```
on success, or the shared error model on failure. Retried requests with the same idempotency key return the original stored response rather than creating a duplicate order.
