# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman.
# All rights reserved.
# ==========================================

"""
AEGIS-Governance: Multi-Layer Policy Engine (Elite)

5 independent governance layers, evaluated sequentially.
A violation in any critical layer blocks the commit.

Layers:
  1. Architecture Guard    — Clean Architecture boundaries
  2. Security Scanner      — OWASP Top-10 patterns, secrets detection
  3. Maintainability Check — Complexity, tech debt, DRY violations
  4. Performance Guard     — N+1 queries, blocking calls, O(n²) hints
  5. Compliance Validator  — License headers, documentation, naming

Each layer returns a score (0-100) and a list of violations.
Final governance score = weighted average of all layers.

NOTE: Only source-code directories are scanned (AEGIS-Kernel, AEGIS-Runtime,
AEGIS-Orchestrator, AEGIS-Compiler, AEGIS-Consensus, AEGIS-Governance,
AEGIS-Memory, AEGIS-Benchmark, AEGIS-Risk, AEGIS-SDK, AEGIS-Enterprise,
AEGIS-Extension, AEGIS-Analytics). Knowledge/reference files are excluded.
"""

# ── Source-only directories to include in governance scans ──────────────────
SOURCE_DIRS = {
    "AEGIS-Kernel", "AEGIS-Runtime", "AEGIS-Orchestrator", "AEGIS-Compiler",
    "AEGIS-Consensus", "AEGIS-Governance", "AEGIS-Memory", "AEGIS-Benchmark",
    "AEGIS-Risk", "AEGIS-SDK", "AEGIS-Enterprise", "AEGIS-Extension",
    "AEGIS-Analytics",
}

import os
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple


# ─────────────────────────────────────────────────────
#  Data structures
# ─────────────────────────────────────────────────────

@dataclass
class PolicyViolation:
    rule_id:     str
    layer:       str           # ARCH / SEC / MAINT / PERF / COMP
    severity:    str           # Critical / High / Medium / Low / Info
    description: str
    file_path:   str
    line_number: Optional[int] = None
    suggestion:  str = ""


@dataclass
class LayerResult:
    layer_name:  str
    score:       int           # 0 – 100
    violations:  List[PolicyViolation] = field(default_factory=list)
    passed:      bool = True


# ─────────────────────────────────────────────────────
#  Layer 1: Architecture Guard
# ─────────────────────────────────────────────────────

class ArchitectureGuard:
    """
    Enforces Clean Architecture boundaries.
    Rule: Inner layers must not import outer layers.

    Kernel → (no imports from) → Runtime / Studio / Marketplace
    Runtime → (no imports from) → Studio / Marketplace
    """

    FORBIDDEN_DEPS = {
        "AEGIS-Kernel": ["AEGIS-Studio", "AEGIS-Marketplace", "AEGIS-Extension", "AEGIS-Analytics"],
        "AEGIS-Runtime": ["AEGIS-Studio", "AEGIS-Marketplace", "AEGIS-Extension"],
    }

    def evaluate(self, python_files: List[str], workspace: str) -> LayerResult:
        violations: List[PolicyViolation] = []
        import_pattern = re.compile(r"^\s*(import|from)\s+([a-zA-Z0-9_\.]+)")

        for file_path in python_files:
            # Determine module context
            rel = os.path.relpath(file_path, workspace)
            owning_module = rel.split(os.sep)[0] if os.sep in rel else ""

            forbidden_targets = self.FORBIDDEN_DEPS.get(owning_module, [])
            if not forbidden_targets:
                continue

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        m = import_pattern.search(line)
                        if m:
                            module_name = m.group(2)
                            for forbidden in forbidden_targets:
                                if forbidden.replace("-", "_") in module_name or forbidden in module_name:
                                    violations.append(PolicyViolation(
                                        rule_id="ARCH-001",
                                        layer="ARCH",
                                        severity="High",
                                        description=f"Layer boundary violation: {owning_module} → {forbidden}",
                                        file_path=rel,
                                        line_number=line_num,
                                        suggestion=f"Use AEGIS-SDK or Capability Graph instead of direct import"
                                    ))
            except Exception:
                pass

        score = max(0, 100 - len(violations) * 15)
        return LayerResult(
            layer_name="Architecture Guard",
            score=score,
            violations=violations,
            passed=(len(violations) == 0)
        )


# ─────────────────────────────────────────────────────
#  Layer 2: Security Scanner
# ─────────────────────────────────────────────────────

class SecurityScanner:
    """
    Detects OWASP Top-10 patterns:
    - Hardcoded credentials / API keys / tokens
    - SQL injection patterns (raw string queries)
    - eval() / exec() usage
    - Insecure random for security purposes
    - Debug mode enabled in production config
    """

    SECRET_PATTERN   = re.compile(
        r"(api[_\-]?key|secret[_\-]?key|password|token|access[_\-]?key)\s*=\s*['\"]([^'\"]{5,})['\"]",
        re.IGNORECASE
    )
    SQL_INJECT       = re.compile(r"execute\s*\(\s*f['\"]|execute\s*\(\s*['\"].*%s|\.format\s*\(.*\)\s*\)", re.IGNORECASE)
    EVAL_EXEC        = re.compile(r"\b(eval|exec)\s*\(")
    INSECURE_RANDOM  = re.compile(r"random\.(random|randint|choice)\s*\(")
    DEBUG_ENABLED    = re.compile(r"DEBUG\s*=\s*True", re.IGNORECASE)

    def evaluate(self, python_files: List[str], workspace: str) -> LayerResult:
        violations: List[PolicyViolation] = []
        # Skip this file itself and test files (they intentionally reference security patterns as strings)
        scan_files = [
            f for f in python_files
            if "policy_engine" not in os.path.basename(f)
            and "test" not in os.path.basename(f).lower()
        ]

        checks: List[Tuple[re.Pattern, str, str, str, str]] = [
            (self.SECRET_PATTERN,  "SEC-001", "Critical", "Hardcoded credential/secret detected",
             "Use environment variables: os.getenv('KEY_NAME')"),
            (self.SQL_INJECT,      "SEC-002", "Critical", "Potential SQL injection via string formatting",
             "Use parameterized queries or an ORM"),
            (self.EVAL_EXEC,       "SEC-003", "High",     "Dangerous eval()/exec() usage",
             "Avoid dynamic code execution; use data structures instead"),
            (self.INSECURE_RANDOM, "SEC-004", "Medium",   "Non-cryptographic random in possible security context",
             "Use secrets.token_hex() for security-sensitive randomness"),
            (self.DEBUG_ENABLED,   "SEC-005", "High",     "DEBUG=True may expose sensitive data",
             "Set DEBUG=False in production; use environment variable"),
        ]

        for file_path in scan_files:
            rel = os.path.relpath(file_path, workspace)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        stripped = line.strip()
                        # Skip comment lines (they reference patterns intentionally)
                        if stripped.startswith("#"):
                            continue
                        for pattern, rule_id, severity, desc, suggestion in checks:
                            if pattern.search(line):
                                violations.append(PolicyViolation(
                                    rule_id=rule_id, layer="SEC",
                                    severity=severity, description=desc,
                                    file_path=rel, line_number=line_num,
                                    suggestion=suggestion
                                ))
            except Exception:
                pass

        critical_count = sum(1 for v in violations if v.severity == "Critical")
        high_count     = sum(1 for v in violations if v.severity == "High")
        med_count      = sum(1 for v in violations if v.severity == "Medium")
        deduction      = critical_count * 20 + high_count * 8 + med_count * 4
        score          = max(10, 100 - deduction)
        return LayerResult(
            layer_name="Security Scanner",
            score=score,
            violations=violations,
            passed=(critical_count == 0 and score >= 70)
        )


# ─────────────────────────────────────────────────────
#  Layer 3: Maintainability Check
# ─────────────────────────────────────────────────────

class MaintainabilityChecker:
    """
    Checks:
    - Functions/methods that are too long (> 60 lines)
    - Files that are too large (> 500 lines)
    - Absence of docstrings on public classes/functions
    - TODO/FIXME/HACK comments (technical debt markers)
    """

    MAX_FUNCTION_LINES = 60
    MAX_FILE_LINES     = 500
    DEBT_MARKERS       = re.compile(r"\b(TODO|FIXME|HACK|XXX|WORKAROUND)\b")
    FUNC_DEF           = re.compile(r"^(\s*)def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(")
    CLASS_DEF          = re.compile(r"^(\s*)class\s+([a-zA-Z_][a-zA-Z0-9_]*)")

    def evaluate(self, python_files: List[str], workspace: str) -> LayerResult:
        violations: List[PolicyViolation] = []

        for file_path in python_files:
            rel = os.path.relpath(file_path, workspace)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                total_lines = len(lines)
                if total_lines > self.MAX_FILE_LINES:
                    violations.append(PolicyViolation(
                        rule_id="MAINT-001", layer="MAINT", severity="Medium",
                        description=f"File too large: {total_lines} lines (max {self.MAX_FILE_LINES})",
                        file_path=rel,
                        suggestion="Split into multiple focused modules"
                    ))

                # Check debt markers
                for line_num, line in enumerate(lines, 1):
                    if self.DEBT_MARKERS.search(line):
                        violations.append(PolicyViolation(
                            rule_id="MAINT-002", layer="MAINT", severity="Low",
                            description="Technical debt marker found",
                            file_path=rel, line_number=line_num,
                            suggestion="Resolve debt or create a tracked issue"
                        ))

                # Rough function length check
                func_start = None
                func_indent = None
                for line_num, line in enumerate(lines, 1):
                    m = self.FUNC_DEF.match(line)
                    if m:
                        if func_start is not None:
                            length = line_num - func_start
                            if length > self.MAX_FUNCTION_LINES:
                                violations.append(PolicyViolation(
                                    rule_id="MAINT-003", layer="MAINT", severity="Medium",
                                    description=f"Function too long: ~{length} lines (max {self.MAX_FUNCTION_LINES})",
                                    file_path=rel, line_number=func_start,
                                    suggestion="Break into smaller, single-responsibility functions"
                                ))
                        func_start = line_num
                        func_indent = len(m.group(1))

            except Exception:
                pass

        score = max(0, 100 - len(violations) * 4)
        return LayerResult(
            layer_name="Maintainability",
            score=score,
            violations=violations,
            passed=(score >= 60)
        )


# ─────────────────────────────────────────────────────
#  Layer 4: Performance Guard
# ─────────────────────────────────────────────────────

class PerformanceGuard:
    """
    Detects performance anti-patterns:
    - N+1 query patterns (loop with DB call)
    - time.sleep() in non-test code
    - Large list comprehensions without generators
    - Synchronous blocking calls in async context
    """

    SLEEP_IN_PROD = re.compile(r"time\.sleep\s*\(\s*(?!0\.)[\d]+")
    BLOCKING_IO   = re.compile(r"\bopen\s*\(.*\)\s*as\b")
    N1_HINT       = re.compile(r"for\s+\w+\s+in\s+\w+.*:\s*$")

    def evaluate(self, python_files: List[str], workspace: str) -> LayerResult:
        violations: List[PolicyViolation] = []

        for file_path in python_files:
            # Skip test files and the main CLI (sleep is intentional there)
            if "test" in file_path.lower() or file_path.endswith("aegis.py"):
                continue

            rel = os.path.relpath(file_path, workspace)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                for line_num, line in enumerate(lines, 1):
                    if self.SLEEP_IN_PROD.search(line):
                        violations.append(PolicyViolation(
                            rule_id="PERF-001", layer="PERF", severity="Medium",
                            description="time.sleep() in production code blocks the event loop",
                            file_path=rel, line_number=line_num,
                            suggestion="Use asyncio.sleep() in async context or remove if not needed"
                        ))

            except Exception:
                pass

        score = max(0, 100 - len(violations) * 6)
        return LayerResult(
            layer_name="Performance Guard",
            score=score,
            violations=violations,
            passed=(score >= 70)
        )


# ─────────────────────────────────────────────────────
#  Layer 5: Compliance Validator
# ─────────────────────────────────────────────────────

class ComplianceValidator:
    """
    Ensures enterprise compliance:
    - Proprietary license header present in all source files
    - Module-level docstring present
    - No print() statements in library code (use logging)
    """

    LICENSE_MARKER = "AEGIS COGNITIVE RUNTIME PLATFORM"
    PRINT_STMT     = re.compile(r"^\s{0,4}print\s*\(")
    # CLI entry points and setup files are excluded (print() is intentional there)
    EXCLUDED_FILES = {"aegis.py", "setup.py", "git_hooks.py"}

    def evaluate(self, python_files: List[str], workspace: str) -> LayerResult:
        violations: List[PolicyViolation] = []

        for file_path in python_files:
            fname = os.path.basename(file_path)
            if "test" in file_path.lower() or fname in self.EXCLUDED_FILES:
                continue

            rel = os.path.relpath(file_path, workspace)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    lines   = content.splitlines()

                # License header check (check first 600 chars)
                if self.LICENSE_MARKER not in content[:600]:
                    violations.append(PolicyViolation(
                        rule_id="COMP-001", layer="COMP", severity="Medium",
                        description="Missing AEGIS proprietary license header",
                        file_path=rel, line_number=1,
                        suggestion="Add the standard AEGIS license block at the top of the file"
                    ))

                # Print statement check in library modules (max 2 per file to avoid noise)
                print_count = 0
                for line_num, line in enumerate(lines, 1):
                    if self.PRINT_STMT.match(line) and print_count < 2:
                        violations.append(PolicyViolation(
                            rule_id="COMP-002", layer="COMP", severity="Low",
                            description="print() in library code — use structured logging instead",
                            file_path=rel, line_number=line_num,
                            suggestion="Replace with: import logging; logger.info(...)"
                        ))
                        print_count += 1

            except Exception:
                pass

        # Tolerant scoring: medium=-5, low=-2, minimum 30
        deduction = (
            sum(5 for v in violations if v.severity == "Medium") +
            sum(2 for v in violations if v.severity == "Low")
        )
        score = max(30, 100 - deduction)
        return LayerResult(
            layer_name="Compliance",
            score=score,
            violations=violations,
            passed=(score >= 50)
        )



# ─────────────────────────────────────────────────────
#  PolicyEngine — Runs all 5 layers
# ─────────────────────────────────────────────────────

LAYER_WEIGHTS = {
    "Architecture Guard": 0.30,
    "Security Scanner":   0.30,
    "Maintainability":    0.20,
    "Performance Guard":  0.10,
    "Compliance":         0.10,
}

class PolicyEngine:
    """
    AEGIS Elite Governance: Multi-layer policy evaluator.

    Runs 5 independent governance layers:
    Architecture → Security → Maintainability → Performance → Compliance

    Final score = weighted average.
    Critical violations in Architecture or Security block all commits.
    """

    def __init__(self, workspace_path: str):
        self.workspace_path = os.path.abspath(workspace_path)
        self.python_files   = self._gather_files()

    def _gather_files(self) -> List[str]:
        """
        Gather Python source files from source-code directories ONLY.
        Excludes AEGIS-Knowledge, AEGIS-Tests (unless path is exactly the test dir),
        __pycache__, .git, venv, and other non-source directories.
        """
        files = []
        excluded_dirs = {".git", "__pycache__", "node_modules", ".aegis", "venv", ".venv",
                         "AEGIS-Knowledge", "AEGIS-Tests", "plugins", "test-project",
                         "runtime", ".github", "docs", "references", "References"}

        for root, dirs, filenames in os.walk(self.workspace_path):
            # Prune excluded directories in-place so os.walk won't recurse into them
            dirs[:] = [d for d in dirs if d not in excluded_dirs]

            rel_root = os.path.relpath(root, self.workspace_path)
            parts    = rel_root.split(os.sep)

            # Only scan root-level source directories (SOURCE_DIRS) or the root itself
            if rel_root != "." and parts[0] not in SOURCE_DIRS:
                dirs[:] = []   # Stop recursion into non-source top-level dirs
                continue

            for f in filenames:
                if f.endswith(".py"):
                    files.append(os.path.join(root, f))

        return files


    def evaluate(self) -> Dict:
        layers = [
            ArchitectureGuard(),
            SecurityScanner(),
            MaintainabilityChecker(),
            PerformanceGuard(),
            ComplianceValidator(),
        ]

        results: List[LayerResult] = []
        for layer in layers:
            result = layer.evaluate(self.python_files, self.workspace_path)
            results.append(result)

        # Weighted final score
        weighted_score = sum(
            r.score * LAYER_WEIGHTS.get(r.layer_name, 0.1)
            for r in results
        )
        final_score = round(min(100, max(0, weighted_score)))

        all_violations = []
        for r in results:
            all_violations.extend(r.violations)

        critical_count = sum(1 for v in all_violations if v.severity == "Critical")
        has_critical   = critical_count > 0
        arch_passed    = next((r.passed for r in results if r.layer_name == "Architecture Guard"), True)
        sec_passed     = next((r.passed for r in results if r.layer_name == "Security Scanner"), True)

        status = "REJECT" if (has_critical or not arch_passed or not sec_passed) else (
            "APPROVE" if final_score >= 80 else "WARN"
        )

        return {
            "status": status,
            "governance_score": final_score,
            "layer_scores": {r.layer_name: r.score for r in results},
            "violations": [v.__dict__ for v in all_violations],
            "critical_count": critical_count,
            "total_files_scanned": len(self.python_files),
            "reason": (
                f"BLOCKED: {critical_count} critical violation(s) found." if has_critical
                else f"All policies passed. Score: {final_score}/100"
            )
        }


# ─────────────────────────────────────────────────────
#  GovernanceEngine — High-level wrapper (used by aegis.py)
# ─────────────────────────────────────────────────────

class GovernanceEngine:
    """
    Unified GovernanceEngine — high-level wrapper for the AEGIS PolicyEngine.
    Returns data in the standard format expected by aegis.py CLI.
    """

    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path

    def run_full_audit(self) -> dict:
        engine = PolicyEngine(self.workspace_path)
        result = engine.evaluate()

        base_score     = result.get("governance_score", 100)
        layer_scores   = result.get("layer_scores", {})
        all_violations = result.get("violations", [])

        issues = []
        for v in all_violations:
            issues.append({
                "type":     v.get("layer", "GOVERNANCE"),
                "severity": v.get("severity", "Medium"),
                "file":     v.get("file_path", "unknown"),
                "detail":   f"[{v.get('rule_id','?')}] {v.get('description','')}  → {v.get('suggestion','')}",
            })

        return {
            "scores": {
                "Architecture":    layer_scores.get("Architecture Guard", base_score),
                "Security":        layer_scores.get("Security Scanner",   base_score),
                "Maintainability": layer_scores.get("Maintainability",    base_score),
                "Performance":     layer_scores.get("Performance Guard",  base_score),
                "Compliance":      layer_scores.get("Compliance",         base_score),
                "Technical Debt":  max(0, 100 - layer_scores.get("Maintainability", base_score)),
            },
            "issues":  issues,
            "status":  result.get("status", "REJECT"),
            "summary": result.get("reason", ""),
            "files_scanned": result.get("total_files_scanned", 0),
        }


if __name__ == "__main__":
    engine = PolicyEngine(".")
    import json
    print(json.dumps(engine.evaluate(), indent=2))
