# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

import json
import os
import time
from datetime import datetime

class ProjectMemory:
    """Tracks project architecture topology and context over time."""
    def __init__(self, workspace_path):
        self.workspace = workspace_path
        self.memory_dir = os.path.join(workspace_path, ".aegis", "memory")
        self.context_file = os.path.join(self.memory_dir, "topology.json")
        self._ensure_setup()
        
    def _ensure_setup(self):
        os.makedirs(self.memory_dir, exist_ok=True)
        if not os.path.exists(self.context_file):
            with open(self.context_file, "w") as f:
                json.dump({"components": [], "last_scan": None}, f)
                
    def snapshot_topology(self, components):
        """Save the current architecture topology."""
        data = {
            "components": components,
            "last_scan": datetime.utcnow().isoformat()
        }
        with open(self.context_file, "w") as f:
            json.dump(data, f, indent=2)
        return True


class DecisionHistory:
    """A ledger of all Architecture Decision Records (ADRs)."""
    def __init__(self, workspace_path):
        self.ledger_file = os.path.join(workspace_path, ".aegis", "memory", "decisions.json")
        if not os.path.exists(self.ledger_file):
            with open(self.ledger_file, "w") as f:
                json.dump([], f)
                
    def record_decision(self, title, context, decision, consequences):
        """Append a new ADR to the ledger."""
        with open(self.ledger_file, "r") as f:
            ledger = json.load(f)
            
        adr = {
            "id": f"ADR-{len(ledger) + 1:03d}",
            "date": datetime.utcnow().isoformat(),
            "title": title,
            "context": context,
            "decision": decision,
            "consequences": consequences
        }
        ledger.append(adr)
        
        with open(self.ledger_file, "w") as f:
            json.dump(ledger, f, indent=2)
            
        return adr["id"]


class LearningLoop:
    """Analyzes past failures to adjust future governance rules."""
    def __init__(self, workspace_path):
        self.rules_file = os.path.join(workspace_path, ".aegis", "memory", "learned_rules.json")
        if not os.path.exists(self.rules_file):
            with open(self.rules_file, "w") as f:
                json.dump({"strictness_multiplier": 1.0, "blocked_patterns": []}, f)
                
    def analyze_failure(self, failure_context):
        """Simulate learning from a failed test or bad architecture choice."""
        with open(self.rules_file, "r") as f:
            rules = json.load(f)
            
        # Example logic: increase strictness on repeated failures
        rules["strictness_multiplier"] = min(2.0, rules["strictness_multiplier"] + 0.1)
        
        # If it was a specific pattern, block it
        if "N+1 query" in failure_context.lower():
            if "N+1_QUERY_FORBIDDEN" not in rules["blocked_patterns"]:
                rules["blocked_patterns"].append("N+1_QUERY_FORBIDDEN")
                
        with open(self.rules_file, "w") as f:
            json.dump(rules, f, indent=2)
            
        return rules["strictness_multiplier"]
