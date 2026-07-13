# Exceptions

- Use exceptions for exceptional, unexpected conditions — not for routine control flow.
- Custom exception types should carry enough context to act on (what failed, with what input, why) — not just a message string.
- Never catch a broad exception type just to suppress it; catch what you can actually handle.
