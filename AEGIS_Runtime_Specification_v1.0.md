# AEGIS Runtime Specification v1.0

## 1. Core Philosophy
AEGIS is an **Engineering Intelligence Platform**, not just a collection of AI tools. 
The Runtime is the beating heart of AEGIS. It dictates how intents are captured, how decisions are routed, how code is evaluated, and how memory is persisted across the lifecycle of an engineering task.

## 2. The OS Architecture (Event-Driven)
The architecture completely avoids direct engine-to-engine coupling. All interactions are facilitated through the **AEGIS Event Bus** and the **Internal SDK**.

### The Flow of Execution
When a user issues a command (e.g., "Build a Login Page"):

1. **`User` → `CLI Gateway`**
   - The user's natural language intent enters the CLI Gateway (`aegis.py`).
2. **`CLI` → `Orchestrator` (`EVENT: TASK_RECEIVED`)**
   - The Orchestrator receives the task and creates an `ExecutionContext`.
3. **`Orchestrator` → `AEGIS-Compiler` (`EVENT: INTENT_ANALYZED`)**
   - Translates raw text into a strict AST-like Abstract Engineering Intent (AEI).
4. **`AEGIS-Compiler` → `AEGIS-Risk` (`EVENT: RISK_CHECK_START`)**
   - Evaluates the blast radius of the proposed intent. If critical, pipeline halts.
5. **`AEGIS-Risk` → `Model Router` (`EVENT: EXECUTION_START`)**
   - Dynamically provisions the correct LLM (Claude for coding, GPT for reasoning) via the Capability Graph.
6. **`Model Router` → `Execution Engine` (`EVENT: CODE_GENERATED`)**
   - The chosen agent/tool implements the code.
7. **`Execution Engine` → `AEGIS-Governance` (`EVENT: AUDIT_START`)**
   - Code is statically and dynamically audited against enterprise policies.
8. **`AEGIS-Governance` → `AEGIS-Consensus` (`EVENT: VOTE_START`)**
   - If complexity or policy violation is high, a multi-agent council votes on approval.
9. **`AEGIS-Consensus` → `AEGIS-Memory` (`EVENT: MEMORY_UPDATE`)**
   - An Architecture Decision Record (ADR) and a topology snapshot are committed to the project's long-term memory.
10. **`AEGIS-Memory` → `Telemetry` (`EVENT: TASK_COMPLETE`)**
    - Success metrics are sent to Benchmark and Analytics engines for continuous learning.

## 3. Capability Graph
AEGIS does not hardcode which tool does what. It uses a Capability Graph to resolve dependencies.

```mermaid
graph TD
    A[Capability Request: Web Scraping] --> B{Capability Resolver}
    B -->|Resolves to| C[firecrawl-py Plugin]
    B -->|Resolves to| D[Playwright Toolkit]
    B -->|Resolves to| E[curl/wget (Fallback)]
```

### 4. The Internal SDK (`AEGIS-Kernel/sdk.py`)
No engine is permitted to import another engine directly. 
All interactions must flow through the Internal SDK, which acts as the system call (syscall) interface for the AEGIS OS.

**Example Violation:**
`from AEGIS_Governance.policy_engine import GovernanceEngine` ❌

**Example Compliance:**
`aegis_sdk.request_audit(workspace_path, policies=["security", "architecture"])` ✅

## 5. Mandatory vs Optional Modules
- **Mandatory (Kernel Ring 0):** `Orchestrator`, `Event Bus`, `Context Manager`, `Memory`.
- **Optional (Userland Ring 3):** `Consensus` (only for complex tasks), `Benchmark`, `Studio`, `Marketplace`.
