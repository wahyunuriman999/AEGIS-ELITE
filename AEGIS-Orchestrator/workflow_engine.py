# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from event_bus import EventBus
from context_manager import ExecutionContext

class WorkflowEngine:
    """
    The orchestrator that drives the AEGIS engineering lifecycle using Event Bus.
    Creates a 30-second WOW terminal experience.
    """
    def __init__(self, workspace_path: str):
        self.bus = EventBus()
        self.context = ExecutionContext(workspace_path)
        self._setup_default_listeners()

    def _setup_default_listeners(self):
        # We listen to our own events to print the beautiful UI
        self.bus.subscribe("TASK_RECEIVED", self._log_event)
        self.bus.subscribe("INTENT_ANALYZED", self._log_event)
        self.bus.subscribe("RISK_CHECK", self._log_event)
        self.bus.subscribe("CAPABILITY_RESOLVED", self._log_event)
        self.bus.subscribe("CODE_GENERATED", self._log_event)
        self.bus.subscribe("AUDIT_PASSED", self._log_event)
        self.bus.subscribe("CONSENSUS_REACHED", self._log_event)
        self.bus.subscribe("MEMORY_SAVED", self._log_event)

    def _log_event(self, payload):
        event = payload.get("event", "UNKNOWN")
        desc = payload.get("desc", "")
        print(f"\033[96m[Event Bus]\033[0m ⚡ \033[1m{event:<20}\033[0m : {desc}")
        time.sleep(1.2) # Simulate work

    def execute_lifecycle(self, task: str):
        print("\n" + "=" * 65)
        print("  🚀 AEGIS ELITE OS — RUNTIME EXECUTION INITIATED")
        print("=" * 65)
        print(f"  Task Context: {task}")
        print("=" * 65 + "\n")

        # The simulated Event-Driven WOW flow
        self.bus.publish("TASK_RECEIVED", {"event": "TASK_RECEIVED", "desc": f"Ingesting intent: '{task}'"})
        
        self.bus.publish("INTENT_ANALYZED", {"event": "INTENT_ANALYZED", "desc": "AST mapped. Breaking down into sub-tasks."})
        
        self.bus.publish("RISK_CHECK", {"event": "RISK_CHECK", "desc": "\033[92mBlast Radius LOW\033[0m. Safe to proceed."})
        
        self.bus.publish("CAPABILITY_RESOLVED", {"event": "CAPABILITY_RESOLVED", "desc": "Model Router selected \033[93mClaude 3.5 Sonnet\033[0m for coding."})
        
        self.bus.publish("CODE_GENERATED", {"event": "CODE_GENERATED", "desc": "Implementation complete. Emitting to Governance."})
        
        self.bus.publish("AUDIT_PASSED", {"event": "AUDIT_PASSED", "desc": "Security & Architecture policies passed (Score: 98)."})
        
        self.bus.publish("CONSENSUS_REACHED", {"event": "CONSENSUS_REACHED", "desc": "Multi-agent review council \033[92mAPPROVED\033[0m changes."})
        
        self.bus.publish("MEMORY_SAVED", {"event": "MEMORY_SAVED", "desc": "ADR-101 committed to long-term memory."})

        print("\n" + "=" * 65)
        print("  ✅ \033[92mEXECUTION COMPLETE.\033[0m All systems nominal.")
        print("=" * 65 + "\n")
