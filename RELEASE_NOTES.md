AEGIS-Elite - Release Notes (pending push)

Summary of changes made locally:

- API hardening: CORS, secure headers, rate limiting, metrics, optional waitress WSGI.
- Studio: proxy `/proxy/runs` endpoint with optional `STUDIO_PROXY_SECRET`.
- Persistence: migrate legacy `api/state.json` -> SQLite `api/state.db` with migration helper.
- Migrations: added minimal `api/migrations.py` scaffolding.
- Backup: `scripts/backup_db.py` to snapshot DB.
- Tests: `AEGIS-Tests/test_api.py` integration tests; existing tests fixed.
- CI: updated `.github/workflows/ci.yml` to run tests, lint, bandit and to build/push Docker image to ghcr.io.
- Dockerfile: installs requirements and runs via `api.app` (waitress preferred).
- Security/dev tools: added `flake8`, `bandit`, `alembic` to `requirements.txt`.

Next steps (on remote):
- Push these changes to the repository to trigger GitHub Actions (Docker build and publish).
- Optionally configure GitHub repository settings and secrets if needed.

Instructions: run `push_changes.ps1` (Windows) or `push_changes.sh` (Unix) with your remote URL to push.
