# AEGIS Cognitive State Machine

Every execution within AEGIS MUST transition through these explicit states. The AI must declare its current state internally before processing.

## States:
1. `IDLE`: Awaiting user input.
2. `OBSERVING`: Parsing input, identifying intent, and checking L0 Working Memory.
3. `PLANNING`: Emitting `EVENT_PLAN_START` to construct the execution graph.
4. `REASONING`: Traversing the Knowledge Compiler output (`runtime_image.json`).
5. `SIMULATING`: Running Engineering Physics (Entropy, Cost, Energy) checks.
6. `VALIDATING`: Emitting `EVENT_DEBATE_REQUIRED` if entropy is high.
7. `EXECUTING`: Writing the output code or architecture document.
8. `REFLECTING`: Comparing outcome against L3 Memory (Failure DB).
9. `LEARNING`: Mutating Genome and emitting `EVENT_EVOLUTION_COMPLETE`.
10. `DONE`: Transition back to `IDLE`.
