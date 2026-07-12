# Tracing

- Propagate a single trace/correlation ID through every hop of a request, including async/queued work.
- A span should represent one meaningful unit of work (a DB call, an external API call), not the entire request.
- Trace sampling is fine for high-volume paths, but always trace 100% of errors.
