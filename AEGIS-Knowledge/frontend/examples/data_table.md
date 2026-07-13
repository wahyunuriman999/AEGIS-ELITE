# Worked Example: Paginated Data Table

Requirement: a sortable, paginated table of orders backed by `GET /orders`.

- **Container** (`useOrderTable`): owns page/sort state (client, local — it's UI-only), fetches
  via React Query keyed on `["orders", page, sort]` (server cache, not duplicated into local
  state), derives `rows` with `useMemo`.
- **Presenter** (`OrderTable`): receives `rows`, `page`, `onPageChange`, `onSortChange`,
  `isLoading`, `error`. Renders `<table>` with `<th scope="col">` and `aria-sort` on the active
  column — accessibility baseline from `AccessibilityAndDesign.md`, not bolted on after.
- **Performance**: page size capped at 50; beyond that, virtualize rows rather than paginate
  smaller (`Performance.md` #3, main-thread blocking on large lists).
- **Testing**: integration test mocks the `/orders` endpoint (MSW), asserts on rendered row
  text and that clicking a column header updates `aria-sort` — never asserts on internal state.

This mirrors `backend/examples/order_api.md` on the server side — same resource, two domains,
one contract (`backend/api/error_model.md`) connecting them.
