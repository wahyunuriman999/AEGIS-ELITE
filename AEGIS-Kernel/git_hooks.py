# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

import os
import stat

PRE_COMMIT_HOOK_TEMPLATE = """#!/usr/bin/env bash
# AEGIS Elite Pre-Commit Hook

echo "=========================================================="
echo "🛡️  AEGIS ELITE: Running Pre-Commit Pipeline..."
echo "=========================================================="

# Run the full AEGIS pipeline
aegis pipeline --task "Pre-commit Review" --path .

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ AEGIS VERDICT: BLOCKED. Fix the issues before committing."
    echo "=========================================================="
    exit 1
fi

echo ""
echo "✅ AEGIS VERDICT: APPROVED. Safe to commit."
echo "=========================================================="
exit 0
"""

class GitHooksManager:
    """Manages integration of AEGIS with Git repository hooks."""
    
    def __init__(self, workspace_path: str = "."):
        self.workspace_path = os.path.abspath(workspace_path)
        self.git_dir = os.path.join(self.workspace_path, ".git")
        self.hooks_dir = os.path.join(self.git_dir, "hooks")
        self.pre_commit_path = os.path.join(self.hooks_dir, "pre-commit")

    def install_pre_commit(self) -> bool:
        """Installs the AEGIS pipeline as a pre-commit hook."""
        if not os.path.exists(self.git_dir):
            print(f"\n  ❌ No .git directory found in {self.workspace_path}")
            print("  Initialize a git repository first using 'git init'.\n")
            return False

        os.makedirs(self.hooks_dir, exist_ok=True)
        
        print(f"\n  📥 Installing AEGIS pre-commit hook into {self.pre_commit_path}...")
        
        with open(self.pre_commit_path, "w", encoding="utf-8") as f:
            f.write(PRE_COMMIT_HOOK_TEMPLATE)
            
        # Make executable
        st = os.stat(self.pre_commit_path)
        os.chmod(self.pre_commit_path, st.st_mode | stat.S_IEXEC)
        
        print(f"  ✅ \033[92mSuccessfully installed AEGIS pre-commit hook!\033[0m")
        print("  AEGIS will now review every commit automatically.\n")
        return True
