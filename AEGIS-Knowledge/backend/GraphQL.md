# GraphQL

- Use when clients need to fetch varied, nested shapes of data and over/under-fetching from REST is a real, measured problem — not by default.
- Guard against unbounded query depth/complexity (a malicious or careless client can request an exponential-cost query) — set complexity limits.
- N+1 is the default failure mode for resolvers — use a dataloader/batching layer.
- Errors are `200 OK` with an `errors` array by spec — make sure clients actually check it.
