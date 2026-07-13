from pathlib import Path
from . import db

MIGRATION_TABLE = "migrations"


def init_migrations():
    conn = db._connect()
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {MIGRATION_TABLE} (name TEXT PRIMARY KEY, applied_at TEXT DEFAULT (datetime('now')))")
    conn.commit()
    conn.close()


def applied_migrations():
    conn = db._connect()
    cur = conn.cursor()
    cur.execute(f"SELECT name FROM {MIGRATION_TABLE}")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return set(rows)


def apply_migration(name: str, sql: str):
    conn = db._connect()
    cur = conn.cursor()
    cur.executescript(sql)
    cur.execute(f"INSERT OR REPLACE INTO {MIGRATION_TABLE} (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


def ensure_base():
    init_migrations()
    applied = applied_migrations()
    if '000_create_runs' not in applied:
        apply_migration('000_create_runs', """
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            status TEXT,
            summary TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );
        """)
