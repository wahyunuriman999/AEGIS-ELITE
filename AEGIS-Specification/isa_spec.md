# AEGIS Cognitive Instruction Set Architecture (ISA)

The AEGIS ISA defines the standard set of opcodes required for a model to execute cognitive tasks. Any language implementation (Rust, Go, Python) MUST support these opcodes to be AEGIS-compatible.

## Formal Specification

### `0x01: OBSERVE`
- **Description**: Parses user intent and current environment state.
- **Input**: `UserRequest (String)`, `EnvironmentState (JSON)`
- **Output**: `TaskContext (JSON)`
- **Side Effects**: Modifies L0 Working Memory.
- **Cost**: Low
- **Confidence Impact**: Baseline (+0.0)

### `0x02: RETRIEVE`
- **Description**: Queries L1 (Context), L2 (Experience), and L4 (Failure) Memory.
- **Input**: `TaskContext`
- **Output**: `RelevantKnowledge (Array)`
- **Side Effects**: Reads from external Vector DB / JSON stores.
- **Cost**: Medium

### `0x03: INFER`
- **Description**: Deductive reasoning to bridge gaps between Request and Knowledge.
- **Input**: `TaskContext`, `RelevantKnowledge`
- **Output**: `Hypotheses (Array)`
- **Cost**: High

### `0x04: PLAN`
- **Description**: Constructs the execution graph.
- **Input**: `Hypotheses`
- **Output**: `ExecutionGraph (JSON)`
- **Side Effects**: Modifies L3 Decision Memory (Decision Ledger).
- **Cost**: High

### `0x05: SIMULATE`
- **Description**: Dry-runs the execution graph in isolation.
- **Input**: `ExecutionGraph`
- **Output**: `SimulationResult (Boolean)`
- **Confidence Impact**: +0.2 (Pass) / -0.5 (Fail)

### `0x06: VALIDATE`
- **Description**: Reviews the simulated execution against the Precedence DB.
- **Input**: `SimulationResult`
- **Output**: `ValidationScore (Float)`

### `0x07: ACT/EXECUTE`
- **Description**: Mutates the environment (e.g. tool calls, file writes).
- **Input**: `ExecutionGraph`
- **Output**: `ExecutionTrace (JSON)`
- **Side Effects**: High (Environment Mutation)

### `0x08: REFLECT`
- **Description**: Compares intended outcome vs actual outcome.
- **Input**: `ExecutionTrace`
- **Output**: `Delta (String)`

### `0x09: LEARN`
- **Description**: Integrates new knowledge into L5 Evolution Memory.
- **Input**: `Delta`
- **Output**: `GenomeUpdate (Boolean)`
- **Side Effects**: Writes to `knowledge.graph.json`.
