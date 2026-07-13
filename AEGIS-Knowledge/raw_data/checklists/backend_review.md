# Backend Review Checklist

- [ ] Every mutating endpoint validates input and re-checks ownership against the session
- [ ] Error responses follow the shared error model, no leaked internals
- [ ] Rate limiting/auth applied before the change reaches domain logic
- [ ] External calls wrapped with a circuit breaker/timeout, not an unbounded await
- [ ] Retried/duplicate-safe (idempotency) if the endpoint mutates state
- [ ] Breaking API changes are versioned and documented
