# Monolith

A single deployable unit. The right default for most projects, especially early on — it avoids premature distributed-systems complexity. A well-modularized monolith (clear internal boundaries, see `ServiceBoundaries.md`) can be split into services later *if and when* a real need appears; the reverse (un-splitting microservices) is much harder.
