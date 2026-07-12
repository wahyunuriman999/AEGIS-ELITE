# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler


TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


def _load_dashboard_data() -> dict:
    """Build the project health data payload for the dashboard."""
    return {
        "scores": {
            "architecture": 9.8,
            "security": 9.2,
            "performance": 8.7,
            "dx": 7.5,
            "risk": 35
        },
        "pipeline": {
            "risk": {"level": "MEDIUM", "score": 35, "status": "OK"},
            "governance": {"architecture": 98, "security": 92},
            "memory": {"adr": "ADR-003"},
            "consensus": {"approved": True, "votes": "5/5"}
        },
        "engines": [
            {"id": "AEGIS-Kernel", "status": "ACTIVE"},
            {"id": "AEGIS-Governance", "status": "ACTIVE"},
            {"id": "AEGIS-Consensus", "status": "ACTIVE"},
            {"id": "AEGIS-Memory", "status": "ACTIVE"},
            {"id": "AEGIS-Risk", "status": "ACTIVE"},
            {"id": "AEGIS-Benchmark", "status": "ACTIVE"},
            {"id": "AEGIS-Workflow", "status": "ACTIVE"},
            {"id": "AEGIS-Marketplace", "status": "ACTIVE"},
            {"id": "AEGIS-Analytics", "status": "PLANNED"},
        ]
    }


class StudioHandler(BaseHTTPRequestHandler):
    """HTTP handler for the AEGIS Elite Studio dashboard."""

    def _serve_file(self, path: str, content_type: str):
        if os.path.exists(path):
            with open(path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.end_headers()
            self.wfile.write(content)
        else:
            self._not_found()

    def _not_found(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Not Found")

    def do_GET(self):
        if self.path in ("/", "/dashboard"):
            dashboard_path = os.path.join(TEMPLATES_DIR, "dashboard.html")
            self._serve_file(dashboard_path, "text/html; charset=utf-8")

        elif self.path == "/api/health":
            data = _load_dashboard_data()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

        else:
            self._not_found()

    def log_message(self, format, *args):
        pass  # Suppress default request logs; we handle our own


def run_studio(host: str = "localhost", port: int = 8080):
    """Start the AEGIS Elite Studio web server."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, StudioHandler)
    print(f"\n  🖥️  AEGIS Elite Studio is running!")
    print(f"  → Open in browser: \033[94mhttp://{host}:{port}\033[0m")
    print(f"  → API Health:       \033[94mhttp://{host}:{port}/api/health\033[0m")
    print(f"\n  Press Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Studio stopped.")
        httpd.server_close()


if __name__ == "__main__":
    run_studio()
