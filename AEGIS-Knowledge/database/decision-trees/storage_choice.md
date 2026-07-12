# Decision Tree — Storage Choice

```
New storage need
  ├─ Relational data, complex queries, need ACID? → PostgreSQL (default)
  ├─ Relational, existing MySQL ecosystem/team expertise? → MySQL
  ├─ Genuinely variable/document-shaped schema? → MongoDB
  ├─ Cache / session / ephemeral fast lookup? → Redis
  ├─ Time-series data? → TimescaleDB / InfluxDB
  └─ Full-text search? → Elasticsearch / OpenSearch
```
When unsure, PostgreSQL is the safe default — it covers relational, JSONB semi-structured, and full-text search reasonably well without adding a new engine to operate.
