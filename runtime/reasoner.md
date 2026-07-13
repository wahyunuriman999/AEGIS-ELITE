# Reasoner (Knowledge Engine)

## The Contextual Reasoning Loop
Once the Planner has delegated a task, the Reasoner must load and analyze the context.

1. **Graph Traversal**: Read `knowledge.graph.json`. Locate the relevant nodes and follow the `depends_on` relationships.
2. **Precedence Check**: Cross-reference the proposed approach with `PRECEDENCE.md`. If a conflict exists, strict adherence to PRECEDENCE is mandatory.
3. **Tradeoff Analysis**: Determine the Cost vs. Speed vs. Maintenance of the approach.
4. **Handoff**: Pass the theoretical solution to the `simulation_engine.md`.
