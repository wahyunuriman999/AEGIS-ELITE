# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

"""
AEGIS Runtime Dispatcher
========================
The Event Dispatcher is the traffic controller of the AEGIS Runtime.
It receives incoming tasks (events), resolves the appropriate Capability
from the graph, selects the best Provider, and dispatches execution.

Architecture:
  User Task / CLI
       ↓
  Dispatcher.dispatch(task)
       ↓
  CapabilityGraph.invoke(capability_name)
       ↓
  ModelRouter.select(task_complexity)
       ↓
  Provider (Claude / GPT / Gemini / Ollama)
       ↓
  EventBus.publish(result_event)
"""

import os
import sys
import time
from typing import Any, Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TaskComplexity:
    TRIVIAL   = "trivial"    # < 50 tokens
    MODERATE  = "moderate"   # 50-500 tokens
    COMPLEX   = "complex"    # > 500 tokens
    CRITICAL  = "critical"   # Requires multi-agent consensus


class DispatchResult:
    def __init__(self, task: str, capability: str, provider: str,
                 status: str, payload: Any = None, elapsed_ms: float = 0.0):
        self.task = task
        self.capability = capability
        self.provider = provider
        self.status = status
        self.payload = payload
        self.elapsed_ms = elapsed_ms
        self.timestamp = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task": self.task,
            "capability": self.capability,
            "provider": self.provider,
            "status": self.status,
            "elapsed_ms": round(self.elapsed_ms, 2),
            "timestamp": self.timestamp,
        }


class Dispatcher:
    """
    The AEGIS Runtime Dispatcher.
    Central traffic controller that routes all tasks to the correct Capability.
    """

    CAPABILITY_MAP = {
        # Task keyword → Capability name
        "build":       "platform.model_router",
        "create":      "platform.model_router",
        "generate":    "platform.model_router",
        "implement":   "platform.model_router",
        "write":       "platform.model_router",
        "review":      "platform.governance",
        "audit":       "platform.governance",
        "scan":        "platform.governance",
        "check":       "platform.governance",
        "validate":    "platform.governance",
        "test":        "engine.benchmark",
        "benchmark":   "engine.benchmark",
        "compile":     "engine.compilation",
        "index":       "engine.compilation",
        "risk":        "engine.risk",
        "assess":      "engine.risk",
        "consensus":   "platform.consensus",
        "vote":        "platform.consensus",
        "remember":    "core.memory",
        "save":        "core.memory",
    }

    def __init__(self):
        self._dispatch_log: list = []

    def _classify_complexity(self, task: str) -> TaskComplexity:
        words = len(task.split())
        if words < 5:
            return TaskComplexity.TRIVIAL
        elif words < 20:
            return TaskComplexity.MODERATE
        elif words < 50:
            return TaskComplexity.COMPLEX
        else:
            return TaskComplexity.CRITICAL

    def _resolve_capability(self, task: str) -> str:
        """Resolve the best capability for a given task string."""
        task_lower = task.lower()
        for keyword, capability in self.CAPABILITY_MAP.items():
            if keyword in task_lower:
                return capability
        return "platform.model_router"  # Default to model router

    def dispatch(self, task: str, bus=None) -> DispatchResult:
        """
        Main dispatch method. Routes a task to the appropriate Capability.
        Publishes events to the EventBus if provided.
        """
        start = time.time()
        capability = self._resolve_capability(task)
        complexity = self._classify_complexity(task)

        self._emit(bus, "TASK_DISPATCHED", {
            "task": task,
            "capability": capability,
            "complexity": complexity,
        })

        # Select provider based on complexity and capability
        provider = self._select_provider(capability, complexity)

        self._emit(bus, "PROVIDER_SELECTED", {
            "provider": provider,
            "capability": capability,
            "reason": f"Complexity={complexity}",
        })

        # Simulate execution (real implementation would call the provider)
        time.sleep(0.8)

        elapsed = (time.time() - start) * 1000
        result = DispatchResult(
            task=task,
            capability=capability,
            provider=provider,
            status="success",
            elapsed_ms=elapsed,
        )
        self._dispatch_log.append(result.to_dict())

        self._emit(bus, "DISPATCH_COMPLETE", {
            "task": task,
            "status": "success",
            "elapsed_ms": round(elapsed, 2),
        })

        return result

    def _select_provider(self, capability: str, complexity: str) -> str:
        """Active provider selection based on capability and task complexity."""
        if capability == "platform.governance":
            return "AEGIS-Governance (static-analysis)"
        if capability == "engine.benchmark":
            return "AEGIS-Benchmark (pytest + AEGIS-Eval)"
        if capability == "engine.compilation":
            return "AEGIS-Compiler (knowledge-pipeline)"
        if capability == "engine.risk":
            return "AEGIS-Risk (blast-radius-scorer)"
        if capability == "platform.consensus":
            return "AEGIS-Consensus (multi-agent-council)"
        if capability == "core.memory":
            return "AEGIS-Memory (decision-ledger)"
        # Default: Model Router
        if complexity == TaskComplexity.TRIVIAL:
            return "Gemini 2.5 Flash (trivial)"
        elif complexity == TaskComplexity.MODERATE:
            return "Claude 3.5 Sonnet (moderate)"
        elif complexity == TaskComplexity.COMPLEX:
            return "Claude 3.7 Sonnet (complex)"
        else:
            return "GPT-4o + Consensus Council (critical)"

    def _emit(self, bus, event_type: str, payload: Dict[str, Any]):
        if bus:
            try:
                bus.publish(event_type, payload)
            except Exception:
                pass  # Bus failure must not block dispatch

    def get_dispatch_log(self) -> list:
        return self._dispatch_log

    def print_dispatch_summary(self):
        print(f"\n  [Dispatcher] Total dispatched: {len(self._dispatch_log)} tasks")
        for entry in self._dispatch_log[-5:]:
            print(f"    · {entry['task'][:40]:<42} → {entry['provider']:<35} {entry['elapsed_ms']:.0f}ms")
