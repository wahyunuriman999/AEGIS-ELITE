# Performance

- Measure before optimizing — profile first, guess never.
- Fix algorithmic complexity before micro-optimizing (an O(N²) → O(N) fix beats any constant-factor tuning).
- Common culprits: N+1 queries, synchronous I/O on a hot path, unbounded caches, unnecessary serialization/deserialization, missing indexes (see `database/Indexing.md`).
- Set a budget (latency/memory) before you start — "faster" without a target never finishes.
