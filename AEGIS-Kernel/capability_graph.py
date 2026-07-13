# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

"""
AEGIS Capability Graph
======================
The Capability System is the cornerstone of the AEGIS OS.
ALL modules MUST register themselves as a Capability.
No module is allowed to be invoked directly — only through
the Capability Graph. This enforces:
  - Decoupling between modules
  - Single responsibility per Capability
  - Observability (all invocations are logged)
  - Replaceability (swap providers without touching callers)
"""

from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field
from enum import Enum
import time


class CapabilityStatus(Enum):
    AVAILABLE = "available"
    DEGRADED  = "degraded"
    OFFLINE   = "offline"
    PLANNED   = "planned"


class CapabilityTier(Enum):
    KERNEL    = "kernel"    # Ring-0: platform dies without it
    PLATFORM  = "platform"  # Core services
    ENGINE    = "engine"    # Pluggable engines
    EXTENSION = "extension" # Third-party plugins


@dataclass
class CapabilityRecord:
    name: str
    description: str
    tier: CapabilityTier
    provider: str                         # Which module provides this
    entry_fn: Optional[Callable] = None   # The actual callable
    status: CapabilityStatus = CapabilityStatus.AVAILABLE
    version: str = "1.0.0"
    owner: str = "aegis-core"
    dependencies: List[str] = field(default_factory=list)
    policies: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=lambda: {
        "invocations": 0,
        "failures": 0,
        "avg_latency_ms": 0.0,
    })
    health: Dict[str, Any] = field(default_factory=lambda: {
        "last_check": None,
        "healthy": True,
        "message": "OK"
    })


class CapabilityGraph:
    """
    The Single Source of Truth for ALL capabilities in AEGIS.
    Think of this as the syscall table of the AEGIS OS kernel.
    """

    _instance: Optional["CapabilityGraph"] = None
    _capabilities: Dict[str, CapabilityRecord] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._capabilities = {}
            cls._instance._boot_kernel_capabilities()
        return cls._instance

    def _boot_kernel_capabilities(self):
        """Register Ring-0 (Kernel) capabilities at boot."""
        kernel_caps = [
            CapabilityRecord(
                name="core.event_bus",
                description="Asynchronous event publication and subscription",
                tier=CapabilityTier.KERNEL,
                provider="AEGIS-Orchestrator.event_bus",
            ),
            CapabilityRecord(
                name="core.registry",
                description="Single source of truth for all engine registrations",
                tier=CapabilityTier.KERNEL,
                provider="AEGIS-Kernel.registry",
            ),
            CapabilityRecord(
                name="core.scheduler",
                description="Task scheduling and execution queue management",
                tier=CapabilityTier.KERNEL,
                provider="AEGIS-Runtime.dispatcher",
            ),
            CapabilityRecord(
                name="core.memory",
                description="Long-term memory and ADR persistence",
                tier=CapabilityTier.KERNEL,
                provider="AEGIS-Memory.memory_engine",
            ),
            CapabilityRecord(
                name="platform.model_router",
                description="Intelligent model selection and routing",
                tier=CapabilityTier.PLATFORM,
                provider="AEGIS-Orchestrator.model_router",
            ),
            CapabilityRecord(
                name="platform.governance",
                description="Policy enforcement and code audit",
                tier=CapabilityTier.PLATFORM,
                provider="AEGIS-Governance.policy_engine",
            ),
            CapabilityRecord(
                name="platform.consensus",
                description="Multi-agent review council",
                tier=CapabilityTier.PLATFORM,
                provider="AEGIS-Consensus.voting_engine",
            ),
            CapabilityRecord(
                name="engine.compilation",
                description="Knowledge compilation pipeline (Markdown → AST → Index)",
                tier=CapabilityTier.ENGINE,
                provider="AEGIS-Compiler.pipeline",
            ),
            CapabilityRecord(
                name="engine.risk",
                description="Blast radius assessment and risk scoring",
                tier=CapabilityTier.ENGINE,
                provider="AEGIS-Risk.risk_assessor",
            ),
            CapabilityRecord(
                name="engine.benchmark",
                description="Performance benchmarking and regression testing",
                tier=CapabilityTier.ENGINE,
                provider="AEGIS-Benchmark.runner",
            ),
        ]
        for cap in kernel_caps:
            self._capabilities[cap.name] = cap

    def register(self, capability: CapabilityRecord) -> bool:
        """Register a new capability. Returns True if registration succeeded."""
        if capability.name in self._capabilities:
            existing = self._capabilities[capability.name]
            if existing.tier == CapabilityTier.KERNEL:
                print(f"[CapabilityGraph] ERROR: Cannot override Kernel capability '{capability.name}'")
                return False
        self._capabilities[capability.name] = capability
        return True

    def invoke(self, capability_name: str, **kwargs) -> Any:
        """
        Invoke a capability by name. This is the ONLY sanctioned way
        to call any AEGIS module. All invocations are tracked.
        """
        if capability_name not in self._capabilities:
            raise ValueError(f"[CapabilityGraph] Unknown capability: '{capability_name}'")

        cap = self._capabilities[capability_name]

        if cap.status == CapabilityStatus.OFFLINE:
            raise RuntimeError(f"[CapabilityGraph] Capability '{capability_name}' is OFFLINE.")

        if cap.entry_fn is None:
            # No real fn registered; return a simulated success for now
            cap.metrics["invocations"] += 1
            return {"status": "ok", "capability": capability_name, "provider": cap.provider}

        # Track invocation metrics
        start = time.time()
        cap.metrics["invocations"] += 1
        try:
            result = cap.entry_fn(**kwargs)
            elapsed = (time.time() - start) * 1000
            # Running average
            n = cap.metrics["invocations"]
            cap.metrics["avg_latency_ms"] = (
                cap.metrics["avg_latency_ms"] * (n - 1) + elapsed
            ) / n
            return result
        except Exception as e:
            cap.metrics["failures"] += 1
            cap.health["healthy"] = False
            cap.health["message"] = str(e)
            raise

    def health_check(self) -> Dict[str, Any]:
        """Run a health check across all capabilities."""
        results = {}
        for name, cap in self._capabilities.items():
            results[name] = {
                "status": cap.status.value,
                "healthy": cap.health["healthy"],
                "invocations": cap.metrics["invocations"],
                "failures": cap.metrics["failures"],
                "tier": cap.tier.value,
            }
        return results

    def print_capability_table(self):
        """Print a formatted capability table (for `aegis status`)."""
        tier_order = [CapabilityTier.KERNEL, CapabilityTier.PLATFORM,
                      CapabilityTier.ENGINE, CapabilityTier.EXTENSION]
        tier_labels = {
            CapabilityTier.KERNEL:    "\033[91m[KERNEL   ]\033[0m",
            CapabilityTier.PLATFORM:  "\033[93m[PLATFORM ]\033[0m",
            CapabilityTier.ENGINE:    "\033[96m[ENGINE   ]\033[0m",
            CapabilityTier.EXTENSION: "\033[94m[EXTENSION]\033[0m",
        }
        status_icons = {
            CapabilityStatus.AVAILABLE: "\033[92m●\033[0m",
            CapabilityStatus.DEGRADED:  "\033[93m◐\033[0m",
            CapabilityStatus.OFFLINE:   "\033[91m○\033[0m",
            CapabilityStatus.PLANNED:   "\033[90m◌\033[0m",
        }

        print("\n" + "═" * 75)
        print("  AEGIS CAPABILITY GRAPH — System Topology")
        print("═" * 75)
        for tier in tier_order:
            caps_in_tier = [c for c in self._capabilities.values() if c.tier == tier]
            if not caps_in_tier:
                continue
            print(f"\n  {tier_labels[tier]}")
            for cap in caps_in_tier:
                icon = status_icons[cap.status]
                inv = cap.metrics["invocations"]
                lat = f"{cap.metrics['avg_latency_ms']:.1f}ms" if inv > 0 else "—"
                print(f"    {icon} {cap.name:<35} {cap.provider:<35} inv={inv} lat={lat}")
        print("═" * 75 + "\n")

    def list_capabilities(self) -> List[str]:
        return list(self._capabilities.keys())

    def get(self, capability_name: str) -> Optional[CapabilityRecord]:
        return self._capabilities.get(capability_name)


# Global singleton — the AEGIS syscall table
graph = CapabilityGraph()
