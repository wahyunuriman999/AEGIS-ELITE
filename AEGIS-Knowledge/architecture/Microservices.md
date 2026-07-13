# Microservices

Independently deployable services, each owning its own data. Justify the split with an actual organizational or scaling need (independent deploy cadence, independent scaling, team ownership boundaries) — not just "microservices are best practice."

**Costs:** network calls replace function calls (latency, partial failure), distributed data consistency, more operational surface (deploy, observe, secure N services instead of 1).
