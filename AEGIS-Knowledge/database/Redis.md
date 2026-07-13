# Redis

- Good fit for: session storage, caching, rate limiting, distributed locks, ephemeral fast lookups — not as a system of record for data you can't afford to lose.
- Plan explicitly for data loss on restart unless persistence (RDB/AOF) and replication are configured.
- Use a clear key naming convention (`session:user:12345`) for operability.
- Set `EXPIRE`/TTL on every non-permanent key — unbounded keys are a slow memory leak.
- Distributed lock pattern: `SET key value NX PX <ttl>` — always set an expiry so a crashed holder doesn't lock forever.
