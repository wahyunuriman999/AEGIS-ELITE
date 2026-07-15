import sqlite3
from pathlib import Path
from typing import List, Dict, Any

DB_PATH = Path(__file__).resolve().parent / "state.db"


def _connect():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            status TEXT,
            summary TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()
    conn.close()


def insert_run(task: str, status: str, summary: str) -> Dict[str, Any]:
    conn = _connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO runs (task, status, summary) VALUES (?,?,?)", (task, status, summary))
    conn.commit()
    rowid = cur.lastrowid
    cur.execute("SELECT * FROM runs WHERE id = ?", (rowid,))
    row = cur.fetchone()
    conn.close()
    return dict(row)


def list_runs(limit: int = 100) -> List[Dict[str, Any]]:
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM runs ORDER BY id DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def migrate_from_state_json(state_json_path: Path):
    import json
    if not state_json_path.exists():
        return 0
    with state_json_path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    runs = data.get("runs") or []
    count = 0
    for r in runs:
        insert_run(r.get("task", "unspecified"), r.get("status", "completed"), r.get("summary", ""))
        count += 1
    return count
