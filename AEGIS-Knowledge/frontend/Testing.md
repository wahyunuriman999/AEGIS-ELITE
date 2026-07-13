# Frontend Testing

Test the same pyramid as `engineering/Testing.md`, applied to UI:

- **Unit** — pure functions, hooks in isolation (`renderHook`), presentation components with
  shallow prop assertions. Fast, most numerous.
- **Integration** — a feature/container rendered with a mocked network layer (MSW or
  equivalent), asserting on user-visible behavior (text, roles) not implementation detail
  (no `wrapper.state()`, no CSS class selectors).
- **End-to-end** — the critical user journeys only (sign-up, checkout, primary CRUD flow).
  Slow and flaky by nature; keep the count small and stable.

Query by role/label/text (`getByRole`, `getByLabelText`), never by CSS class or DOM structure —
tests that assert on structure break on every refactor even when behavior is unchanged, which
is exactly the "brittle test" failure mode `engineering/Testing.md` warns against.

A test that mocks so much of the component's own logic that it can't fail is worse than no
test — it's a false-confidence signal in a review, see `foundation/AntiPatterns.md`.
