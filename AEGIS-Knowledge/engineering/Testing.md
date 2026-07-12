# Testing

- A test is a specification of behavior, not a formality — write it to fail if the bug returns.
- Cover: happy path, boundary values, invalid input, and at least one concurrency/ordering case if relevant.
- Prefer fast, isolated unit tests for logic; integration tests for the seams between components; keep end-to-end tests few and high-value.
- A flaky test is worse than no test — fix or delete it, don't ignore it.
- New behavior without a new/updated test is not considered done (Verification Matrix, Engine 14).
