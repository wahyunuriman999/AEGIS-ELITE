# Queues & Async Processing

- Assume every message can be delivered more than once — consumers must be idempotent (`patterns/idempotency.md`).
- Set `maxRetries` with backoff, and a dead-letter queue for messages that exceed it — don't let poison messages block the queue forever.
- Keep message payloads small and versioned; put large blobs in object storage and reference them.
- Preserve a correlation ID across the async boundary for tracing.
