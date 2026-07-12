# Playbook — Debug Session

1. Reproduce the bug reliably (write down exact repro steps).
2. Gather evidence: full stack trace, relevant logs, recent related commits (`git log -p` on the suspect file).
3. Form a hypothesis and find the cheapest way to test it (add a log line, run a smaller repro, read one more function).
4. Isolate root cause — confirm it explains *all* observed symptoms, not just the first one.
5. Write the regression test that fails on the old code.
6. Implement the minimal fix.
7. Confirm the regression test now passes and the rest of the suite is still green.
