# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

from dataclasses import dataclass
from typing import List, Dict, Optional
import os
import re

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
        self.workspace_path = os.path.abspath(workspace_path)
        self.violations: List[PolicyViolation] = []
        self.score = 100
        self.python_files = self._gather_files()

    def _gather_files(self) -> List[str]:
        files = []
        for root, _, filenames in os.walk(self.workspace_path):
            if ".git" in root or "__pycache__" in root or "node_modules" in root:
                continue
            for f in filenames:
                if f.endswith(".py"):
                    files.append(os.path.join(root, f))
        return files

    def enforce_clean_architecture(self):
        """Checks for architectural boundary violations (e.g., Kernel importing Studio/GUI)."""
        import_pattern = re.compile(r"^\s*(import|from)\s+([a-zA-Z0-9_\.]+)")
        
        for file_path in self.python_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        match = import_pattern.search(line)
                        if match:
                            module_name = match.group(2)
                            # Rule: Kernel cannot import from Studio or Marketplace
                            if "AEGIS-Kernel" in file_path and ("AEGIS-Studio" in module_name or "AEGIS-Marketplace" in module_name):
                                self.violations.append(PolicyViolation(
                                    rule_id="ARCH-001",
                                    severity="High",
                                    description=f"Clean Architecture Violation: Kernel layer cannot depend on UI/Platform layer '{module_name}'",
                                    file_path=os.path.relpath(file_path, self.workspace_path),
                                    line_number=line_num
                                ))
                                self.score -= 10
            except Exception:
                pass

    def enforce_security_standards(self):
        """Scans for security flaws like hardcoded secrets."""
        secret_pattern = re.compile(r"(api[_\-]?key|secret|password|token)\s*=\s*['\"]([^'\"]{5,})['\"]", re.IGNORECASE)
        
        for file_path in self.python_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        if secret_pattern.search(line):
                            self.violations.append(PolicyViolation(
                                rule_id="SEC-001",
                                severity="Critical",
                                description="Hardcoded credential/secret detected in source code",
                                file_path=os.path.relpath(file_path, self.workspace_path),
                                line_number=line_num
                            ))
                            self.score -= 20
            except Exception:
                pass
        
    def evaluate(self) -> Dict:
        """Run all governance policies and return the evaluation result."""
        self.enforce_clean_architecture()
        self.enforce_security_standards()
        
        # Ensure score doesn't go below 0
        self.score = max(0, self.score)
        
        has_critical = any(v.severity in ["Critical", "High"] for v in self.violations)
        status = "APPROVE" if self.score >= 80 and not has_critical else "REJECT"
        
        return {
            "status": status,
            "governance_score": self.score,
            "violations": [v.__dict__ for v in self.violations],
            "reason": f"{len(self.violations)} violations found." if has_critical else "All policies passed."
        }


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
        
        base_score = result.get("governance_score", 100)
        issues = []
        for v in result.get("violations", []):
            issues.append({
                "type": "GOVERNANCE",
                "severity": v.get("severity", "MEDIUM"),
                "file": v.get("file_path", "unknown"),
                "detail": f"[Line {v.get('line_number', '?')}] {v.get('description', '')}"
            })
            
        return {
            "scores": {
                "Architecture": base_score,
                "Security": max(0, base_score - sum(5 for i in issues if i["severity"] == "Critical")),
                "Maintainability": max(0, base_score - len(issues)),
                "Technical Debt": max(0, 100 - base_score),
            },
            "issues": issues,
            "status": result.get("status", "REJECT")
        }

if __name__ == "__main__":
    engine = PolicyEngine(".")
    print(engine.evaluate())
