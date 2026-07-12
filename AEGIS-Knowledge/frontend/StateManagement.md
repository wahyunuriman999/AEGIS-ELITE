# State Management

Pick the narrowest scope that satisfies the requirement — escalating scope is the single
biggest source of unnecessary re-renders and coupling.

| Scope | Use when | Tooling example |
|---|---|---|
| Local | State used by one component and its direct children | `useState`/`useReducer` |
| Lifted | Two sibling components need to sync | Move state to nearest common parent |
| Shared (feature) | Several components in one feature/route need it | Context, feature store slice |
| Server cache | Data originates from an API and can go stale | React Query / SWR — never hand-roll cache invalidation |
| Global | Truly cross-cutting (auth session, theme, locale) | App-level store (Redux/Zustand/Context) |

Do not default to global state. Every promotion up this table should be justified by an actual
cross-component read, not "might need it later" (see `foundation/AntiPatterns.md` —
speculative generality).

Server state and client state are different problems: server state is cached, can be stale,
and is owned by the network layer; client state (form inputs, UI toggles) is synchronous and
owned by the component. Mixing them in one store is the most common state-management defect —
see `decision-trees/state_management_choice.md`.
