# AEGIS Elite: Architecture Blueprint

## The North Star
**AEGIS is the Operating System for the Entire AI Engineering Lifecycle.**

AEGIS is not just an editor, a chatbot, or a standalone agent. It is an **Engineering Intelligence Platform**. It is the invisible layer that manages, audits, and orchestrates the complex process of engineering AI solutions.

## The Core Philosophy
*   **Architecture Driven, not Feature Driven.** Every capability must map to the core lifecycle. If it doesn't belong to the core orchestration, it is a plugin, not a core engine.
*   **Event-Driven Decoupling.** Core engines do not directly command each other. They publish and subscribe to the Event Bus within the Orchestrator.
*   **Single Source of Truth.** This blueprint dictates the boundaries and responsibilities of every module.

## The Architecture Topology

### 1. The Heart: AEGIS-Orchestrator
The Orchestrator is the central nervous system. It connects the autonomous engines together.
*   **Workflow Engine:** Manages the sequential or autonomous execution of tasks.
*   **Event Bus:** A Pub/Sub mechanism (`PIPELINE_START`, `RISK_DETECTED`, `CODE_GENERATED`).
*   **Context Manager:** Maintains the global state, history, and workspace context during execution.
*   **Model Router:** Dynamically selects the best LLM (Claude, GPT, Gemini, Ollama) based on the current context and complexity.

### 2. The Organs: The Core Engines
These engines subscribe to the Event Bus and perform specialized intelligence tasks:
*   **AEGIS-Memory:** (The Hippocampus) Snapshots project topology and records Architecture Decision Records (ADRs).
*   **AEGIS-Governance:** (The Prefrontal Cortex) Audits architecture, security, and maintainability against predefined policies.
*   **AEGIS-Risk:** (The Amygdala) Detects vulnerabilities, scope creep, and dangerous patterns.
*   **AEGIS-Consensus:** (The Council) Runs multi-agent voting rounds to resolve disputes and approve code changes.
*   **AEGIS-Benchmark:** (The Arena) Tests and profiles output against strict performance baselines.

### 3. The Library: AEGIS-Knowledge
Contains passive data, patterns, and external references to be injected into prompts.
*   **Reference Packs:** Clean, static representations of external repositories (without git history).
*   **Genome Seeds:** Baseline patterns, anti-patterns, and architectural styles.

## The Event Lifecycle (Example)

1.  **`TASK_RECEIVED`**: User submits a request. Orchestrator initializes Context Manager.
2.  **`RISK_ASSESSMENT_START`**: AEGIS-Risk evaluates the task scope. If high risk, emits `RISK_CRITICAL` (halting pipeline). Otherwise, emits `RISK_CLEARED`.
3.  **`EXECUTION_START`**: Orchestrator routes the task to a primary agent via Model Router.
4.  **`CODE_GENERATED`**: Agent finishes coding.
5.  **`GOVERNANCE_AUDIT_START`**: AEGIS-Governance reviews the code. Emits `GOVERNANCE_PASSED` or `POLICY_VIOLATION`.
6.  **`CONSENSUS_START`**: If a policy is violated or a major decision is made, AEGIS-Consensus votes on the outcome.
7.  **`MEMORY_SNAPSHOT`**: AEGIS-Memory records the final ADR and topology.
8.  **`TASK_COMPLETE`**: Orchestrator finalizes the context.

## Excluded Capabilities (Not Core)
*   *Marketplace, Plugins, SDKs, Enterprise Workspaces:* These are future phases (Phases 4-6). They are built **on top** of this core, not embedded within it.
