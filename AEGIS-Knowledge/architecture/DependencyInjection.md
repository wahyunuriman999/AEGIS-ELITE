# Dependency Injection

Pass dependencies in (constructor/parameter) rather than constructing them internally — this is what makes a unit testable in isolation.

- Prefer explicit constructor injection over a magic global container when the graph is small.
- A composition root (one place that wires everything together) keeps DI from leaking into every layer.
- DI is a means to testability/decoupling, not a goal in itself — don't inject things that never vary.
