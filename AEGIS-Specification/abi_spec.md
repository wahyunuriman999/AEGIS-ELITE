# AEGIS Application Binary Interface (ABI)

Defines how plugins, providers, and external engines communicate with the AEGIS Kernel over the Event Bus.

## 1. Provider ABI
Providers MUST respond to the standard payload:
```json
{
  "abi_version": "v1.0",
  "call_type": "generate",
  "capability_required": "reasoning",
  "payload": {
    "task": "...",
    "context": "..."
  }
}
```

## 2. Memory ABI
Memory engines (Vector DBs, Redis, local JSON) MUST implement:
- `memory.read(layer, query)`
- `memory.write(layer, data)`
- `memory.snapshot()`
