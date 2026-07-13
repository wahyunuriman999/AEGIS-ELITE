# gRPC

- Use for internal service-to-service calls where you control both ends and want strong typing + streaming; avoid exposing gRPC directly to untrusted browser clients (use a gateway/REST facade instead).
- Define errors using gRPC status codes plus a structured error detail message, not just a string.
- Version via the `.proto` package name; never remove or renumber existing fields — only add new optional ones.
