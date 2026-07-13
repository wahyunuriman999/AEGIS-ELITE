# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

"""
AEGIS Compiler Output Contract
================================
The CompilerManifest is the SIGNED OUTPUT CONTRACT of every compilation run.
Anyone who receives compiled knowledge MUST check this manifest to verify:
  - What was compiled (source, version, hash)
  - When it was compiled (timestamp)
  - What the output looks like (stats, paths)
  - Whether the pipeline succeeded (stage results)
  - Whether this manifest is still valid (ttl)
"""

import json
import time
import hashlib
import os
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class CompilerManifest:
    """
    The signed output contract for AEGIS knowledge compilation.
    Every consumer of compiled knowledge must read this manifest first.
    """
    compiler_version: str
    knowledge_root: str
    total_nodes: int
    total_edges: int
    cache_path: str
    stage_results: List[Dict[str, Any]] = field(default_factory=list)

    # Auto-populated on write
    manifest_id: str = ""
    compiled_at: float = 0.0
    compiled_at_iso: str = ""
    ttl_seconds: int = 3600          # Cache valid for 1 hour
    signature: str = ""              # Content hash for integrity check
    status: str = "ok"

    def _compute_signature(self) -> str:
        content = f"{self.knowledge_root}:{self.total_nodes}:{self.total_edges}:{self.compiled_at}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def write(self, output_dir) -> str:
        """Finalize and write the manifest to disk. Returns the manifest path."""
        self.compiled_at = time.time()
        self.compiled_at_iso = time.strftime(
            "%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.compiled_at)
        )
        self.manifest_id = f"cm-{int(self.compiled_at)}"
        self.signature = self._compute_signature()

        # Determine overall status
        failed_stages = [s for s in self.stage_results if s.get("status") == "error"]
        self.status = "error" if failed_stages else (
            "warn" if any(s.get("status") == "warn" for s in self.stage_results) else "ok"
        )

        out_path = Path(output_dir) / "compiler_manifest.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=2)

        return str(out_path)

    @classmethod
    def load(cls, manifest_path: str) -> Optional["CompilerManifest"]:
        """Load and validate a manifest from disk."""
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            manifest = cls(**data)
            # Check TTL
            age = time.time() - manifest.compiled_at
            if age > manifest.ttl_seconds:
                print(f"  [Manifest] ⚠ Cache expired ({age:.0f}s > {manifest.ttl_seconds}s TTL)")
            return manifest
        except Exception as e:
            print(f"  [Manifest] ERROR loading manifest: {e}")
            return None

    def is_valid(self) -> bool:
        """Verify the manifest integrity signature."""
        expected = self._compute_signature()
        return self.signature == expected and self.status != "error"

    def display(self):
        """Print a formatted manifest summary."""
        status_color = {
            "ok":    "\033[92m✓ OK\033[0m",
            "warn":  "\033[93m⚠ WARN\033[0m",
            "error": "\033[91m✗ ERROR\033[0m",
        }.get(self.status, self.status)

        print(f"\n  ┌─ Compiler Manifest ──────────────────────────────────")
        print(f"  │  ID          : {self.manifest_id}")
        print(f"  │  Status      : {status_color}")
        print(f"  │  Compiled    : {self.compiled_at_iso}")
        print(f"  │  Source      : {self.knowledge_root}")
        print(f"  │  Nodes       : {self.total_nodes}")
        print(f"  │  Edges       : {self.total_edges}")
        print(f"  │  Cache       : {self.cache_path}")
        print(f"  │  Signature   : {self.signature}")
        print(f"  │  Valid       : {'Yes' if self.is_valid() else 'No — recompile required'}")
        print(f"  └─────────────────────────────────────────────────────\n")
