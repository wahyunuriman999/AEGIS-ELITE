# Component Architecture

Split every non-trivial UI unit into two layers:

- **Presentation component** — props in, JSX out. No data fetching, no business logic, no
  direct store access. Trivially testable and reusable across pages.
- **Container/hook** — owns data fetching, derived state, and event handlers; passes plain
  props down. In React this is usually a custom hook (`useOrderTable()`), not a wrapper
  component — hooks compose better than HOCs or render-props.

Rules of thumb:
- If a component needs a mock server to render in a test, presentation/container are mixed —
  split it.
- Prop-drill no more than 2 levels; beyond that, lift state or use context/store (see
  `StateManagement.md`).
- A component that both fetches data AND renders a complex layout is doing two jobs — this is
  the #1 review flag in `checklists/frontend_review.md`.

See `patterns/container_presenter.md` for the worked split and `patterns/compound_components.md`
for composable widget families (Tabs, Select, Accordion).
