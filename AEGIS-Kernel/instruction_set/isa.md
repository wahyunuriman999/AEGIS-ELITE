# AEGIS Cognitive Instruction Set Architecture (ISA)

The AI MUST execute reasoning exclusively using the following instruction set. Any output that skips this sequence is a violation of the Cognitive Kernel.

## Instruction Set
1. `OBSERVE`: Parse user intent, environment state, and constraints.
2. `RETRIEVE`: Fetch compiled nodes from the Runtime Image (`aegis.image.bin` / JSON representation).
3. `COMPARE`: Cross-reference retrieved nodes against `PRECEDENCE.md`.
4. `EVALUATE`: Calculate Engineering Entropy (Cost, Latency, Maintenance) of the proposed solution.
5. `PLAN`: Construct a DAG (Directed Acyclic Graph) of actions.
6. `PREDICT`: Run a theoretical timeline (6 months, 1 year, 5 years) to identify long-term tech debt.
7. `SIMULATE`: Stress test the plan against catastrophic failures.
8. `DEBATE`: If architectural entropy is HIGH, invoke virtual sub-agents (`architecture`, `security`, `performance`) to argue the decision.
9. `VALIDATE`: Reach consensus. If consensus fails, fallback to lowest-entropy solution.
10. `REFLECT`: Compare final output against `FAILURE_DB.json`.
11. `LEARN`: If execution completes, log mutation to the Genome and cache the state.
