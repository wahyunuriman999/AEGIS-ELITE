# Playbook — System Design

1. State the actual requirements: expected load, consistency needs, latency budget, team size/ownership.
2. Walk the decision tree (`decision-trees/architecture_choice.md`) instead of defaulting to a favorite pattern.
3. Draw the boundaries and data ownership before writing any code.
4. Write the decision and its rationale as an ADR (`templates/adr.md`).
5. Design for the current need with clear seams for the *next* likely need — not for every hypothetical future.
