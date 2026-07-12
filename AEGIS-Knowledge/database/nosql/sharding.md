# Sharding

- Choose a shard key that distributes both data and query load evenly — a poorly chosen key creates hot shards.
- Design queries to include the shard key wherever possible; cross-shard queries/joins are expensive or impossible without an aggregation layer.
- Plan for resharding from day one — data volume growth is not optional, and resharding without a plan is an operational emergency.
