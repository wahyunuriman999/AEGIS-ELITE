# AEGIS Adaptive Model Orchestrator

Located at the Dispatcher layer, this Engine receives the Execution Graph from the Planner and assigns specific tasks to the most optimal Provider.

## Pipeline Flow

1. **Task Analyzer**: Breaks down the overarching goal into sub-tasks (e.g., *Need Architecture*, *Need Code*, *Need Cost Analysis*).
2. **Model Ranking Engine**: Scores models based on capability requirements.
3. **Provider Ranking Engine**: Selects the route (Direct API vs 9Router vs LiteLLM).
4. **Cost & Latency Engine**: If speed is prioritized, selects Gemini/DeepSeek. If reliability is prioritized, routes via 9Router.
5. **Execution**: Hands off the payload to `AEGIS-Provider`.

*AEGIS is strictly model-agnostic. The Kernel only orchestrates Cognition.*
