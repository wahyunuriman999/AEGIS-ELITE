# 9Router Patterns (AI Gateway Infrastructure)

*Reference: https://github.com/decolua/9router.git*

9Router resolves infrastructure-layer problems, not cognitive-layer problems. It is categorized under `AEGIS-Knowledge/infrastructure/`.

## Key Patterns
1. **Multi-provider Proxy**: Unifies OpenAI, Anthropic, Gemini into a single endpoint.
2. **Auto Fallback**: If OpenAI is rate-limited or down, 9Router automatically falls back to Anthropic or Azure.
3. **Token Optimizer**: Caches responses and minimizes token overhead.
4. **Provider Manager**: Manages API keys and rate limits externally to the application logic.

**AEGIS Context:** AEGIS Planner decides *WHAT* to think about. 9Router ensures the physical request *SUCCEEDS* across the wire.
