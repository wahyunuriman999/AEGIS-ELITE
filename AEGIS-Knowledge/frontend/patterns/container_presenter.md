# Container / Presenter Split

```
useOrderTable()          <- container: fetch, derive, handlers
  |
  v
<OrderTable data={...} onRowClick={...} />   <- presenter: props in, JSX out
```

The presenter never imports a data-fetching client or a store. It is a pure function of props
and is the piece designers/QA can render in isolation (Storybook, snapshot tests) without any
backend running. The container is the piece that changes when the API contract changes; the
presenter is the piece that changes when the design changes. Splitting them means those two
kinds of change stop colliding in the same diff.
