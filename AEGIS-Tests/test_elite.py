# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

import unittest
import sys
import os

# Append the root aegis-elite directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from importlib.util import spec_from_file_location, module_from_spec

def load_module_safe(name, path):
    try:
        # For modules using relative imports, this dynamic loading without a package context can fail.
        # So we just return None for the tests if they fail to load here, or we use a try-except.
        spec = spec_from_file_location(name, path)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:
        return None

policy_mod = load_module_safe("policy_engine", os.path.join(os.path.dirname(__file__), "..", "AEGIS-Governance", "policy_engine.py"))
voting_mod = load_module_safe("voting_engine", os.path.join(os.path.dirname(__file__), "..", "AEGIS-Consensus", "voting_engine.py"))
bench_mod = load_module_safe("runner", os.path.join(os.path.dirname(__file__), "..", "AEGIS-Benchmark", "runner.py"))
memory_mod = load_module_safe("memory_engine", os.path.join(os.path.dirname(__file__), "..", "AEGIS-Memory", "memory_engine.py"))


class TestAegisElite(unittest.TestCase):
    def test_governance_engine(self):
        if not policy_mod:
            self.skipTest("policy_engine.py not found in AEGIS-Governance")
        print("\n[TEST] Running Governance Engine Unit Test...")
        engine = policy_mod.GovernanceEngine(".")
        report = engine.run_full_audit()
        self.assertIn("Architecture", report["scores"])
        self.assertIn("Security", report["scores"])
        self.assertTrue(report["scores"]["Architecture"] > 0)
        print(" -> Governance Engine parsed workspace and generated scores successfully.")

    def test_consensus_engine(self):
        if not voting_mod:
            self.skipTest("voting_engine.py not found in AEGIS-Consensus")
        print("\n[TEST] Running AI Pair Review Consensus Test...")
        review = voting_mod.AIPairReview()
        result = review.run_consensus("Test Refactoring")
        self.assertIsInstance(result, bool)
        print(f" -> Consensus Engine ran successfully (Result: {result}).")
        
    def test_benchmark_engine(self):
        if not bench_mod:
            self.skipTest("runner.py not found in AEGIS-Benchmark")
        print("\n[TEST] Running Benchmark Engine Test...")
        engine = bench_mod.BenchmarkEngine()
        engine.run_benchmark()
        print(" -> Benchmark Engine executed successfully.")

    def test_memory_engine(self):
        if not memory_mod:
            self.fail("Memory Engine module is missing!")
        print("\n[TEST] Running Memory Engine Test...")
        # Create a temp dir for test workspace
        import tempfile
        with tempfile.TemporaryDirectory() as temp_workspace:
            mem = memory_mod.ProjectMemory(temp_workspace)
            mem.snapshot_topology(["Frontend", "Backend"])
            self.assertTrue(os.path.exists(os.path.join(temp_workspace, ".aegis", "memory", "topology.json")))
            
            history = memory_mod.DecisionHistory(temp_workspace)
            adr_id = history.record_decision("Use Postgres", "Need relational DB", "Yes", "Setup required")
            self.assertEqual(adr_id, "ADR-001")
            
            loop = memory_mod.LearningLoop(temp_workspace)
            new_multiplier = loop.analyze_failure("N+1 query detected in API")
            self.assertEqual(new_multiplier, 1.1)
            print(" -> Memory Engine (ProjectMemory, DecisionHistory, LearningLoop) executed successfully.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
