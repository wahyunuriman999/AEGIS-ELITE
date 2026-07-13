#!/usr/bin/env python3
import sqlite3

def main():
    conn = sqlite3.connect('api/state.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print('tables:', cur.fetchall())
    try:
        cur.execute("SELECT count(*) FROM runs")
        print('runs count:', cur.fetchone()[0])
    except Exception as e:
        print('runs query error:', e)
    try:
        cur.execute("SELECT * FROM alembic_version")
        print('alembic_version:', cur.fetchall())
    except Exception as e:
        print('alembic_version query error:', e)
    conn.close()

if __name__ == '__main__':
    main()
