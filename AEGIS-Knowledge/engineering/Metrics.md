# Metrics

- Every metric should answer a question someone will actually ask on-call ("is it slow?", "is it failing?", "is it overloaded?").
- Prefer the RED method for services (Rate, Errors, Duration) and USE for resources (Utilization, Saturation, Errors).
- A metric with no alert threshold is a metric nobody will notice when it breaks — pair metrics with alertability (Engine 12).
