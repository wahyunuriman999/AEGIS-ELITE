# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

import json
import datetime
import os

class DecisionLedger:
    """
    AEGIS Project Memory:
    Records every architectural decision, why it was made, and the trade-offs considered.
    """
    def __init__(self, ledger_path: str = ".aegis/decision_ledger.json"):
        self.ledger_path = ledger_path
        self._ensure_exists()

    def _ensure_exists(self):
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        if not os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'w') as f:
                json.dump([], f)

    def record_decision(self, title: str, context: str, decision: str, trade_offs: list):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "title": title,
            "context": context,
            "decision": decision,
            "trade_offs": trade_offs
        }
        
        with open(self.ledger_path, 'r') as f:
            data = json.load(f)
            
        data.append(entry)
        
        with open(self.ledger_path, 'w') as f:
            json.dump(data, f, indent=4)
            
        return entry

if __name__ == "__main__":
    ledger = DecisionLedger()
    ledger.record_decision(
        "Use Strategy Pattern for Governance",
        "Need to support multiple dynamic policy evaluations",
        "Implement base Policy class and derive specific policies",
        ["Pros: Extensible", "Cons: More boilerplate files"]
    )
    print("Decision recorded to ledger.")
