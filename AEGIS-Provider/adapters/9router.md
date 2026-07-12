# 9Router Adapter (AI Gateway)

Implements `IAegisProvider`.

9Router is utilized when the Model Orchestrator identifies a need for:
- Auto-fallback (High availability required)
- Multi-provider load balancing
- Cost optimization across endpoints

```python
def generate(task, context):
    # Route through 9Router gateway
    # Endpoint: https://api.9router.com/v1/chat/completions
    return 9router_execute(task)
```
