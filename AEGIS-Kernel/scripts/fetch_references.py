# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

"""
AEGIS Elite - External Reference Fetcher
Clones key GitHub repositories as knowledge references into AEGIS-Knowledge/References
"""

import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS_DIR = os.path.join(BASE_DIR, "AEGIS-Knowledge", "References")

# Repositories to clone as knowledge/prompt references
REPOS = [
    {
        "name": "system-prompts-and-models",
        "url": "https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools.git",
        "reason": "System prompts of top AI tools (Cursor, Copilot, Devin)"
    },
    {
        "name": "letta-ai-skills",
        "url": "https://github.com/letta-ai/skills.git",
        "reason": "Memory management skills from Letta (MemGPT)"
    },
    {
        "name": "minimax-skills",
        "url": "https://github.com/MiniMax-AI/skills.git",
        "reason": "Agent skill patterns from MiniMax"
    },
    {
        "name": "cre-agent-skills",
        "url": "https://github.com/ahacker-1/cre-agent-skills.git",
        "reason": "Agent skill implementations"
    },
    {
        "name": "AI-research-skills",
        "url": "https://github.com/orchestra-research/AI-research-SKILLs.git",
        "reason": "Research-grade AI skills"
    },
    {
        "name": "PraisonAI",
        "url": "https://github.com/MervinPraison/PraisonAI.git",
        "reason": "Multi-agent framework for Consensus Engine reference"
    },
    {
        "name": "AutoGPT",
        "url": "https://github.com/Significant-Gravitas/AutoGPT.git",
        "reason": "Autonomous agent loop architecture reference",
        "depth": 1  # shallow clone - repo is huge
    },
    {
        "name": "hermes-agent",
        "url": "https://github.com/NousResearch/hermes-agent.git",
        "reason": "Local LLM agent architecture"
    },
    {
        "name": "firecrawl",
        "url": "https://github.com/mendableai/firecrawl.git",
        "reason": "Web scraping for real-time docs ingestion",
        "depth": 1
    },
    {
        "name": "notebooklm-mcp-cli",
        "url": "https://github.com/jacob-bd/notebooklm-mcp-cli.git",
        "reason": "NotebookLM-style RAG MCP CLI"
    },
]

def clone_repo(name: str, url: str, reason: str, depth: int = None):
    target = os.path.join(REFS_DIR, name)
    if os.path.exists(target):
        print(f"  [SKIP] {name} already exists.")
        return True
    
    print(f"  [CLONE] {name} — {reason}")
    cmd = ["git", "clone", "--quiet"]
    if depth:
        cmd += ["--depth", str(depth)]
    cmd += [url, target]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  [OK]   {name} cloned successfully.")
        return True
    else:
        print(f"  [ERR]  {name} failed: {result.stderr.strip()[:80]}")
        return False

def main():
    os.makedirs(REFS_DIR, exist_ok=True)
    print(f"\n{'='*60}")
    print("  AEGIS Elite — External Reference Fetcher")
    print(f"  Target: {REFS_DIR}")
    print(f"{'='*60}\n")
    
    success, failed = 0, 0
    for repo in REPOS:
        ok = clone_repo(
            repo["name"],
            repo["url"],
            repo["reason"],
            repo.get("depth")
        )
        if ok:
            success += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"  Done: {success} cloned, {failed} failed")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
