# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman.
# All rights reserved.
# ==========================================

import importlib.util
import os
import json
import http.server
import socketserver
from pathlib import Path


class AEGISStudioHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/status":
            self._send_json(self._collect_status())
            return

        if self.path in ("/", "/index.html"):
            content = self._render_dashboard()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
            return

        if self.path.startswith('/static/'):
            try:
                base = Path(__file__).resolve().parent / 'static'
                rel = self.path[len('/static/'):]
                target = base / rel
                if target.exists() and target.is_file():
                    ct = 'text/html' if target.suffix == '.html' else 'application/octet-stream'
                    self.send_response(200)
                    self.send_header('Content-type', ct)
                    self.end_headers()
                    self.wfile.write(target.read_bytes())
                    return
            except Exception:
                pass

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(self._render_dashboard().encode("utf-8"))

    def _load_module(self, module_name: str, module_path: Path):
        try:
            spec = importlib.util.spec_from_file_location(module_name, str(module_path))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception:
            return None

    def _collect_status(self):
        base = Path(__file__).resolve().parent.parent
        payload = {
            "platform": "AEGIS Elite",
            "status": "DEGRADED",
            "governance_score": 0,
            "registry_loaded": 0,
            "registry_total": 0,
            "benchmark": {"aegis": 0},
            "capabilities": 0,
        }

        registry_mod = self._load_module("registry", base / "AEGIS-Kernel" / "registry.py")
        cap_graph_mod = self._load_module("capability_graph", base / "AEGIS-Kernel" / "capability_graph.py")
        policy_mod = self._load_module("policy_engine", base / "AEGIS-Governance" / "policy_engine.py")
        benchmark_mod = self._load_module("benchmark_runner", base / "AEGIS-Benchmark" / "runner.py")

        try:
            if registry_mod:
                registry = registry_mod.EngineRegistry(str(base))
                report = registry.boot()
                payload["registry_loaded"] = report.get("loaded", 0)
                payload["registry_total"] = report.get("total", 0)
                payload["status"] = "OPERATING" if report.get("loaded", 0) > 0 else "DEGRADED"

            if cap_graph_mod and registry_mod:
                if hasattr(cap_graph_mod.graph, "wire_from_registry") and registry_mod:
                    cap_graph_mod.graph.wire_from_registry(registry)
                payload["capabilities"] = len(cap_graph_mod.graph.list_capabilities())

            if policy_mod:
                governance = policy_mod.PolicyEngine(str(base)).evaluate()
                payload["governance_score"] = governance.get("governance_score", 0)

            if benchmark_mod:
                benchmark_report = benchmark_mod.BenchmarkEngine().run_benchmark(str(base)) if hasattr(benchmark_mod.BenchmarkEngine, 'run_benchmark') else None
                if benchmark_report and benchmark_report.get("results", {}).get("aegis"):
                    payload["benchmark"]["aegis"] = benchmark_report["results"]["aegis"]["score"]
        except Exception as exc:
            payload["error"] = str(exc)

        return payload

    def _send_json(self, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_raw_json(self, body: bytes):
      self.send_response(200)
      self.send_header("Content-type", "application/json")
      self.send_header("Content-Length", str(len(body)))
      self.end_headers()
      self.wfile.write(body)

    def _render_dashboard(self):
        return """
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <title>AEGIS Studio</title>
          <style>
            :root { color-scheme: dark; }
            body { margin:0; font-family: Inter, Segoe UI, Arial, sans-serif; background:#07111f; color:#e6f4ff; }
            .shell { max-width: 1180px; margin: 0 auto; padding: 28px; }
            .card { background: linear-gradient(135deg, #12253d, #09131f); border:1px solid #24415f; border-radius: 18px; padding: 22px; box-shadow: 0 16px 40px rgba(0,0,0,.35); margin-bottom: 18px; }
            h1 { margin:0 0 6px; font-size: 28px; }
            .pill { display:inline-block; padding:6px 10px; border-radius:999px; background:#103b5a; color:#76d7ff; font-size:12px; font-weight:700; margin-top:8px; }
            .grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
            .metric { background:#0b1727; border:1px solid #1f3650; border-radius: 14px; padding: 16px; }
            .metric .label { color:#7cb7e3; font-size:12px; text-transform:uppercase; letter-spacing:.16em; }
            .metric .value { font-size: 28px; font-weight: 700; margin-top: 8px; }
            .bar { height:10px; border-radius:999px; background:#1e2c3f; overflow:hidden; margin-top:10px; }
            .bar > span { display:block; height:100%; background:linear-gradient(90deg,#00d4ff,#7f5cff); }
            code { background:#0b1727; padding:2px 6px; border-radius:6px; }
          </style>
        </head>
        <body>
          <div class="shell">
            <div class="card">
              <h1>AEGIS Studio</h1>
              <div>Enterprise control plane for governance, runtime, and engineering intelligence.</div>
              <div class="pill">STATUS: OPERATING</div>
            </div>
            <div class="grid">
              <div class="metric"><div class="label">Governance Score</div><div class="value" id="gov">--</div></div>
              <div class="metric"><div class="label">Registry</div><div class="value" id="registry">--</div></div>
              <div class="metric"><div class="label">Benchmark</div><div class="value" id="benchmark">--</div></div>
            </div>
            <div class="card">
              <h2>Live System Snapshot</h2>
              <p>Use <code>python aegis.py status</code> and <code>python aegis.py benchmark</code> for CLI-based diagnostics.</p>
              <div class="bar"><span style="width:87%"></span></div>
            </div>
          </div>
          <script>
            async function refresh(){
              try {
                const response = await fetch('/api/status');
                const data = await response.json();
                document.getElementById('gov').textContent = data.governance_score + '/100';
                document.getElementById('registry').textContent = data.registry_loaded + '/' + data.registry_total;
                document.getElementById('benchmark').textContent = 'AEGIS ' + data.benchmark.aegis;
              } catch (e) {
                document.getElementById('gov').textContent = 'n/a';
              }
            }
            refresh();
            setInterval(refresh, 5000);
          </script>
        </body>
        </html>
        """


def run_studio(port: int = 8080):
    handler = AEGISStudioHandler
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        print(f"AEGIS Studio running at http://127.0.0.1:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    run_studio()
