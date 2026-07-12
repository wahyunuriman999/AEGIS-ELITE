# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name: str, weight: float = 1.0):
        self.name = name
        self.weight = weight
        
    @abstractmethod
    def review(self, context: dict) -> dict:
        """Must return a dict with 'approved' (bool) and 'reason' (str)"""
        pass
