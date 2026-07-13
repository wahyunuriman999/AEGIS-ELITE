# Circuit Breaker

Wrap every external dependency call in a circuit breaker:
- **Closed** — normal operation, calls pass through.
- **Open** — failures exceeded threshold, calls fail fast without hitting the dependency (protects both sides from cascading load).
- **Half-Open** — after a cooldown, allow a probe request through to test recovery before fully closing again.
Without this, one slow/failing downstream dependency can exhaust your own service's threads/connections.
