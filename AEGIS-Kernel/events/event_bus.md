# AEGIS Cognitive Event Bus

Sub-engines within AEGIS do not call each other directly. They broadcast and listen to events. This ensures decoupling and true OS-level orchestration.

## Core Events:
- `EVENT_USER_INPUT`: Triggered when the user submits a prompt.
- `EVENT_PLAN_START`: Triggered by Planner.
- `EVENT_GRAPH_TRAVERSAL`: Triggered by Reasoner when reading `runtime_image.json`.
- `EVENT_SIMULATION_FAILED`: Triggered if Engineering Entropy > 0.8. Forces fallback.
- `EVENT_DEBATE_REQUIRED`: Triggered by Validator if Simulation passes but risk is > 0.5. Wakes up `architecture_agent`, `security_agent`, `performance_agent`.
- `EVENT_EXECUTION_READY`: Triggered when consensus is reached.
- `EVENT_EVOLUTION_COMPLETE`: Triggered by Learning Engine after Genome mutation.
