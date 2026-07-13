# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

"""
AEGIS Compiler Pipeline — Official Compile Contract
====================================================
The Compiler answers: "Compile what? Into what?"

Official Pipeline:
  ┌─────────────────────────────────────────────────────┐
  │  INPUT: Raw Markdown / YAML / JSON Knowledge Files   │
  │            ↓ Stage 1: Tokenize & Parse               │
  │  Knowledge AST (Abstract Syntax Tree)                │
  │            ↓ Stage 2: Resolve References & Links     │
  │  Knowledge Graph (JSON-LD / NetworkX)                │
  │            ↓ Stage 3: Generate Embeddings            │
  │  Vector Index (FAISS / Chroma compatible)            │
  │            ↓ Stage 4: Compress & Cache               │
  │  Runtime Cache (aegis_runtime_cache.json)            │
  │            ↓ Stage 5: Write Manifest                 │
  │  OUTPUT: CompilerManifest (contract.py schema)       │
  └─────────────────────────────────────────────────────┘

Every run produces a CompilerManifest — the signed output contract
that guarantees what was compiled, when, and into what form.
"""

import os
import json
import time
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict


# ─── Data Structures ──────────────────────────────────────────────────────────

@dataclass
class KnowledgeNode:
    """A single node in the Knowledge AST."""
    id: str
    title: str
    source_path: str
    content_hash: str
    tags: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    depth: int = 0


@dataclass
class KnowledgeGraph:
    """The compiled Knowledge Graph."""
    nodes: List[KnowledgeNode] = field(default_factory=list)
    edges: List[Dict[str, str]] = field(default_factory=list)  # {from, to, relation}
    total_nodes: int = 0
    total_edges: int = 0

    def add_node(self, node: KnowledgeNode):
        self.nodes.append(node)
        self.total_nodes = len(self.nodes)

    def add_edge(self, from_id: str, to_id: str, relation: str = "references"):
        self.edges.append({"from": from_id, "to": to_id, "relation": relation})
        self.total_edges = len(self.edges)


@dataclass
class PipelineStageResult:
    stage: str
    status: str          # "ok" | "warn" | "error"
    items_processed: int
    elapsed_ms: float
    notes: str = ""


# ─── Pipeline Stages ──────────────────────────────────────────────────────────

class CompilerPipeline:
    """
    AEGIS Knowledge Compiler Pipeline.
    Transforms raw knowledge files into a structured, indexed, cacheable format.
    """

    def __init__(self, knowledge_root: str, output_dir: str):
        self.knowledge_root = Path(knowledge_root)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.graph = KnowledgeGraph()
        self.stage_results: List[PipelineStageResult] = []

    # ── Stage 1: Tokenize & Parse ────────────────────────────────────────────
    def stage_parse(self) -> List[KnowledgeNode]:
        """Scan knowledge root and parse all .md / .yaml / .json files into AST nodes."""
        start = time.time()
        nodes: List[KnowledgeNode] = []
        extensions = {".md", ".yaml", ".yml", ".json"}

        if not self.knowledge_root.exists():
            self.stage_results.append(PipelineStageResult(
                stage="1-Parse", status="warn", items_processed=0,
                elapsed_ms=0, notes=f"Knowledge root not found: {self.knowledge_root}"
            ))
            return []

        for file_path in self.knowledge_root.rglob("*"):
            if file_path.suffix.lower() not in extensions:
                continue
            try:
                raw = file_path.read_text(encoding="utf-8", errors="ignore")
                content_hash = hashlib.md5(raw.encode()).hexdigest()[:8]
                node = KnowledgeNode(
                    id=content_hash,
                    title=file_path.stem.replace("_", " ").title(),
                    source_path=str(file_path),
                    content_hash=content_hash,
                    tags=self._extract_tags(raw),
                    depth=len(file_path.relative_to(self.knowledge_root).parts) - 1,
                )
                nodes.append(node)
            except Exception:
                pass

        elapsed = (time.time() - start) * 1000
        self.stage_results.append(PipelineStageResult(
            stage="1-Parse", status="ok", items_processed=len(nodes), elapsed_ms=elapsed
        ))
        return nodes

    # ── Stage 2: Build Knowledge Graph ───────────────────────────────────────
    def stage_build_graph(self, nodes: List[KnowledgeNode]) -> KnowledgeGraph:
        """Link nodes by shared tags to form the Knowledge Graph."""
        start = time.time()
        for node in nodes:
            self.graph.add_node(node)

        # Simple reference resolution: shared tags → edge
        tag_index: Dict[str, List[str]] = {}
        for node in nodes:
            for tag in node.tags:
                tag_index.setdefault(tag, []).append(node.id)

        for tag, node_ids in tag_index.items():
            for i in range(len(node_ids) - 1):
                self.graph.add_edge(node_ids[i], node_ids[i + 1], relation=f"shares:{tag}")

        elapsed = (time.time() - start) * 1000
        self.stage_results.append(PipelineStageResult(
            stage="2-Graph", status="ok",
            items_processed=self.graph.total_edges, elapsed_ms=elapsed,
            notes=f"{self.graph.total_nodes} nodes, {self.graph.total_edges} edges"
        ))
        return self.graph

    # ── Stage 3: Embeddings (stub — real impl uses sentence-transformers) ─────
    def stage_embed(self, nodes: List[KnowledgeNode]) -> Dict[str, List[float]]:
        """Stub for vector embedding generation. Returns dummy vectors for now."""
        start = time.time()
        embeddings = {
            node.id: [hash(node.content_hash + str(i)) % 100 / 100.0 for i in range(8)]
            for node in nodes
        }
        elapsed = (time.time() - start) * 1000
        self.stage_results.append(PipelineStageResult(
            stage="3-Embed", status="ok", items_processed=len(embeddings),
            elapsed_ms=elapsed, notes="Stub embeddings (256-dim in production)"
        ))
        return embeddings

    # ── Stage 4: Write Runtime Cache ─────────────────────────────────────────
    def stage_cache(self, graph: KnowledgeGraph, embeddings: Dict) -> str:
        """Write the compiled output to the runtime cache."""
        start = time.time()
        cache_path = self.output_dir / "aegis_knowledge_cache.json"
        cache = {
            "compiled_at": time.time(),
            "graph": {
                "total_nodes": graph.total_nodes,
                "total_edges": graph.total_edges,
                "nodes": [vars(n) for n in graph.nodes[:100]],  # cap for perf
                "edges": graph.edges[:200],
            },
            "embeddings_count": len(embeddings),
        }
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)
        elapsed = (time.time() - start) * 1000
        self.stage_results.append(PipelineStageResult(
            stage="4-Cache", status="ok", items_processed=1,
            elapsed_ms=elapsed, notes=str(cache_path)
        ))
        return str(cache_path)

    # ── Stage 5: Write Manifest (Output Contract) ─────────────────────────────
    def stage_manifest(self, cache_path: str) -> "CompilerManifest":
        """Write the CompilerManifest — the signed output contract."""
        from AEGIS_Compiler_contract import CompilerManifest  # noqa
        manifest = CompilerManifest(
            compiler_version="1.0.0",
            knowledge_root=str(self.knowledge_root),
            total_nodes=self.graph.total_nodes,
            total_edges=self.graph.total_edges,
            cache_path=cache_path,
            stage_results=[asdict(sr) for sr in self.stage_results],
        )
        manifest.write(self.output_dir)
        return manifest

    # ── Public: Run Full Pipeline ─────────────────────────────────────────────
    def compile(self) -> "CompilerManifest":
        """Run the full 5-stage pipeline and return the CompilerManifest."""
        print("\n  [Compiler] ⚙  Starting Knowledge Compilation Pipeline...")
        nodes      = self.stage_parse()
        graph      = self.stage_build_graph(nodes)
        embeddings = self.stage_embed(nodes)
        cache_path = self.stage_cache(graph, embeddings)

        # Print stage summary
        for sr in self.stage_results:
            icon = "\033[92m✓\033[0m" if sr.status == "ok" else "\033[93m⚠\033[0m"
            print(f"  [Compiler]  {icon} Stage {sr.stage:<12} "
                  f"{sr.items_processed:>5} items  {sr.elapsed_ms:>7.1f}ms  {sr.notes}")

        # Import contract here to avoid circular
        import importlib.util, os as _os
        spec = importlib.util.spec_from_file_location(
            "contract",
            _os.path.join(_os.path.dirname(__file__), "contract.py")
        )
        contract_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(contract_mod)

        manifest = contract_mod.CompilerManifest(
            compiler_version="1.0.0",
            knowledge_root=str(self.knowledge_root),
            total_nodes=self.graph.total_nodes,
            total_edges=self.graph.total_edges,
            cache_path=cache_path,
            stage_results=[asdict(sr) for sr in self.stage_results],
        )
        manifest.write(self.output_dir)
        print(f"  [Compiler] ✅ Manifest written → {self.output_dir / 'compiler_manifest.json'}\n")
        return manifest

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _extract_tags(self, content: str) -> List[str]:
        """Extract hashtag-style tags from markdown content."""
        import re
        tags = re.findall(r"#([a-zA-Z][a-zA-Z0-9_-]*)", content)
        return list(set(tags[:10]))  # cap at 10 tags per file
