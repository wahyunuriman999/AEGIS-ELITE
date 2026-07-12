# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

import re
import os

class GovernanceEngine:
    def __init__(self, workspace_path):
        self.workspace_path = workspace_path
        self.scores = {
            "Architecture": 95,
            "Security": 90,
            "Performance": 88,
            "Maintainability": 92,
            "Documentation": 90,
            "Technical Debt": 8
        }
        self.issues = []

    def audit_file(self, file_path):
        """Perform static analysis on a single code file for clean code, SOLID, and security issues."""
        if not os.path.exists(file_path):
            return
            
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.splitlines()

        filename = os.path.basename(file_path)
        
        # 1. Clean Code Checks
        long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 100]
        if long_lines:
            self.issues.append({
                "type": "Clean Code",
                "severity": "Low",
                "file": filename,
                "detail": f"Lines exceed 100 chars: {long_lines[:5]}..."
            })
            self.scores["Maintainability"] -= min(len(long_lines) * 0.5, 5)

        # Large functions check
        funcs = re.findall(r'def\s+(\w+)\(.*?\):', content)
        large_methods = []
        current_func = None
        func_lines = 0
        for i, line in enumerate(lines):
            match = re.match(r'^\s*def\s+(\w+)', line)
            if match:
                if current_func and func_lines > 50:
                    large_methods.append(current_func)
                current_func = match.group(1)
                func_lines = 0
            elif current_func:
                if line.strip() != "":
                    func_lines += 1
        if large_methods:
            self.issues.append({
                "type": "Clean Code",
                "severity": "Medium",
                "file": filename,
                "detail": f"Functions exceed 50 lines: {large_methods}"
            })
            self.scores["Maintainability"] -= len(large_methods) * 2

        # 2. Security Checks
        secret_patterns = [r'(?i)api_key\s*=\s*["\'][a-zA-Z0-9_\-]{16,}["\']', r'(?i)password\s*=\s*["\'][a-zA-Z0-9_\-]{8,}["\']']
        for pattern in secret_patterns:
            matches = re.findall(pattern, content)
            if matches:
                self.issues.append({
                    "type": "Security",
                    "severity": "High",
                    "file": filename,
                    "detail": "Potential hardcoded secret or API credential detected."
                })
                self.scores["Security"] -= 15

        if "eval(" in content or "exec(" in content:
            self.issues.append({
                "type": "Security",
                "severity": "High",
                "file": filename,
                "detail": "Use of dangerous functions (eval/exec) detected."
            })
            self.scores["Security"] -= 20

        # 3. SOLID / Architecture Checks
        classes = re.findall(r'class\s+(\w+)', content)
        for cls in classes:
            cls_def_start = re.search(r'class\s+' + cls, content)
            if cls_def_start:
                cls_content = content[cls_def_start.start():]
                next_class = re.search(r'\nclass\s+', cls_content[1:])
                if next_class:
                    cls_content = cls_content[:next_class.start()+1]
                methods_count = len(re.findall(r'def\s+\w+', cls_content))
                if methods_count > 15:
                    self.issues.append({
                        "type": "Architecture",
                        "severity": "Medium",
                        "file": filename,
                        "detail": f"Class '{cls}' violates Single Responsibility Principle (SRP) with {methods_count} methods."
                    })
                    self.scores["Architecture"] -= 5

    def run_full_audit(self):
        """Scans the workspace directory."""
        for root, _, files in os.walk(self.workspace_path):
            if '.git' in root or '__pycache__' in root or 'node_modules' in root:
                continue
            for file in files:
                if file.endswith('.py'):
                    self.audit_file(os.path.join(root, file))

        for k in self.scores:
            if k == "Technical Debt":
                self.scores[k] = max(0, min(100, int(len(self.issues) * 1.5)))
            else:
                self.scores[k] = max(0, min(100, int(self.scores[k])))

        return {
            "scores": self.scores,
            "issues": self.issues
        }

if __name__ == "__main__":
    import sys
    workspace = sys.argv[1] if len(sys.argv) > 1 else "."
    engine = GovernanceEngine(workspace)
    report = engine.run_full_audit()
    print("Governance Scores:")
    for k, v in report["scores"].items():
        print(f"  {k}: {v}")
    print(f"\nFound {len(report['issues'])} issues.")
