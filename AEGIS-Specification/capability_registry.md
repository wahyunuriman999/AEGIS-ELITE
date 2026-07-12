# Capability Registry

AEGIS Kernel does not hardcode providers (e.g., "Use GPT-4"). It routes based on required *Capabilities*.

## Standard Capabilities
- `core.reasoning`: Deductive/Inductive logic. (Default: Claude-3.5-Sonnet)
- `core.planning`: Workflow generation. (Default: GPT-4o)
- `core.coding`: Syntax generation. (Default: GPT-4o / Claude-3.5-Sonnet)
- `core.cost_analysis`: Mathematical / Optimization tasks. (Default: Gemini 1.5 Pro)
- `core.simulation`: Dry-run execution.
- `infrastructure.routing`: Request fallback / Proxy. (Default: 9Router / LiteLLM)

*The Model Orchestrator maps Task Capabilities to the Provider Registry during Tick 4 (PLAN).*
