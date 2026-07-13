# Risk

Classify every non-trivial change as `Low` | `Medium` | `High`, with the reason stated explicitly — not inferred by the reader.

**High risk signals:** touches auth/payments/data-deletion, irreversible migrations, changes a public API contract, affects concurrency/ordering guarantees, has no test coverage.

**Reduce risk before shipping, don't just report it:** feature-flag it, make the migration reversible, add the missing test, shrink the diff — then re-classify.
