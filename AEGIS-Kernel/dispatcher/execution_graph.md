# AEGIS Execution Graph (Dispatcher)

Unlike a rigid tree, AEGIS executes via a Directed Graph, allowing for cognitive loops.

- If `VALIDATING` fails, the Dispatcher creates an edge back to `PLANNING` or `REASONING`.
- If `SIMULATING` results in catastrophic entropy, the Dispatcher forces an immediate `EVENT_SIMULATION_FAILED` and routes back to L2 Memory to fetch an alternative blueprint.
- The Dispatcher owns the Priority Queue (Scheduler). Kernel Interrupts bypass the normal graph flow.
