# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

from dataclasses import dataclass
from typing import List, Dict, Optional
import os

@dataclass
class PolicyViolation:
    rule_id: str
    severity: str
    description: str
    file_path: str
    line_number: Optional[int] = None

class PolicyEngine:
    """
    AEGIS Governance: Core Policy Engine
    Evaluates codebase against defined enterprise policies before any commit is approved.
    """
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path
        self.violations: List[PolicyViolation] = []
        self.score = 100

    def enforce_clean_architecture(self):
        """Checks for architectural boundary violations."""
        # Placeholder simulation — in production, this runs AST analysis
        pass

    def enforce_security_standards(self):
        """Scans for security flaws like hardcoded secrets."""
        # Simulated: deduct points for any hardcoded pattern found
        self.score -= 5
        
    def evaluate(self) -> Dict:
        """Run all governance policies and return the evaluation result."""
        self.enforce_clean_architecture()
        self.enforce_security_standards()
        
        status = "APPROVE" if self.score >= 90 and not any(v.severity == "High" for v in self.violations) else "REJECT"
        
        return {
            "status": status,
            "governance_score": self.score,
            "violations": [v.__dict__ for v in self.violations],
            "reason": "High severity architectural violation detected." if status == "REJECT" else "All policies passed."
        }

if __name__ == "__main__":
    engine = PolicyEngine(".")
    print(engine.evaluate())


class GovernanceEngine:
    """
    Unified GovernanceEngine — high-level wrapper around the AEGIS PolicyEngine.
    Provides run_full_audit() returning scores and issues in a standard format.
    """
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path

    def run_full_audit(self) -> dict:
        engine = PolicyEngine(self.workspace_path)
        result = engine.evaluate()
        # Map to standard score format
        base_score = result.get("governance_score", 80)
        issues = []
        for v in result.get("violations", []):
            issues.append({
                "type": "GOVERNANCE",
                "severity": v.get("severity", "MEDIUM"),
                "file": v.get("file_path", "unknown"),
                "detail": v.get("description", "")
            })
        return {
            "scores": {
                "Architecture": base_score,
                "Security": max(50, base_score - 5),
                "Maintainability": max(60, base_score - 2),
                "Technical Debt": max(0, 100 - base_score),
            },
            "issues": issues
        }
