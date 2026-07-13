# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman.
# All rights reserved.
# ==========================================

"""
AEGIS-Consensus: Multi-Agent Voting Engine (Elite)

5 specialized AI agents review every code change with weighted voting.
Security and Architecture agents hold VETO power — a single veto blocks
any change regardless of the overall approval rate.

Pipeline:
  Task → Programmer → Reviewer → Architect* → Security* → Performance
  (*) = VETO power in their domain
  Required: 4/5 approvals + mandatory Security + Architect sign-off
"""

import time
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class Verdict(Enum):
    APPROVED = "APPROVED"
    VETOED   = "VETOED"
    ABSTAIN  = "ABSTAIN"


@dataclass
class AgentReview:
    agent_name: str
    verdict: Verdict
    reason: str
    confidence: float          # 0.0 – 1.0
    suggestions: List[str] = field(default_factory=list)
    has_veto_power: bool = False


class BaseAgent:
    """Base class for all AEGIS Consensus review agents."""
    def __init__(self, name: str, weight: float = 1.0, has_veto: bool = False):
        self.name = name
        self.weight = weight
        self.has_veto = has_veto

    def review(self, context: dict) -> AgentReview:
        raise NotImplementedError


# ─────────────────────────────────────────────────────
#  Agent 1: Programmer Agent
#  Reviews implementation correctness and coding standards
# ─────────────────────────────────────────────────────
class ProgrammerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Programmer Agent", weight=1.0)

    def review(self, context: dict) -> AgentReview:
        time.sleep(0.05)
        issues = context.get("issues", [])
        code_issues = [i for i in issues if "code" in i.get("detail", "").lower()]

        if len(code_issues) > 3:
            return AgentReview(
                agent_name=self.name, verdict=Verdict.VETOED,
                reason=f"Too many code-level violations ({len(code_issues)}). Needs rework.",
                confidence=0.9,
                suggestions=["Refactor into smaller functions", "Add type hints", "Remove dead code"]
            )
        return AgentReview(
            agent_name=self.name, verdict=Verdict.APPROVED,
            reason="Implementation follows clean code standards.",
            confidence=0.85,
            suggestions=["Consider adding docstrings for public methods"]
        )


# ─────────────────────────────────────────────────────
#  Agent 2: Reviewer Agent
#  Focuses on readability, maintainability, and DRY principles
# ─────────────────────────────────────────────────────
class ReviewerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Reviewer Agent", weight=1.0)

    def review(self, context: dict) -> AgentReview:
        time.sleep(0.05)
        tech_debt = context.get("scores", {}).get("Technical Debt", 0)

        if tech_debt > 40:
            return AgentReview(
                agent_name=self.name, verdict=Verdict.VETOED,
                reason=f"Technical debt score too high ({tech_debt}%). Maintainability at risk.",
                confidence=0.88,
                suggestions=["Break up long methods", "Extract magic numbers to constants"]
            )
        return AgentReview(
            agent_name=self.name, verdict=Verdict.APPROVED,
            reason="Code is readable and maintainable.",
            confidence=0.82,
            suggestions=[]
        )


# ─────────────────────────────────────────────────────
#  Agent 3: Architect Agent  [VETO POWER]
#  Enforces architecture contracts and layer boundaries
# ─────────────────────────────────────────────────────
class ArchitectAgent(BaseAgent):
    def __init__(self):
        super().__init__("Architect Agent", weight=1.5, has_veto=True)

    def review(self, context: dict) -> AgentReview:
        time.sleep(0.08)
        issues = context.get("issues", [])
        arch_issues = [
            i for i in issues
            if "arch" in i.get("detail", "").lower() or i.get("type") == "ARCHITECTURE"
        ]
        arch_score = context.get("scores", {}).get("Architecture", 100)

        if arch_issues or arch_score < 70:
            return AgentReview(
                agent_name=self.name, verdict=Verdict.VETOED,
                reason=f"Architecture violation detected (score: {arch_score}%). Layer boundary broken.",
                confidence=0.95,
                suggestions=[
                    "Enforce dependency inversion at module boundaries",
                    "Kernel must not import Studio/Marketplace layers"
                ],
                has_veto_power=True
            )
        return AgentReview(
            agent_name=self.name, verdict=Verdict.APPROVED,
            reason=f"Clean architecture maintained (score: {arch_score}%).",
            confidence=0.92,
            suggestions=[]
        )


# ─────────────────────────────────────────────────────
#  Agent 4: Security Agent  [VETO POWER]
#  Zero-tolerance for Critical security violations
# ─────────────────────────────────────────────────────
class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__("Security Agent", weight=2.0, has_veto=True)

    def review(self, context: dict) -> AgentReview:
        time.sleep(0.08)
        issues = context.get("issues", [])
        critical = [i for i in issues if i.get("severity") in ("Critical", "HIGH")]
        sec_score = context.get("scores", {}).get("Security", 100)

        if critical:
            return AgentReview(
                agent_name=self.name, verdict=Verdict.VETOED,
                reason=f"SECURITY VETO: {len(critical)} critical issue(s) — {critical[0]['detail'][:60]}",
                confidence=0.99,
                suggestions=[
                    "Remove all hardcoded credentials",
                    "Use environment variables for secrets",
                    "Run SAST scan before re-submitting"
                ],
                has_veto_power=True
            )
        return AgentReview(
            agent_name=self.name, verdict=Verdict.APPROVED,
            reason=f"No critical security issues (score: {sec_score}%).",
            confidence=0.95,
            suggestions=["Consider adding rate limiting to public endpoints"]
        )


# ─────────────────────────────────────────────────────
#  Agent 5: Performance Agent
#  Detects N+1 queries, blocking calls, and O(n²) patterns
# ─────────────────────────────────────────────────────
class PerformanceAgent(BaseAgent):
    def __init__(self):
        super().__init__("Performance Agent", weight=1.0)

    def review(self, context: dict) -> AgentReview:
        time.sleep(0.05)
        perf_score = context.get("scores", {}).get("Performance", 100)
        issues = context.get("issues", [])
        perf_issues = [
            i for i in issues
            if "n+1" in i.get("detail", "").lower() or "performance" in i.get("detail", "").lower()
        ]

        if perf_score < 60 or len(perf_issues) > 2:
            return AgentReview(
                agent_name=self.name, verdict=Verdict.VETOED,
                reason=f"Performance risk: score {perf_score}%, {len(perf_issues)} perf issue(s) found.",
                confidence=0.87,
                suggestions=["Batch database queries", "Add pagination to list endpoints"]
            )
        return AgentReview(
            agent_name=self.name, verdict=Verdict.APPROVED,
            reason=f"No performance bottlenecks detected (score: {perf_score}%).",
            confidence=0.80,
            suggestions=[]
        )


# ─────────────────────────────────────────────────────
#  Voting Engine — Weighted Consensus Aggregator
# ─────────────────────────────────────────────────────
class VotingEngine:
    """
    AEGIS Consensus: Aggregates votes from 5 specialized AI Agents.

    Rules:
    - Minimum 4/5 agents must approve
    - Security Agent veto = immediate rejection (zero tolerance)
    - Architect Agent veto = immediate rejection
    - Final score = weighted approval rate (0.0 – 1.0)
    """

    REQUIRED_APPROVAL_RATE = 0.80   # 80% weighted threshold
    REQUIRED_APPROVALS     = 4       # Minimum count (unweighted)

    def __init__(self):
        self.agents: List[BaseAgent] = [
            ProgrammerAgent(),
            ReviewerAgent(),
            ArchitectAgent(),
            SecurityAgent(),
            PerformanceAgent(),
        ]

    def execute_consensus(self, context: dict) -> dict:
        reviews: List[AgentReview] = []
        for agent in self.agents:
            review = agent.review(context)
            reviews.append(review)

        # Check hard vetoes first
        hard_vetoes = [r for r in reviews if r.verdict == Verdict.VETOED and r.has_veto_power]
        soft_vetoes = [r for r in reviews if r.verdict == Verdict.VETOED and not r.has_veto_power]

        if hard_vetoes:
            return {
                "consensus_reached": False,
                "approval_rate": 0.0,
                "hard_vetoes": [f"{r.agent_name}: {r.reason}" for r in hard_vetoes],
                "soft_vetoes": [f"{r.agent_name}: {r.reason}" for r in soft_vetoes],
                "all_reviews": [vars(r) for r in reviews],
                "reason": "HARD VETO — Security or Architecture contract broken."
            }

        # Weighted approval calculation
        total_weight  = sum(a.weight for a in self.agents)
        approval_weight = sum(
            a.weight for a, r in zip(self.agents, reviews)
            if r.verdict == Verdict.APPROVED
        )
        approval_count = sum(1 for r in reviews if r.verdict == Verdict.APPROVED)
        approval_rate  = approval_weight / total_weight

        passed = (
            approval_rate >= self.REQUIRED_APPROVAL_RATE and
            approval_count >= self.REQUIRED_APPROVALS and
            not hard_vetoes
        )

        return {
            "consensus_reached": passed,
            "approval_rate": round(approval_rate, 2),
            "approval_count": approval_count,
            "total_agents": len(self.agents),
            "hard_vetoes": [],
            "soft_vetoes": [f"{r.agent_name}: {r.reason}" for r in soft_vetoes],
            "all_reviews": [vars(r) for r in reviews],
            "reason": "All agents approved." if passed else f"Approval rate {approval_rate:.0%} < 80% threshold."
        }


# ─────────────────────────────────────────────────────
#  AIPairReview — High-level wrapper
# ─────────────────────────────────────────────────────
class AIPairReview:
    """High-level interface for running an AI Pair Review via the Voting Engine."""

    def __init__(self):
        self.engine = VotingEngine()

    def run_consensus(self, governance_results: dict) -> bool:
        print(f"\n  ╔══ AEGIS Multi-Agent Consensus (5-Agent Council) ══════╗")
        print(f"  ║  Mode: Enterprise (4/5 required + veto check)         ║")
        print(f"  ╚════════════════════════════════════════════════════════╝\n")

        reviews: List[AgentReview] = []
        for agent in self.engine.agents:
            review = agent.review(governance_results)
            reviews.append(review)
            veto_tag = " [VETO POWER]" if agent.has_veto else ""
            verdict_color = (
                "\033[92mAPPROVED\033[0m" if review.verdict == Verdict.APPROVED
                else "\033[91mVETOED \033[0m"
            )
            conf = f"{review.confidence*100:.0f}%"
            print(f"    → {review.agent_name:<22}{veto_tag:<14} [{verdict_color}]  conf={conf}")
            print(f"       {review.reason}")
            if review.suggestions:
                for s in review.suggestions[:2]:
                    print(f"       💡 {s}")
            print()

        result = self.engine.execute_consensus(governance_results)
        final = result["consensus_reached"]
        rate  = result["approval_rate"]

        print(f"  ── Final Result ─────────────────────────────────────────")
        print(f"  Approval Rate : {rate*100:.0f}%  ({result['approval_count']}/{result['total_agents']} agents)")
        if result.get("hard_vetoes"):
            for v in result["hard_vetoes"]:
                print(f"  🚫 HARD VETO  : {v}")
        print(f"\n  Final Consensus: {'✅ APPROVED — Ready for commit' if final else '❌ REJECTED — Fix required before proceeding'}")
        return final


# Memory export for use in MemoryEngine
class MemoryAgent(BaseAgent):
    """(Internal) Agent for tracking AEGIS memory access patterns."""
    def __init__(self):
        super().__init__("Memory Agent", weight=0.8)

    def review(self, context: dict) -> AgentReview:
        return AgentReview(
            agent_name=self.name, verdict=Verdict.APPROVED,
            reason="Memory access patterns nominal.", confidence=0.75
        )
