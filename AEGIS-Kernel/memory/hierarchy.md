# AEGIS Cognitive Memory Hierarchy

The Kernel manages context using a strict 5-layer hierarchy.

- **L0 (Working Memory)**: The current conversation context, immediate variable names, and cursor position. (Extremely fast, volatile).
- **L1 (Task Memory)**: The current `task.md` or `implementation_plan.md`. Defines the active goal.
- **L2 (Knowledge Memory)**: The compiled `runtime_image.json`. The sum of all engineering patterns and blueprints. (Read-only during execution).
- **L3 (Experience Memory)**: The `FAILURE_DB.json`. Historical data of what went wrong in previous attempts.
- **L4 (Evolution Memory)**: The mutations to the Engineering Genome (Fitness, Entropy) over the lifetime of the project.
