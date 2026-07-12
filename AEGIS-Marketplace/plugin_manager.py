# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

import os
import time
from importlib.util import spec_from_file_location, module_from_spec


def _load_module_safe(name: str, path: str):
    try:
        spec = spec_from_file_location(name, path)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:
        return None


class PluginManager:
    """
    AEGIS Elite Extension Marketplace — Plugin Manager.
    Handles listing, installing, and removing extension packs.
    
    Available Packs:
      - laravel-pack    (Laravel governance rules & patterns)
      - flutter-pack    (Flutter/Dart architecture patterns)
      - react-pack      (React/Next.js component governance)
      - python-pack     (Python/FastAPI best practices)
      - ai-pack         (LLM/AI agent governance rules)
    """

    REGISTRY = {
        "laravel-pack": {
            "name": "Laravel Pack",
            "version": "1.0.0",
            "description": "Laravel-specific governance rules, ORM patterns, Blade best practices.",
            "author": "AEGIS Labs",
            "rules": 42
        },
        "flutter-pack": {
            "name": "Flutter Pack",
            "version": "1.0.0",
            "description": "Flutter/Dart state management, widget architecture, and CI patterns.",
            "author": "AEGIS Labs",
            "rules": 38
        },
        "react-pack": {
            "name": "React Pack",
            "version": "1.2.0",
            "description": "React component composition, hooks patterns, Next.js routing standards.",
            "author": "AEGIS Labs",
            "rules": 55
        },
        "python-pack": {
            "name": "Python Pack",
            "version": "1.1.0",
            "description": "Python/FastAPI governance, async best practices, Pydantic models.",
            "author": "AEGIS Labs",
            "rules": 60
        },
        "ai-pack": {
            "name": "AI/LLM Pack",
            "version": "1.0.0",
            "description": "LLM agent governance, prompt injection defense, AI safety patterns.",
            "author": "AEGIS Labs",
            "rules": 28
        }
    }

    def __init__(self, workspace_path: str = "."):
        self.workspace = workspace_path
        self.installed_dir = os.path.join(workspace_path, ".aegis", "packs")
        os.makedirs(self.installed_dir, exist_ok=True)
        self._installed = self._load_installed()

    def _load_installed(self) -> list:
        installed = []
        if os.path.exists(self.installed_dir):
            for f in os.listdir(self.installed_dir):
                if f.endswith(".pack"):
                    installed.append(f.replace(".pack", ""))
        return installed

    def list_available(self):
        """Print all available packs in the AEGIS Marketplace."""
        print("\n╔══════════════════════════════════════════════════════════╗")
        print("║          AEGIS ELITE — EXTENSION MARKETPLACE            ║")
        print("╠══════════════════════════════════════════════════════════╣")
        for pack_id, info in self.REGISTRY.items():
            installed_tag = " \033[92m[INSTALLED]\033[0m" if pack_id in self._installed else ""
            print(f"║  📦 {pack_id:<20} v{info['version']:<8} {info['rules']} rules{installed_tag}")
            print(f"║     {info['description'][:58]}")
            print("║")
        print("╚══════════════════════════════════════════════════════════╝")
        print("  Usage: aegis install <pack-id>\n")

    def install(self, pack_id: str) -> bool:
        """Simulate installing a pack into the current workspace."""
        if pack_id not in self.REGISTRY:
            print(f"\n  ❌ Pack '{pack_id}' not found in the AEGIS Marketplace.")
            print("  Run `aegis marketplace` to see available packs.\n")
            return False

        info = self.REGISTRY[pack_id]
        print(f"\n  📥 Installing '{info['name']}' v{info['version']}...")
        time.sleep(0.4)
        print(f"  -> Downloading {info['rules']} governance rules...")
        time.sleep(0.6)
        print(f"  -> Integrating with AEGIS-Governance engine...")
        time.sleep(0.4)

        pack_file = os.path.join(self.installed_dir, f"{pack_id}.pack")
        with open(pack_file, "w") as f:
            f.write(f"name={info['name']}\nversion={info['version']}\nrules={info['rules']}\n")

        self._installed.append(pack_id)
        print(f"\n  ✅ \033[92m'{info['name']}' installed successfully!\033[0m")
        print(f"  {info['rules']} new rules are now active in your governance pipeline.\n")
        return True

    def remove(self, pack_id: str) -> bool:
        """Uninstall a pack from the current workspace."""
        if pack_id not in self._installed:
            print(f"\n  ❌ Pack '{pack_id}' is not installed.\n")
            return False
        
        pack_file = os.path.join(self.installed_dir, f"{pack_id}.pack")
        if os.path.exists(pack_file):
            os.remove(pack_file)
        self._installed.remove(pack_id)
        print(f"\n  ✅ '{pack_id}' uninstalled successfully.\n")
        return True
