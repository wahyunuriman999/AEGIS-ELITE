import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestCoreImprovements(unittest.TestCase):
    def test_policy_engine_flags_hardcoded_secret(self):
        policy_module = load_module("policy_engine", "AEGIS-Governance/policy_engine.py")

        with tempfile.TemporaryDirectory() as tmpdir:
            sample_path = Path(tmpdir) / "sample.py"
            sample_path.write_text(
                "API_KEY = 'super-secret-value'\n"
                "def run():\n"
                "    return 'ok'\n",
                encoding="utf-8",
            )

            engine = policy_module.PolicyEngine(str(Path(tmpdir)))
            result = engine.evaluate()

            self.assertIn(result["status"], {"REJECT", "WARN"})
            self.assertGreater(result["critical_count"], 0)
            self.assertGreaterEqual(result["governance_score"], 0)

    def test_benchmark_engine_returns_structured_report(self):
        benchmark_module = load_module("benchmark_runner", "AEGIS-Benchmark/runner.py")

        engine = benchmark_module.BenchmarkEngine()
        report = engine.run_benchmark()

        self.assertIn("summary", report)
        self.assertIn("results", report)
        self.assertIn("aegis", report["results"])
        self.assertIn("score", report["results"]["aegis"])
        self.assertGreaterEqual(report["results"]["aegis"]["score"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
