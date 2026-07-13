# Engineering Principles

1. **Correctness first, always.** Nothing else matters if the code is wrong.
2. **Security is not optional polish.** Treat every external input as hostile until validated.
3. **Reversibility is a design goal.** Prefer changes you can roll back in one command over changes that require a second migration to undo.
4. **Don't break the contract.** Public APIs, schemas, and interfaces are promises to other code — breaking them silently is a bug even if the new behavior is "better."
5. **Measure before you optimize.** Performance work without a measurement is guessing.
6. **Tests are a specification, not a chore.** A missing test for a bug fix means the bug can come back unnoticed.
7. **Debt is a loan with interest — track it, don't hide it.**
