# Frontend Review Checklist

- [ ] Presentation/container split respected — no data fetching inside a layout component
- [ ] Every interactive element keyboard-operable with a visible focus state
- [ ] No color-only state signaling; contrast meets WCAG AA
- [ ] State lives at the narrowest scope that satisfies the requirement (`StateManagement.md`)
- [ ] Server-state and client-state are not mixed in one store
- [ ] Images have explicit width/height; nothing below the fold is eagerly loaded
- [ ] New route/heavy component is code-split, not bundled into the main chunk
- [ ] Tests query by role/label/text, not CSS class or DOM structure
- [ ] Design tokens used for color/spacing, no hardcoded hex/px magic numbers
- [ ] Error and loading states are handled explicitly, not left to render a blank screen
