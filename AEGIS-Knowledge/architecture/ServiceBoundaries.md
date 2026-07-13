# Service Boundaries

Draw boundaries around business capabilities, not technical layers ("Orders" not "Controllers"). A good boundary:
- Owns its own data — no other service reaches into its database directly.
- Has a stable, versioned interface (`backend/api/versioning.md`).
- Changes independently more often than it needs to change in lock-step with another service.

If two "services" always deploy together, they're probably one service.
