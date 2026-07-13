# MongoDB

- Fits a genuinely document-shaped, schema-flexible workload — not a default choice for relational data.
- Index every field you actually query on; an unindexed query on a large collection is a full collection scan.
- Embed data for atomic, bounded sub-documents accessed together; reference (separate collection) when the data is unbounded or updated independently.
- Avoid unbounded arrays growing inside a single document — they hit the document size limit and degrade write performance.
