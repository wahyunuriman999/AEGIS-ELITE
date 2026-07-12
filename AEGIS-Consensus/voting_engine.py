# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

import time
from typing import List

class BaseAgent:
    """Base class for all AEGIS Consensus review agents."""
    def __init__(self, name: str, weight: float = 1.0):
        self.name = name
        self.weight = weight

    def review(self, context: dict) -> dict:
        raise NotImplementedError


class ArchitectAgent(BaseAgent):
    def __init__(self):
        super().__init__("Architect Agent", weight=1.5)

    def review(self, context: dict) -> dict:
        time.sleep(0.1)
        # Check if governance found architecture issues
        issues = context.get("issues", [])
        arch_issues = [i for i in issues if "Architecture" in i.get("detail", "")]
        
        if arch_issues:
            return {"approved": False, "reason": f"Architecture violation: {arch_issues[0]['detail']}"}
        return {"approved": True, "reason": "Architecture looks clean."}


class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__("Security Agent", weight=2.0)

    def review(self, context: dict) -> dict:
        time.sleep(0.1)
        issues = context.get("issues", [])
        sec_issues = [i for i in issues if i.get("severity") == "Critical"]
        
        if sec_issues:
            return {"approved": False, "reason": f"Security violation: {sec_issues[0]['detail']}"}
        return {"approved": True, "reason": "No critical security risks found."}


class PerformanceAgent(BaseAgent):
    def __init__(self):
        super().__init__("Performance Agent", weight=1.0)

    def review(self, context: dict) -> dict:
        time.sleep(0.1)
        return {"approved": True, "reason": "No performance bottlenecks detected."}


class VotingEngine:
    """AEGIS Consensus: Aggregates votes from multiple AI Pair Programming Agents."""
    def __init__(self):
        self.agents: List[BaseAgent] = [
            ArchitectAgent(),
            SecurityAgent(),
            PerformanceAgent(),
        ]

    def execute_consensus(self, context: dict) -> dict:
        approvals = 0
        total_weight = 0
        vetoes = []
        for agent in self.agents:
            result = agent.review(context)
            total_weight += agent.weight
            if result["approved"]:
                approvals += agent.weight
            else:
                vetoes.append(f"{agent.name}: {result['reason']}")
        passed = (approvals / total_weight >= 0.8) and len(vetoes) == 0
        return {
            "consensus_reached": passed,
            "approval_rate": round(approvals / total_weight, 2),
            "vetoes": vetoes
        }


class AIPairReview:
    """High-level wrapper for running an AI Pair Review via the Voting Engine."""
    def __init__(self):
        self.engine = VotingEngine()

    def run_consensus(self, governance_results: dict) -> bool:
        print(f"\n  Running AI Pair Consensus Review...")
        results = []
        for agent in self.engine.agents:
            result = agent.review(governance_results)
            verdict = "\033[92mAPPROVED\033[0m" if result["approved"] else "\033[91mVETOED\033[0m"
            print(f"    → {agent.name:<22} [{verdict}] — {result['reason']}")
            results.append(result["approved"])
        final = all(results)
        print(f"\n  Final Consensus: {'✅ APPROVED' if final else '❌ REJECTED'}")
        return final

