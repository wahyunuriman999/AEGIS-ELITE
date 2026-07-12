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

from governance import GovernanceEngine
from consensus import AIPairReview
from benchmark import BenchmarkEngine

class TestAegisElite(unittest.TestCase):
    def test_governance_engine(self):
        print("\n[TEST] Running Governance Engine Unit Test...")
        # Point to current directory to analyze itself
        engine = GovernanceEngine(".")
        report = engine.run_full_audit()
        
        self.assertIn("Architecture", report["scores"])
        self.assertIn("Security", report["scores"])
        self.assertTrue(report["scores"]["Architecture"] > 0)
        print(" -> Governance Engine parsed workspace and generated scores successfully.")

    def test_consensus_engine(self):
        print("\n[TEST] Running AI Pair Review Consensus Test...")
        review = AIPairReview()
        # The result is random, but we just verify it doesn't crash and returns a bool
        result = review.run_consensus("Test Refactoring")
        self.assertIsInstance(result, bool)
        print(f" -> Consensus Engine ran successfully (Result: {result}).")
        
    def test_benchmark_engine(self):
        print("\n[TEST] Running Benchmark Engine Test...")
        engine = BenchmarkEngine()
        # Assuming we just call it to ensure no exceptions
        engine.run_benchmark()
        print(" -> Benchmark Engine executed successfully.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
