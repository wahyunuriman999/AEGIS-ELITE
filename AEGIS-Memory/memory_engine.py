# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman.
# All rights reserved.
# ==========================================

"""
AEGIS-Memory: Cognitive Memory Engine (Elite)

Three memory subsystems that give AEGIS a persistent "brain":

1. ProjectMemory      — Architecture topology snapshots over time
2. DecisionHistory    — Architecture Decision Records (ADR) ledger
3. LearningLoop       — Adapts governance strictness from past failures
4. CognitiveSummary   — Cross-session intelligence: trends, patterns, velocity

Together these enable AEGIS to remember *why* decisions were made,
not just *what* was decided.
"""

import json
import os
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _read_json(path: str, default: Any) -> Any:
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _write_json(path: str, data: Any) -> None:
    _ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ─────────────────────────────────────────────────────
#  1. ProjectMemory — Architecture topology over time
# ─────────────────────────────────────────────────────

class ProjectMemory:
    """
    Tracks and diffs architecture topology snapshots.
    Each snapshot records which components exist, their relationships,
    and the quality scores at the time of the scan.
    """

    def __init__(self, workspace_path: str):
        self.workspace     = workspace_path
        self.memory_dir    = os.path.join(workspace_path, ".aegis", "memory")
        self.topology_file = os.path.join(self.memory_dir, "topology.json")
        _ensure_dir(self.memory_dir)
        if not os.path.exists(self.topology_file):
            _write_json(self.topology_file, {"snapshots": [], "current": None})

    def snapshot_topology(self, components: List[Dict], scores: Optional[Dict] = None) -> Dict:
        """
        Save a new topology snapshot and compute drift from the previous one.

        Args:
            components: List of component dicts {name, type, dependencies, ...}
            scores:     Optional governance scores at time of snapshot

        Returns:
            {"snapshot_id": str, "drift": {...}}
        """
        data     = _read_json(self.topology_file, {"snapshots": [], "current": None})
        previous = data.get("current")

        snapshot = {
            "id":         f"SNAP-{len(data['snapshots']) + 1:04d}",
            "timestamp":  _utcnow(),
            "components": components,
            "scores":     scores or {},
        }

        # Compute drift
        drift = {}
        if previous:
            prev_names = {c["name"] for c in previous.get("components", [])}
            curr_names = {c["name"] for c in components}
            drift = {
                "added":   list(curr_names - prev_names),
                "removed": list(prev_names - curr_names),
                "stable":  list(curr_names & prev_names),
            }

        data["snapshots"].append(snapshot)
        data["current"] = snapshot
        _write_json(self.topology_file, data)

        return {"snapshot_id": snapshot["id"], "drift": drift}

    def get_history(self, limit: int = 5) -> List[Dict]:
        """Return the last N topology snapshots."""
        data = _read_json(self.topology_file, {"snapshots": []})
        return data["snapshots"][-limit:]

    def compare(self, snap_a_id: str, snap_b_id: str) -> Dict:
        """Diff two snapshots by ID."""
        data  = _read_json(self.topology_file, {"snapshots": []})
        snaps = {s["id"]: s for s in data["snapshots"]}
        a, b  = snaps.get(snap_a_id), snaps.get(snap_b_id)
        if not a or not b:
            return {"error": f"Snapshot not found: {snap_a_id or snap_b_id}"}

        a_names = {c["name"] for c in a.get("components", [])}
        b_names = {c["name"] for c in b.get("components", [])}
        return {
            "from":    snap_a_id,
            "to":      snap_b_id,
            "added":   list(b_names - a_names),
            "removed": list(a_names - b_names),
            "stable":  list(a_names & b_names),
        }


# ─────────────────────────────────────────────────────
#  2. DecisionHistory — Architecture Decision Records
# ─────────────────────────────────────────────────────

class DecisionHistory:
    """
    Immutable ledger of Architecture Decision Records (ADRs).

    An ADR captures:
    - WHY a decision was made (context)
    - WHAT was decided
    - The consequences (trade-offs)
    - Who approved it (agents)
    """

    def __init__(self, workspace_path: str):
        self.ledger_file = os.path.join(workspace_path, ".aegis", "memory", "decisions.json")
        _ensure_dir(os.path.dirname(self.ledger_file))
        if not os.path.exists(self.ledger_file):
            _write_json(self.ledger_file, [])

    def record_decision(
        self,
        title:          str,
        context:        str,
        decision:       str,
        consequences:   str,
        approved_by:    Optional[List[str]] = None,
        tags:           Optional[List[str]]  = None,
    ) -> str:
        """
        Append a new ADR.

        Returns:
            The ADR ID (e.g. "ADR-042")
        """
        ledger = _read_json(self.ledger_file, [])
        adr_id = f"ADR-{len(ledger) + 1:03d}"

        adr = {
            "id":           adr_id,
            "date":         _utcnow(),
            "title":        title,
            "context":      context,
            "decision":     decision,
            "consequences": consequences,
            "approved_by":  approved_by or ["AEGIS-Consensus"],
            "tags":         tags or [],
            "status":       "accepted",
        }
        ledger.append(adr)
        _write_json(self.ledger_file, ledger)
        return adr_id

    def list_decisions(self, tag: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Return recent ADRs, optionally filtered by tag."""
        ledger = _read_json(self.ledger_file, [])
        if tag:
            ledger = [a for a in ledger if tag in a.get("tags", [])]
        return ledger[-limit:]

    def deprecate(self, adr_id: str, reason: str) -> bool:
        """Mark an ADR as deprecated (decisions evolve)."""
        ledger = _read_json(self.ledger_file, [])
        for adr in ledger:
            if adr["id"] == adr_id:
                adr["status"]      = "deprecated"
                adr["deprecated_at"] = _utcnow()
                adr["deprecated_reason"] = reason
                _write_json(self.ledger_file, ledger)
                return True
        return False


# ─────────────────────────────────────────────────────
#  3. LearningLoop — Adaptive governance from failures
# ─────────────────────────────────────────────────────

class LearningLoop:
    """
    Analyzes past failures to adapt future governance rules.

    After repeated failures:
    - Strictness multiplier increases (up to 2.0×)
    - Specific anti-patterns are added to the blocked list
    - Governance thresholds are auto-tightened

    This is what makes AEGIS Elite progressively smarter over time.
    """

    DEFAULT_RULES = {
        "strictness_multiplier": 1.0,
        "blocked_patterns": [],
        "failure_counts": {},
        "auto_tightened_rules": [],
        "learning_events": [],
    }

    # Patterns that trigger auto-blocking after repeated failures
    PATTERN_MAP = {
        "n+1 query":       "N1_QUERY_FORBIDDEN",
        "hardcoded secret": "HARDCODED_SECRET_FORBIDDEN",
        "layer violation":  "LAYER_BOUNDARY_FORBIDDEN",
        "eval usage":       "EVAL_EXEC_FORBIDDEN",
        "debug mode":       "DEBUG_IN_PROD_FORBIDDEN",
    }

    def __init__(self, workspace_path: str):
        self.rules_file = os.path.join(workspace_path, ".aegis", "memory", "learned_rules.json")
        _ensure_dir(os.path.dirname(self.rules_file))
        if not os.path.exists(self.rules_file):
            _write_json(self.rules_file, self.DEFAULT_RULES)

    def analyze_failure(self, failure_context: str, severity: str = "High") -> Dict:
        """
        Record a failure and adapt rules.

        Args:
            failure_context: Description of what failed
            severity: Critical / High / Medium / Low

        Returns:
            Updated rules dict
        """
        rules = _read_json(self.rules_file, self.DEFAULT_RULES)
        ctx   = failure_context.lower()

        # Increase strictness for high/critical failures
        if severity in ("Critical", "High"):
            rules["strictness_multiplier"] = min(2.0, rules["strictness_multiplier"] + 0.15)
        else:
            rules["strictness_multiplier"] = min(2.0, rules["strictness_multiplier"] + 0.05)

        # Track failure counts per context keyword
        for keyword, pattern_id in self.PATTERN_MAP.items():
            if keyword in ctx:
                count = rules["failure_counts"].get(keyword, 0) + 1
                rules["failure_counts"][keyword] = count

                # Auto-block after 3 repeated failures of the same type
                if count >= 3 and pattern_id not in rules["blocked_patterns"]:
                    rules["blocked_patterns"].append(pattern_id)
                    rules["auto_tightened_rules"].append({
                        "pattern":     pattern_id,
                        "blocked_at":  _utcnow(),
                        "after_count": count,
                        "reason":      f"Auto-blocked after {count} repeated violations: {keyword}",
                    })

        # Log learning event
        rules["learning_events"].append({
            "timestamp": _utcnow(),
            "context":   failure_context[:120],
            "severity":  severity,
            "multiplier_now": rules["strictness_multiplier"],
        })
        # Keep only last 50 events
        rules["learning_events"] = rules["learning_events"][-50:]

        _write_json(self.rules_file, rules)
        return rules

    def get_current_rules(self) -> Dict:
        return _read_json(self.rules_file, self.DEFAULT_RULES)

    def reset(self) -> None:
        """Reset the learning loop (use with care)."""
        _write_json(self.rules_file, self.DEFAULT_RULES)


# ─────────────────────────────────────────────────────
#  4. CognitiveSummary — Cross-session intelligence
# ─────────────────────────────────────────────────────

class CognitiveSummary:
    """
    Aggregates cross-session intelligence:
    - Score trends (improving / declining / stable)
    - Most frequent violation categories
    - Engineering velocity (tasks per session)
    - Recommendations based on patterns

    This is the "brain" that makes AEGIS Elite progressively
    more valuable the longer you use it.
    """

    def __init__(self, workspace_path: str):
        self.summary_file = os.path.join(workspace_path, ".aegis", "memory", "cognitive_summary.json")
        _ensure_dir(os.path.dirname(self.summary_file))
        if not os.path.exists(self.summary_file):
            _write_json(self.summary_file, {
                "sessions": [],
                "score_history": [],
                "violation_frequency": {},
                "recommendations": [],
            })

    def record_session(self, scores: Dict, violations: List[Dict], tasks_completed: int = 0) -> Dict:
        """Record a governance session and update cognitive patterns."""
        data = _read_json(self.summary_file, {
            "sessions": [], "score_history": [], "violation_frequency": {}, "recommendations": []
        })

        session = {
            "timestamp":       _utcnow(),
            "scores":          scores,
            "violation_count": len(violations),
            "tasks_completed": tasks_completed,
        }
        data["sessions"].append(session)
        data["sessions"] = data["sessions"][-100:]  # Keep last 100

        # Score trend
        avg_score = sum(scores.values()) / len(scores) if scores else 0
        data["score_history"].append({"timestamp": _utcnow(), "avg": round(avg_score, 1)})
        data["score_history"] = data["score_history"][-30:]

        # Violation frequency
        for v in violations:
            category = v.get("type", "UNKNOWN")
            data["violation_frequency"][category] = data["violation_frequency"].get(category, 0) + 1

        # Generate recommendations
        recommendations = []
        freq = data["violation_frequency"]
        top_category = max(freq, key=freq.get) if freq else None
        if top_category:
            recommendations.append(
                f"Most frequent issue: {top_category} ({freq[top_category]} occurrences). "
                f"Consider a dedicated refactor sprint."
            )

        # Score trend analysis
        history = data["score_history"]
        if len(history) >= 3:
            recent  = sum(h["avg"] for h in history[-3:]) / 3
            earlier = sum(h["avg"] for h in history[-6:-3]) / 3 if len(history) >= 6 else recent
            if recent < earlier - 5:
                recommendations.append("⚠️  Quality score declining. Schedule a governance review session.")
            elif recent > earlier + 5:
                recommendations.append("✅ Quality score improving. Keep up the governance discipline.")

        data["recommendations"] = recommendations[-5:]
        _write_json(self.summary_file, data)

        return {
            "session_id":      f"SESSION-{len(data['sessions']):04d}",
            "avg_score":       round(avg_score, 1),
            "trend":           "improving" if len(history) >= 2 and history[-1]["avg"] >= history[-2]["avg"] else "declining",
            "recommendations": recommendations,
        }

    def get_insights(self) -> Dict:
        """Return cross-session intelligence summary."""
        data = _read_json(self.summary_file, {
            "sessions": [], "score_history": [], "violation_frequency": {}, "recommendations": []
        })

        history = data.get("score_history", [])
        avg     = sum(h["avg"] for h in history[-10:]) / max(len(history[-10:]), 1)

        return {
            "total_sessions":      len(data.get("sessions", [])),
            "avg_score_last_10":   round(avg, 1),
            "top_violations":      sorted(data.get("violation_frequency", {}).items(), key=lambda x: -x[1])[:5],
            "recommendations":     data.get("recommendations", []),
            "score_history":       history[-10:],
        }


# ─────────────────────────────────────────────────────
#  MemoryEngine — Unified facade (used by aegis.py)
# ─────────────────────────────────────────────────────

class MemoryEngine:
    """
    High-level facade for all AEGIS memory subsystems.
    Used directly by the CLI and other AEGIS modules.
    """

    def __init__(self, workspace_path: str = "."):
        self.workspace  = workspace_path
        self.project    = ProjectMemory(workspace_path)
        self.decisions  = DecisionHistory(workspace_path)
        self.learning   = LearningLoop(workspace_path)
        self.cognitive  = CognitiveSummary(workspace_path)

    def save_session(
        self,
        task:       str,
        scores:     Dict,
        violations: List[Dict],
        approved:   bool,
        agents:     Optional[List[str]] = None,
    ) -> str:
        """
        Save a complete engineering session to memory.

        Returns:
            ADR ID if a decision was recorded, else ""
        """
        # Record cognitive session
        self.cognitive.record_session(scores, violations)

        # If not approved, feed to learning loop
        if not approved:
            for v in violations[:3]:
                self.learning.analyze_failure(
                    failure_context=v.get("detail", task),
                    severity=v.get("severity", "Medium")
                )

        # Record ADR for every approved task
        if approved:
            adr_id = self.decisions.record_decision(
                title=f"Task approved: {task[:60]}",
                context=f"Governance scores: {scores}",
                decision=f"Approved by AEGIS Consensus",
                consequences="Change committed to codebase.",
                approved_by=agents or ["AEGIS-Consensus"],
                tags=["auto-generated"],
            )
            return adr_id

        return ""

    def get_summary(self) -> Dict:
        """Return a quick cross-session summary for `aegis status`."""
        insights = self.cognitive.get_insights()
        rules    = self.learning.get_current_rules()
        recent   = self.decisions.list_decisions(limit=3)

        return {
            "total_sessions":   insights["total_sessions"],
            "avg_score":        insights["avg_score_last_10"],
            "strictness":       rules["strictness_multiplier"],
            "blocked_patterns": rules["blocked_patterns"],
            "recent_adrs":      [{"id": a["id"], "title": a["title"]} for a in recent],
            "recommendations":  insights["recommendations"],
        }

    def list_decisions(self, limit: int = 10) -> List[Dict]:
        return self.decisions.list_decisions(limit=limit)
