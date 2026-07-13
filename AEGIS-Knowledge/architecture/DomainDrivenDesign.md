# Domain-Driven Design (DDD)

- **Ubiquitous language** — code, docs, and conversation use the same domain terms; a mismatch is a signal the model is wrong.
- **Bounded context** — a domain model is only consistent within its context; the same word (e.g. "Customer") can mean different things in Billing vs Support — don't force one shared model across contexts.
- **Aggregates** — a cluster of objects treated as one consistency boundary; mutate through the aggregate root only.
- Use DDD's weight where the business logic is genuinely complex — it's overkill for a CRUD admin panel.
