# Rate Limiting

- Enforce at the API gateway/edge first, not only in application code.
- Limit per-user/per-client, not just per-IP (shared IPs and NAT break IP-only limiting).
- Return `429 Too Many Requests` with a `Retry-After` header.
- Sliding window or token bucket over fixed window — fixed window allows bursting at the boundary.
