from flask import Flask, jsonify, request, abort
import os
import json
import sys
from pathlib import Path
from . import db as _db
import time

# Simple in-memory rate limiter (per-IP)
_RATE_LIMIT = {}
_RATE_LIMIT_WINDOW = 60  # seconds
_RATE_LIMIT_MAX = 120  # requests per window


app = Flask(__name__)
ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "api" / "state.json"

# API token (simple bearer token). If unset, auth is disabled.
API_TOKEN = os.environ.get("AEGIS_API_TOKEN")


def require_token():
    if not API_TOKEN:
        return True
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer ") and auth.split(" ", 1)[1] == API_TOKEN:
        return True
    abort(401)


def _rate_limited():
    # Allow only localhost access by default when proxy endpoints are used
    ip = request.remote_addr or "local"
    now = int(time.time())
    window = now - (now % _RATE_LIMIT_WINDOW)
    key = f"{ip}:{window}"
    _RATE_LIMIT.setdefault(key, 0)
    _RATE_LIMIT[key] += 1
    return _RATE_LIMIT[key] > _RATE_LIMIT_MAX


def load_state():
    # Legacy fallback; prefer SQLite
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    return {"runs": [], "status": "ready"}


def save_state(state):
    with DATA_FILE.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "aegis-api"})


@app.after_request
def set_secure_headers(response):
    # CORS for local studio; restrict in production
    response.headers.setdefault("Access-Control-Allow-Origin", "http://127.0.0.1:8080")
    response.headers.setdefault("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    response.headers.setdefault("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("Content-Security-Policy", "default-src 'self' 'unsafe-inline' http://127.0.0.1:8000 http://127.0.0.1:8080")
    return response


@app.get("/status")
def status():
    """Return live platform status using the local aegis runtime when available.

    Falls back to disk-backed state file if aegis runtime is not importable.
    """
    # Prefer live data from aegis.py
    try:
        sys.path.insert(0, str(ROOT))
        import aegis
        result = aegis.run_status()
        return jsonify({
            "platform": "AEGIS Elite",
            "status": "operating",
            "governance_score": result.get("governance", 0) if isinstance(result, dict) else 0,
            "registry_loaded": result.get("registry", {}).get("loaded", 0) if isinstance(result, dict) else 0,
            "registry_total": result.get("registry", {}).get("total", 0) if isinstance(result, dict) else 0,
        })
    except Exception:
        # SQLite fallback: ensure DB initialized
        try:
            _db.init_db()
            # migrate legacy state.json if present
            _db.migrate_from_state_json(Path(DATA_FILE))
            runs = _db.list_runs()
            latest = runs[0] if runs else None
            return jsonify({
                "platform": "AEGIS Elite",
                "status": "ready",
                "runs": len(runs),
                "latest": latest,
            })
        except Exception:
            state = load_state()
            return jsonify({
                "platform": "AEGIS Elite",
                "status": state.get("status", "ready"),
                "runs": len(state.get("runs", [])),
                "latest": state.get("runs", [])[-1] if state.get("runs") else None,
            })


@app.get("/benchmark")
def benchmark():
    """Run or return benchmark results using the aegis benchmark engine if available."""
    try:
        sys.path.insert(0, str(ROOT))
        import aegis
        report = aegis.run_benchmark()
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": "benchmark unavailable", "detail": str(e)}), 503


@app.post("/runs")
def create_run():
    require_token()
    payload = request.get_json(silent=True) or {}
    task = payload.get("task", "unspecified")
    status_val = payload.get("status", "completed")
    summary = payload.get("summary", "Execution completed")

    try:
        _db.init_db()
        new = _db.insert_run(task, status_val, summary)
        return jsonify(new), 201
    except Exception:
        # fallback to file-based
        state = load_state()
        run = {
            "id": len(state.get("runs", [])) + 1,
            "task": task,
            "status": status_val,
            "summary": summary,
        }
        state.setdefault("runs", []).append(run)
        state["status"] = "active"
        save_state(state)
        return jsonify(run), 201


@app.get("/runs")
def get_runs():
    require_token()
    try:
        _db.init_db()
        runs = _db.list_runs()
        return jsonify(runs)
    except Exception:
        state = load_state()
        return jsonify(state.get("runs", []))


@app.get("/proxy/runs")
def proxy_runs():
    """Proxy for the Studio to read recent runs without exposing the API token.

    Access is limited to local requests only.
    """
    # Simple guard: only allow local connections
    if request.remote_addr not in ("127.0.0.1", "::1", None):
        abort(403)
    # Optional shared secret header from Studio server
    proxy_secret = os.environ.get("STUDIO_PROXY_SECRET")
    if proxy_secret:
        hdr = request.headers.get("X-Proxy-Secret") or request.headers.get("X-Proxy-Token")
        if not hdr or hdr != proxy_secret:
            abort(403)
    if _rate_limited():
        return jsonify({"error": "rate_limited"}), 429
    try:
        _db.init_db()
        runs = _db.list_runs(limit=50)
        return jsonify(runs)
    except Exception:
        state = load_state()
        return jsonify(state.get("runs", []))


@app.get("/metrics")
def metrics():
    # Minimal internal metrics for health monitoring
    try:
        _db.init_db()
        runs = _db.list_runs(limit=100)
        return jsonify({"runs_total": len(runs)})
    except Exception:
        state = load_state()
        return jsonify({"runs_total": len(state.get("runs", []))})


if __name__ == "__main__":
    # Prefer a production-ready WSGI if available via environment
    use_waitress = os.environ.get("USE_WAITRESS") or os.environ.get("AEGIS_USE_WAITRESS")
    if use_waitress:
        try:
            from waitress import serve
            print("Starting with waitress on 127.0.0.1:8000")
            serve(app, host="127.0.0.1", port=8000)
        except Exception:
            print("waitress not available, falling back to Flask dev server")
            app.run(host="127.0.0.1", port=8000, debug=False)
    else:
        app.run(host="127.0.0.1", port=8000, debug=False)
