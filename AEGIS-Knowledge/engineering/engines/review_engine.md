# Review Engine

Systematic review flow, applied to any diff before it's considered mergeable:

1. Scope check — does the diff match the stated problem?
2. Correctness trace — follow the actual data/control flow, don't pattern-match on shape.
3. Security scan — new input paths, new external calls, new privilege boundaries.
4. Test coverage — new/changed behavior has a test that would fail without the fix.
5. Compatibility classification (Engine 11).
6. Style/lint — last, and mostly automatable.
