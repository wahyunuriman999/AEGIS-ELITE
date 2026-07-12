# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

from typing import List
from .agents.base_agent import BaseAgent
from .agents.architect import ArchitectAgent

class VotingEngine:
    """
    AEGIS Consensus: Aggregates votes from multiple AI Pair Programming Agents.
    """
    def __init__(self):
        self.agents: List[BaseAgent] = [
            ArchitectAgent(),
            # SecurityAgent(), ProgrammerAgent(), etc. would be added here
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
                
        # Must have at least 80% weighted approval and NO vetoes from high-weight agents
        passed = (approvals / total_weight >= 0.8) and len(vetoes) == 0
        
        return {
            "consensus_reached": passed,
            "approval_rate": approvals / total_weight,
            "vetoes": vetoes
        }

if __name__ == "__main__":
    engine = VotingEngine()
    print(engine.execute_consensus({"code": "def func():\n  global state\n  state = 1"}))
