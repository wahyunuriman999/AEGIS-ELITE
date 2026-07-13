# Input Validation

- Validate every external input before it reaches domain logic — never trust the client, including your own frontend.
- Reject unknown/unexpected fields in strict mode rather than silently ignoring them.
- Return all validation errors at once, not one-at-a-time — round-trips are expensive for API consumers.
- Never trust a client-supplied ID for ownership; always re-verify against the authenticated session/token.
