# Test Engine

Systematic procedure for deciding what to test:

1. List the function/module's observable behaviors (inputs → outputs/side effects).
2. For each behavior: happy path, boundary, invalid input.
3. For each bug fixed: one regression test that fails on the pre-fix code.
4. For concurrency-sensitive code: at least one test that exercises the race/ordering concern, or an explicit note that it's untestable deterministically and why.
5. Run the full suite, not just the new tests, before declaring done.
