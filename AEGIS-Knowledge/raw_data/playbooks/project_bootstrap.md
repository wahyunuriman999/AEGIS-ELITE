# Playbook — Project Bootstrap

1. Read `README`, `package.json`/`pyproject.toml`/build file, and CI config first — they define ground truth for how the project runs.
2. Run the existing test suite once, unmodified, to establish a known-good baseline before any change.
3. Identify linter/formatter config and match it — don't introduce a competing style.
4. Confirm how secrets/config are supplied (env vars, `.env`, vault) before writing anything that needs them.
5. Only then start on the actual task.
