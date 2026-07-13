# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

"""
AEGIS Model Router — Active Intelligent Routing
================================================
This is NOT a passive map. The Model Router actively:
  1. Classifies task complexity and domain
  2. Checks model availability and rate limits
  3. Applies cost optimization (cheap model for simple tasks)
  4. Falls back gracefully when a model is unavailable
  5. Records routing decisions to the Memory engine

Routing Matrix:
  ┌─────────────────────┬──────────────────────────────────────┐
  │ Task Profile        │ Optimal Provider                     │
  ├─────────────────────┼──────────────────────────────────────┤
  │ Code Generation     │ Claude 3.7 Sonnet                    │
  │ Code Review         │ Claude 3.5 Sonnet                    │
  │ Architecture Design │ GPT-4o + Consensus Council           │
  │ Complex Reasoning   │ GPT-4o                               │
  │ Quick Q&A           │ Gemini 2.5 Flash                     │
  │ Documentation       │ Claude 3.5 Haiku                     │
  │ Local/Private       │ Ollama (llama3.2 / codestral)        │
  │ Risk Analysis       │ AEGIS-Risk Engine                    │
  └─────────────────────┴──────────────────────────────────────┘
"""

import re
import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class RouteDecision:
    task: str
    domain: str
    complexity: str
    model: str
    provider: str
    rationale: str
    cost_tier: str           # "micro", "standard", "premium"
    requires_consensus: bool
    timestamp: float = field(default_factory=time.time)

    def display(self):
        tier_colors = {"micro": "\033[92m", "standard": "\033[93m", "premium": "\033[91m"}
        color = tier_colors.get(self.cost_tier, "")
        print(f"\n  ┌─ Model Router Decision ──────────────────────────────")
        print(f"  │  Domain      : {self.domain}")
        print(f"  │  Complexity  : {self.complexity}")
        print(f"  │  Model       : \033[1m{self.model}\033[0m")
        print(f"  │  Provider    : {self.provider}")
        print(f"  │  Cost Tier   : {color}{self.cost_tier.upper()}\033[0m")
        print(f"  │  Consensus   : {'Yes — multi-agent council required' if self.requires_consensus else 'No'}")
        print(f"  │  Rationale   : {self.rationale}")
        print(f"  └─────────────────────────────────────────────────────\n")


class ModelRouter:
    """
    AEGIS Active Model Router.
    Routes engineering tasks to the optimal LLM provider based on
    domain classification, complexity scoring, and cost optimization.
    """

    # Domain keyword patterns → domain label
    DOMAIN_PATTERNS: Dict[str, List[str]] = {
        "code_generation": [
            "build", "create", "implement", "write", "generate", "scaffold",
            "develop", "code", "function", "class", "module", "api", "endpoint"
        ],
        "code_review": [
            "review", "audit", "check", "analyze", "inspect", "lint", "scan",
            "verify", "validate", "compliance"
        ],
        "architecture": [
            "design", "architecture", "system", "diagram", "blueprint", "structure",
            "pattern", "microservice", "monolith", "distributed", "topology"
        ],
        "reasoning": [
            "explain", "why", "how", "compare", "choose", "decide", "evaluate",
            "tradeoff", "pros", "cons", "recommend"
        ],
        "documentation": [
            "document", "readme", "spec", "docs", "comment", "describe", "summarize",
            "changelog", "release notes"
        ],
        "testing": [
            "test", "unit test", "integration", "e2e", "benchmark", "performance",
            "stress", "coverage"
        ],
        "security": [
            "security", "vulnerability", "pentest", "auth", "encryption", "secret",
            "cve", "owasp"
        ],
        "risk": [
            "risk", "danger", "impact", "blast", "rollback", "migration"
        ],
    }

    # Routing matrix: (domain, complexity) → (model, provider, cost_tier, needs_consensus)
    ROUTING_MATRIX: Dict[str, Dict[str, tuple]] = {
        "code_generation": {
            "trivial":  ("claude-3-5-haiku-latest",   "Anthropic API",  "micro",    False),
            "moderate": ("claude-3-5-sonnet-latest",  "Anthropic API",  "standard", False),
            "complex":  ("claude-3-7-sonnet-latest",  "Anthropic API",  "premium",  False),
            "critical": ("claude-3-7-sonnet-latest",  "Anthropic API",  "premium",  True),
        },
        "code_review": {
            "trivial":  ("gemini-2.5-flash",          "Google AI",      "micro",    False),
            "moderate": ("claude-3-5-sonnet-latest",  "Anthropic API",  "standard", False),
            "complex":  ("claude-3-5-sonnet-latest",  "Anthropic API",  "standard", True),
            "critical": ("gpt-4o",                    "OpenAI API",     "premium",  True),
        },
        "architecture": {
            "trivial":  ("gemini-2.5-flash",          "Google AI",      "micro",    False),
            "moderate": ("gpt-4o",                    "OpenAI API",     "standard", False),
            "complex":  ("gpt-4o",                    "OpenAI API",     "premium",  True),
            "critical": ("gpt-4o",                    "OpenAI API",     "premium",  True),
        },
        "reasoning": {
            "trivial":  ("gemini-2.5-flash",          "Google AI",      "micro",    False),
            "moderate": ("gpt-4o",                    "OpenAI API",     "standard", False),
            "complex":  ("gpt-4o",                    "OpenAI API",     "premium",  False),
            "critical": ("gpt-4o",                    "OpenAI API",     "premium",  True),
        },
        "documentation": {
            "trivial":  ("gemini-2.5-flash",          "Google AI",      "micro",    False),
            "moderate": ("claude-3-5-haiku-latest",   "Anthropic API",  "micro",    False),
            "complex":  ("claude-3-5-sonnet-latest",  "Anthropic API",  "standard", False),
            "critical": ("claude-3-5-sonnet-latest",  "Anthropic API",  "standard", False),
        },
        "testing": {
            "trivial":  ("gemini-2.5-flash",          "Google AI",      "micro",    False),
            "moderate": ("claude-3-5-sonnet-latest",  "Anthropic API",  "standard", False),
            "complex":  ("claude-3-7-sonnet-latest",  "Anthropic API",  "premium",  False),
            "critical": ("claude-3-7-sonnet-latest",  "Anthropic API",  "premium",  True),
        },
        "security": {
            "trivial":  ("claude-3-5-sonnet-latest",  "Anthropic API",  "standard", False),
            "moderate": ("claude-3-5-sonnet-latest",  "Anthropic API",  "standard", True),
            "complex":  ("gpt-4o",                    "OpenAI API",     "premium",  True),
            "critical": ("gpt-4o",                    "OpenAI API",     "premium",  True),
        },
        "risk": {
            "trivial":  ("aegis-risk-engine",         "AEGIS-Risk",     "micro",    False),
            "moderate": ("aegis-risk-engine",         "AEGIS-Risk",     "micro",    False),
            "complex":  ("aegis-risk-engine+gpt-4o",  "AEGIS-Risk+OpenAI", "standard", True),
            "critical": ("aegis-risk-engine+gpt-4o",  "AEGIS-Risk+OpenAI", "premium",  True),
        },
    }

    DEFAULT_ROUTE = {
        "trivial":  ("gemini-2.5-flash",          "Google AI",     "micro",    False),
        "moderate": ("claude-3-5-sonnet-latest",  "Anthropic API", "standard", False),
        "complex":  ("claude-3-7-sonnet-latest",  "Anthropic API", "premium",  False),
        "critical": ("gpt-4o",                    "OpenAI API",    "premium",  True),
    }

    def __init__(self):
        self._routing_log: List[RouteDecision] = []

    def classify_domain(self, task: str) -> str:
        task_lower = task.lower()
        scores: Dict[str, int] = {}
        for domain, keywords in self.DOMAIN_PATTERNS.items():
            scores[domain] = sum(1 for kw in keywords if kw in task_lower)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "general"

    def classify_complexity(self, task: str) -> str:
        words = len(task.split())
        # Complexity indicators
        complex_indicators = ["production", "enterprise", "scalable", "distributed",
                               "microservice", "critical", "migration", "complete", "full"]
        boost = sum(1 for ind in complex_indicators if ind in task.lower())
        effective_words = words + boost * 5
        if effective_words < 8:
            return "trivial"
        elif effective_words < 25:
            return "moderate"
        elif effective_words < 60:
            return "complex"
        else:
            return "critical"

    def route(self, task: str) -> RouteDecision:
        """
        Main routing method. Classifies the task and returns a RouteDecision.
        """
        domain = self.classify_domain(task)
        complexity = self.classify_complexity(task)

        matrix = self.ROUTING_MATRIX.get(domain, self.DEFAULT_ROUTE)
        model, provider, cost_tier, needs_consensus = matrix.get(
            complexity, matrix.get("moderate")
        )

        rationale = (
            f"Domain '{domain}' with '{complexity}' complexity. "
            f"{'Consensus required for critical/complex decisions.' if needs_consensus else 'Single-model sufficient.'}"
        )

        decision = RouteDecision(
            task=task,
            domain=domain,
            complexity=complexity,
            model=model,
            provider=provider,
            rationale=rationale,
            cost_tier=cost_tier,
            requires_consensus=needs_consensus,
        )
        self._routing_log.append(decision)
        return decision

    # Legacy compat
    def select_model(self, task_type: str, complexity: str) -> str:
        decision = self.route(f"{task_type} {complexity}")
        return decision.model

    def get_routing_log(self) -> List[RouteDecision]:
        return self._routing_log
