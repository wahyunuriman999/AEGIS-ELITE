# Decision Example

**Problem:** A slow endpoint has two candidate fixes: (a) add a DB index, (b) add an in-memory cache.

**Applying the priority order:**
- Correctness: both fine.
- Security: no difference.
- Recoverability: (a) is a one-line reversible migration; (b) adds cache-invalidation complexity and staleness risk.
- Minimal diff: (a) is smaller.

**Decision:** Add the index (a). Revisit caching only if the index alone doesn't hit the latency target — don't solve a problem you don't have yet.
