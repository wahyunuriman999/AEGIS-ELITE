# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

import os
import yaml
from importlib.util import spec_from_file_location, module_from_spec


class EngineRegistry:
    """
    Central Engine Registry powered by aegis_manifest.yaml.
    Loads and manages all AEGIS Elite engine modules dynamically.
    Prevents hardcoded imports and supports hot-reloading of engine packs.
    """

    def __init__(self, base_path: str = None):
        self.base_path = base_path or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.manifest_path = os.path.join(self.base_path, "aegis_manifest.yaml")
        self._engines = {}
        self._manifest = {}
        self._load_manifest()

    def _load_manifest(self):
        """Load the central AEGIS manifest YAML."""
        if not os.path.exists(self.manifest_path):
            raise FileNotFoundError(f"[AEGIS Registry] Manifest not found at: {self.manifest_path}")
        with open(self.manifest_path, "r") as f:
            self._manifest = yaml.safe_load(f)

    def _load_module_safe(self, name: str, path: str):
        """Dynamically load a Python module from a file path."""
        try:
            spec = spec_from_file_location(name, path)
            mod = module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
        except Exception as e:
            print(f"  [Registry] WARNING: Could not load engine '{name}' from '{path}': {e}")
            return None

    def load_all(self):
        """
        Load all active engines from the manifest.
        Returns a dict of { engine_id: module }.
        """
        sections = ["core", "elite", "platform", "labs"]
        for section in sections:
            engines_in_section = self._manifest.get(section, {})
            for engine_id, config in engines_in_section.items():
                if config.get("status") == "active":
                    module_dir = config.get("module", "")
                    entry_file = config.get("entry", "")
                    full_path = os.path.join(self.base_path, module_dir, entry_file)
                    module = self._load_module_safe(engine_id, full_path)
                    self._engines[engine_id] = module
        return self._engines

    def get(self, engine_id: str):
        """Retrieve a specific loaded engine by its ID."""
        return self._engines.get(engine_id)

    def list_engines(self):
        """List all registered engines and their load status."""
        sections = ["core", "elite", "platform", "labs"]
        print("\n========================================")
        print("       AEGIS ELITE ENGINE REGISTRY      ")
        print("========================================")
        for section in sections:
            engines_in_section = self._manifest.get(section, {})
            if engines_in_section:
                print(f"\n  [{section.upper()}]")
                for engine_id, config in engines_in_section.items():
                    status = config.get("status", "unknown")
                    loaded = engine_id in self._engines and self._engines[engine_id] is not None
                    icon = "\033[92m✓\033[0m" if loaded else ("\033[93m~\033[0m" if status == "planned" else "\033[91m✗\033[0m")
                    print(f"    {icon} {engine_id:<18} ({config.get('module','')}) - {config.get('description','')[:60]}")
        print("\n========================================\n")

    def get_packs(self):
        """Return the list of available extension packs."""
        return self._manifest.get("packs", [])
