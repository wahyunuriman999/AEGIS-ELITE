# Decision Tree — API Style

```
New API
  ├─ Internal service-to-service, need streaming/perf? → gRPC
  ├─ Public/browser-facing, simple resource CRUD? → REST
  ├─ Clients need flexible/nested queries, over-fetching is a real problem? → GraphQL
  └─ Real-time bidirectional push needed? → WebSockets (on top of REST for the rest)
```
