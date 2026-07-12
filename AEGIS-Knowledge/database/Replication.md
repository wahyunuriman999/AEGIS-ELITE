# Replication

- Async replication (default in most setups) trades a small window of possible data loss on failover for lower write latency; sync replication trades latency for zero data loss on failover — pick based on actual durability requirements.
- Read replicas offload read traffic but can serve stale data (replication lag) — don't read-your-own-write from a replica right after a write without accounting for this.
- Test failover procedures before you need them in an actual incident.
