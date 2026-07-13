# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

import os
from typing import Dict, Any, List

class AegisSDK:
    """
    The internal System Call (Syscall) API for AEGIS Elite.
    All modules MUST communicate through this SDK to prevent dependency hell.
    """
    
    def __init__(self, orchestrator_bus=None):
        self.bus = orchestrator_bus

    # ---------------------------------------------------------
    # CAPABILITY API (Routing)
    # ---------------------------------------------------------
    def resolve_capability(self, capability_name: str) -> str:
        """Query the Capability Graph for the best tool/plugin."""
        # Simulated Graph Resolution
        if capability_name == "web_scraping":
            return "firecrawl-py"
        if capability_name == "multi_agent":
            return "praisonai"
        return "core-module"

    # ---------------------------------------------------------
    # GOVERNANCE API
    # ---------------------------------------------------------
    def request_audit(self, workspace_path: str, policies: List[str] = None) -> Dict[str, Any]:
        """Request a code audit without directly importing AEGIS-Governance."""
        if self.bus:
            self.bus.publish("AUDIT_START", {"path": workspace_path, "policies": policies})
        return {"status": "audit_requested", "policies": policies or ["default"]}

    # ---------------------------------------------------------
    # MEMORY API
    # ---------------------------------------------------------
    def record_decision(self, title: str, context: str, decision: str) -> str:
        """Record an Architecture Decision Record (ADR) safely."""
        if self.bus:
            self.bus.publish("MEMORY_UPDATE", {"adr_title": title, "decision": decision})
        return "ADR-101"

    # ---------------------------------------------------------
    # RUNTIME API
    # ---------------------------------------------------------
    def emit_event(self, event_type: str, payload: Any):
        """Emit an event to the global Event Bus."""
        if self.bus:
            self.bus.publish(event_type, payload)

# Global SDK Instance (The Kernel's Syscall interface)
sdk = AegisSDK()
