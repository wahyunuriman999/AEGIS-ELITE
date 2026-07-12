# Playbook — API Release

1. Design the contract first (`templates/openapi_template.md`) — review before implementation starts.
2. Implement with validation, auth, and error-model compliance from the first commit, not bolted on after.
3. Add rate limiting and idempotency for any mutating endpoint.
4. Write both a happy-path and an error-path integration test.
5. If replacing/changing an existing contract, ship the new version alongside the old with a deprecation date — never break existing clients silently.
