#!/usr/bin/env python3
from alembic.config import Config
from alembic import command
from pathlib import Path
import sys
import sqlite3

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

def main():
    cfg = Config(str(ROOT / 'alembic.ini'))
    cfg.set_main_option('script_location', 'alembic')
    cfg.set_main_option('sqlalchemy.url', 'sqlite:///'+ str(ROOT / 'api' / 'state.db'))
    # If the runs table already exists, stamp the head instead of attempting to recreate it.
    db_path = ROOT / 'api' / 'state.db'
    try:
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='runs'")
        exists = cur.fetchone() is not None
        conn.close()
    except Exception:
        exists = False

    try:
        if exists:
            command.stamp(cfg, 'head')
            print('Alembic stamp applied (runs table already existed).')
        else:
            command.upgrade(cfg, 'head')
            print('Alembic upgrade complete')
    except Exception as e:
        print('Alembic error:', e)

if __name__ == '__main__':
    main()
