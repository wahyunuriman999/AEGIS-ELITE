# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

import time
import random

class ConsensusAgent:
    def __init__(self, role, strictness):
        self.role = role
        self.strictness = strictness  # 0.0 to 1.0

    def review(self, task_context):
        # Simulate agent reviewing the code based on its role and strictness
        print(f"[{self.role}] Analyzing context...")
        time.sleep(0.3)
        
        # Simulated logic: higher strictness means higher chance of rejection
        approval_chance = 1.0 - (self.strictness * 0.4)
        approved = random.random() < approval_chance
        
        if approved:
            reason = "Meets all criteria for this domain."
        else:
            if self.role == "Security":
                reason = "Potential vulnerability detected in data handling."
            elif self.role == "Architect":
                reason = "Violates dependency inversion principle."
            elif self.role == "Performance":
                reason = "O(n^2) complexity found in core loop."
            else:
                reason = "Code does not meet quality standards."
                
        return {"approved": approved, "reason": reason}

class AIPairReview:
    def __init__(self):
        self.agents = [
            ConsensusAgent("Programmer", 0.2),    # Usually optimistic
            ConsensusAgent("Reviewer", 0.6),      # Standard code reviewer
            ConsensusAgent("Architect", 0.8),     # Strict on patterns
            ConsensusAgent("Security", 0.9),      # Very strict on vulnerabilities
            ConsensusAgent("Performance", 0.7)    # Strict on efficiency
        ]

    def run_consensus(self, task_context="Architecture Refactoring"):
        print(f"\n--- Initiating AI Pair Review Consensus ---")
        print(f"Task: {task_context}\n")
        
        votes = []
        for agent in self.agents:
            vote = agent.review(task_context)
            votes.append(vote)
            status = "APPROVE" if vote["approved"] else "REJECT"
            color_code = "\033[92m" if vote["approved"] else "\033[91m"
            reset_code = "\033[0m"
            print(f"{color_code}[{status}]{reset_code} {agent.role}: {vote['reason']}")
            
        approvals = sum(1 for v in votes if v["approved"])
        total = len(self.agents)
        
        print("\n--- Consensus Results ---")
        print(f"Approvals: {approvals}/{total}")
        
        # Require 100% consensus from Architect and Security, and at least 4/5 overall
        security_approved = votes[3]["approved"]
        architect_approved = votes[2]["approved"]
        
        if approvals >= 4 and security_approved and architect_approved:
            print("\033[92m[CONSENSUS REACHED] Proceeding with execution.\033[0m")
            return True
        else:
            print("\033[91m[CONSENSUS FAILED] Re-routing to Planning Phase for revision.\033[0m")
            if not security_approved:
                print(" -> Security vetoed the change.")
            if not architect_approved:
                print(" -> Architect vetoed the change.")
            return False

if __name__ == "__main__":
    review = AIPairReview()
    # Force seed for consistent demonstration in benchmark or tests
    # random.seed(42) 
    review.run_consensus("Refactor User Authentication Module")
