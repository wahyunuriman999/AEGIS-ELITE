# Decision Tree — Architecture Choice

```
New system/module
  ├─ Is business logic simple CRUD? → Layered / simple Monolith, skip DDD/CQRS
  ├─ Complex domain rules, shared language needed? → DDD, bounded contexts
  ├─ Read/write load very asymmetric? → consider CQRS
  ├─ Need independent deploy/scale per capability, real org need? → Microservices
  │    └─ Otherwise → Monolith (modularized, splittable later)
  └─ Need to swap infra (DB, messaging) without touching core logic? → Hexagonal/Clean Architecture
```
