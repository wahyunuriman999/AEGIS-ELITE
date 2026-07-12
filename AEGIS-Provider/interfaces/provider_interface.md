# AEGIS Provider Interface

All LLM Providers MUST implement this standard interface to be invoked by the AEGIS Cognitive Model Orchestrator. The Kernel does not care what model is running, it only expects this interface.

## Interface Signature

```python
class IAegisProvider:
    def generate(self, task_payload: dict, context_memory: dict) -> dict:
        \"\"\"
        Executes a specific cognitive task.
        
        Args:
            task_payload: The segmented task from the Task Analyzer.
            context_memory: The subset of L0/L1 memory required for execution.
            
        Returns:
            dict containing the response, token usage, and latency.
        \"\"\"
        pass
```
