# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

from typing import Dict, Any

class ExecutionContext:
    """
    Global Context Manager for AEGIS Elite.
    Holds state during the lifecycle of an engineering task.
    """
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path
        self.state: Dict[str, Any] = {}
        self.history: list = []

    def set(self, key: str, value: Any):
        self.state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)

    def record_step(self, step_name: str, result: str):
        self.history.append({"step": step_name, "result": result})
