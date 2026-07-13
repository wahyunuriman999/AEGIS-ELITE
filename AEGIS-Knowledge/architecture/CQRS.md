# CQRS (Command Query Responsibility Segregation)

Separate the write model (commands, business rules, validation) from the read model (queries, optimized for display).

**Use when:** read and write workloads have very different shapes/scale, or the read side needs denormalized views the write model shouldn't be polluted with.
**Avoid when:** the domain is simple CRUD — CQRS adds real complexity (eventual consistency between models, more moving parts) that isn't worth it below a certain complexity threshold.
