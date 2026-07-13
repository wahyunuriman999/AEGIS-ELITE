#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

def main():
    try:
        from api import migrations
        migrations.ensure_base()
        print("Migrations applied: base schema ensured.")
        # show applied migrations
        applied = migrations.applied_migrations()
        print("Applied migrations:", applied)
    except Exception as e:
        print("Migration runner error:", e)

if __name__ == '__main__':
    main()
