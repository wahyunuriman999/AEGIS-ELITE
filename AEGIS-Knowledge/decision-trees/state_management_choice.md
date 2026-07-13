# State Management Decision Tree

```
Does the data come from a server/API?
├── Yes → Use a server-cache library (React Query/SWR).
│         Do NOT copy it into a global store — that's a second source of truth.
└── No → Is it read by more than one component?
    ├── No  → useState/useReducer in the component that owns it.
    └── Yes → Are those components in the same feature/route?
        ├── Yes → Lift to nearest common parent, or a feature-scoped context.
        └── No  → Is it truly cross-cutting (auth, theme, locale)?
            ├── Yes → Global store.
            └── No  → Reconsider — this is usually a sign the feature boundary
                       is drawn wrong (see architecture/ServiceBoundaries.md),
                       not that the state needs to go global.
```
