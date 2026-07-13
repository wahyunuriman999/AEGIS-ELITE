# Clean Architecture

Concentric layers: Entities (core business rules) → Use Cases → Interface Adapters (controllers, presenters) → Frameworks/Drivers (DB, web, UI). Dependencies point inward only — the core never imports from infrastructure.

**Signal you're violating it:** a use case or entity importing an ORM model, an HTTP framework type, or a specific database driver directly.
