# REST API Design

- Resources are nouns (`/orders`), not verbs (`/getOrder`).
- Use HTTP methods correctly: GET (safe, idempotent), POST (create), PUT (full replace, idempotent), PATCH (partial update), DELETE (idempotent).
- Status codes must be accurate — never `200 OK` with `{"success": false}` in the body.
- Consistent error body across the whole API (see `api/error_model.md`).
- Paginate every list endpoint from day one — retrofitting pagination is a breaking change.
- Version in the URL path (`/v1/orders`) or a header — pick one convention and apply it everywhere (see `api/versioning.md`).
