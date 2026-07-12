# Hexagonal Architecture (Ports & Adapters)

The application core defines **ports** (interfaces) for what it needs (a repository, a notifier); **adapters** implement those ports for a specific technology (Postgres repository, SMTP notifier). The core never depends on a concrete adapter.

Enables swapping infrastructure (e.g. Postgres → different store) without touching business logic, and makes the core trivially testable with fake adapters.
