# Component Release Playbook

1. Confirm the presenter has zero data-fetching/store imports (`ComponentArchitecture.md`).
2. Run the accessibility baseline manually: Tab through it, check focus ring, check contrast.
3. Verify state scope against `decision-trees/state_management_choice.md` — don't ship a
   feature-local piece of state promoted to global "just in case".
4. Confirm loading/error/empty states are handled, not just the happy path.
5. Run `checklists/frontend_review.md` against the diff.
6. If the component is user-facing and API-backed, confirm the contract against
   `backend/api/error_model.md` — the presenter's error state and the API's error shape should
   agree.
7. Ship behind a flag if it touches a high-traffic route; otherwise merge.
