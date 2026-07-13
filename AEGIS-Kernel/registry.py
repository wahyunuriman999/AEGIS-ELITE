# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

"""
AEGIS Registry — Single Source of Truth
========================================
Every component in AEGIS must declare itself here.
The Registry is the authoritative source for:
  - Capability → Provider mapping
  - Permission requirements
  - Lifecycle state (booting / running / draining / stopped)
  - Dependencies graph
  - Metrics (invocations, failures, latency)
  - Health checks
  - Version & owner metadata
  - Policy handles
  - Documentation links
"""

import os
import yaml
import time
from typing import Dict, Any, List, Optional
from importlib.util import spec_from_file_location, module_from_spec
from enum import Enum


class LifecycleState(Enum):
    BOOTING  = "booting"
    RUNNING  = "running"
    DRAINING = "draining"
    STOPPED  = "stopped"
    FAILED   = "failed"


class EngineRecord:
    def __init__(self, engine_id: str, config: Dict[str, Any]):
        self.id = engine_id
        self.module_path = config.get("module", "")
        self.entry_file = config.get("entry", "")
        self.description = config.get("description", "")
        self.version = config.get("version", "0.0.0")
        self.owner = config.get("owner", "aegis-core")
        self.capabilities = config.get("capabilities", [])
        self.dependencies = config.get("dependencies", [])
        self.policies = config.get("policies", [])
        self.status = config.get("status", "unknown")
        self.lifecycle: LifecycleState = LifecycleState.STOPPED
        self.module = None
        self.metrics: Dict[str, Any] = {
            "load_time_ms": 0.0,
            "invocations": 0,
            "failures": 0,
        }
        self.health: Dict[str, Any] = {
            "healthy": False,
            "last_check": None,
            "message": "Not loaded",
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
            "owner": self.owner,
            "capabilities": self.capabilities,
            "dependencies": self.dependencies,
            "policies": self.policies,
            "status": self.status,
            "lifecycle": self.lifecycle.value,
            "metrics": self.metrics,
            "health": self.health,
        }


class EngineRegistry:
    """
    The AEGIS Single Source of Truth (SSOT) for all engine registrations.
    This is NOT just a plugin list — it is the authoritative manifest for
    the entire platform's component graph.
    """

    def __init__(self, base_path: str = None):
        self.base_path = base_path or os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        self.manifest_path = os.path.join(self.base_path, "aegis_manifest.yaml")
        self._engines: Dict[str, EngineRecord] = {}
        self._manifest: Dict[str, Any] = {}
        self._start_time = time.time()
        self._load_manifest()

    def _load_manifest(self):
        if not os.path.exists(self.manifest_path):
            raise FileNotFoundError(
                f"[AEGIS Registry] Manifest not found at: {self.manifest_path}"
            )
        with open(self.manifest_path, "r") as f:
            self._manifest = yaml.safe_load(f)

    def _load_module_safe(self, record: EngineRecord) -> bool:
        full_path = os.path.join(
            self.base_path, record.module_path, record.entry_file
        )
        start = time.time()
        try:
            spec = spec_from_file_location(record.id, full_path)
            mod = module_from_spec(spec)
            spec.loader.exec_module(mod)
            record.module = mod
            record.lifecycle = LifecycleState.RUNNING
            record.metrics["load_time_ms"] = (time.time() - start) * 1000
            record.health = {
                "healthy": True,
                "last_check": time.time(),
                "message": "Loaded successfully",
            }
            return True
        except Exception as e:
            record.lifecycle = LifecycleState.FAILED
            record.health = {
                "healthy": False,
                "last_check": time.time(),
                "message": str(e),
            }
            return False

    def boot(self) -> Dict[str, Any]:
        """
        Boot sequence: load all active engines from manifest.
        Returns a boot report.
        """
        sections = ["core", "elite", "platform", "labs"]
        loaded = 0
        failed = 0
        planned = 0

        for section in sections:
            for engine_id, config in self._manifest.get(section, {}).items():
                config["id"] = engine_id
                record = EngineRecord(engine_id, config)
                self._engines[engine_id] = record

                if config.get("status") == "active":
                    record.lifecycle = LifecycleState.BOOTING
                    success = self._load_module_safe(record)
                    if success:
                        loaded += 1
                    else:
                        failed += 1
                elif config.get("status") == "planned":
                    record.lifecycle = LifecycleState.STOPPED
                    planned += 1

        uptime = time.time() - self._start_time
        return {
            "loaded": loaded,
            "failed": failed,
            "planned": planned,
            "total": len(self._engines),
            "boot_time_ms": uptime * 1000,
        }

    def get(self, engine_id: str) -> Optional[Any]:
        """Retrieve a loaded engine's module by ID."""
        record = self._engines.get(engine_id)
        return record.module if record else None

    def get_record(self, engine_id: str) -> Optional[EngineRecord]:
        return self._engines.get(engine_id)

    def list_all(self) -> Dict[str, Dict[str, Any]]:
        return {eid: rec.to_dict() for eid, rec in self._engines.items()}

    def get_by_capability(self, capability: str) -> List[EngineRecord]:
        """Find all engines that provide a given capability."""
        return [
            rec for rec in self._engines.values()
            if capability in rec.capabilities
        ]

    def health_report(self) -> Dict[str, Any]:
        """Comprehensive health report across all registered engines."""
        healthy = sum(1 for r in self._engines.values() if r.health["healthy"])
        total = len(self._engines)
        return {
            "summary": f"{healthy}/{total} engines healthy",
            "healthy": healthy == total,
            "engines": {eid: rec.health for eid, rec in self._engines.items()},
        }

    def print_registry_table(self):
        """Beautiful registry table for `aegis status`."""
        lifecycle_colors = {
            LifecycleState.RUNNING:  "\033[92m▶ RUNNING \033[0m",
            LifecycleState.BOOTING:  "\033[93m◎ BOOTING \033[0m",
            LifecycleState.STOPPED:  "\033[90m◌ PLANNED \033[0m",
            LifecycleState.DRAINING: "\033[93m⏸ DRAIN   \033[0m",
            LifecycleState.FAILED:   "\033[91m✗ FAILED  \033[0m",
        }
        print("\n" + "═" * 80)
        print("  AEGIS ENGINE REGISTRY — Single Source of Truth")
        print("═" * 80)
        print(f"  {'ID':<25} {'LIFECYCLE':<22} {'VERSION':<10} {'OWNER':<15} HEALTH")
        print("  " + "─" * 76)
        for eid, rec in self._engines.items():
            lc = lifecycle_colors.get(rec.lifecycle, "?")
            health_icon = "\033[92m✓\033[0m" if rec.health["healthy"] else "\033[91m✗\033[0m"
            print(f"  {eid:<25} {lc} {rec.version:<10} {rec.owner:<15} {health_icon}")
        print("═" * 80)
        report = self.health_report()
        print(f"  Summary: {report['summary']}")
        print("═" * 80 + "\n")

    def get_packs(self):
        return self._manifest.get("packs", [])
