# Event-Driven Architecture

Components communicate via events (something happened) rather than direct calls (do this now) — this decouples producers from consumers in time and in knowledge of each other.

**Trade-offs:** gains loose coupling and scalability; costs eventual consistency, harder end-to-end tracing (mitigate with correlation IDs, `engineering/Tracing.md`), and the need for idempotent consumers (`backend/patterns/idempotency.md`).
