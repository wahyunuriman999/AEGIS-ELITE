# API Error Model

Consistent shape across the entire API:
```json
{ "error": { "code": "VALIDATION_ERROR", "message": "email is invalid", "details": [...] } }
```
- `code` is a stable, machine-readable string clients can branch on — never change it once shipped.
- `message` is human-readable, safe to show a developer, never leaks internals (stack traces, SQL, file paths).
- Map internal exception types to this model at the API boundary — don't leak internal exception classes to the response.
