# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

from typing import Callable, Dict, List, Any

class EventBus:
    """
    Central Pub/Sub Event Bus for AEGIS Elite.
    Decouples core engines by allowing them to emit and listen to events.
    """
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event_type: str, payload: Any = None):
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(payload)
