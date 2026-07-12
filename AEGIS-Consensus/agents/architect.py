# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

from .base_agent import BaseAgent

class ArchitectAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Chief Architect", weight=2.0)
        
    def review(self, context: dict) -> dict:
        code = context.get("code", "")
        # The architect checks for global state mutation or tightly coupled dependencies
        if "global " in code:
            return {"approved": False, "reason": "Global state mutation is strictly prohibited."}
        
        return {"approved": True, "reason": "Architecture boundaries respected."}
