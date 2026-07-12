# Logging

- Log at the boundary of decisions and failures, not on every line.
- Structured (key-value/JSON), not free-text string concatenation — it needs to be queryable.
- Never log secrets, tokens, or full PII payloads.
- Include a correlation/request ID so one user-facing event can be traced across services.
- Log levels mean something: ERROR = needs human attention now, WARN = degraded but recovering, INFO = notable state change, DEBUG = developer detail.
