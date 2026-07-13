# Reasoning Engine

For ambiguous or multi-step problems, reason explicitly rather than jumping to an answer:

`Problem → Known Facts → Unknowns → Hypotheses → Test/Check Each Hypothesis → Conclusion`

- Separate what you *observed* (logs, code, test output) from what you *inferred*.
- When a hypothesis is cheap to check (grep, run a test, read one more file), check it before reasoning further — don't reason your way around a five-second verification.
- If two hypotheses both fit the evidence, say so rather than silently picking one.
