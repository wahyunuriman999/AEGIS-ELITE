from pathlib import Path
from shutil import copy2
from datetime import datetime


def backup_db(dst_dir: Path = Path('backups')):
    src = Path(__file__).resolve().parent.parent / 'api' / 'state.db'
    dst_dir.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        print('No database to backup')
        return None
    name = f'state-{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}.db'
    dst = dst_dir / name
    copy2(src, dst)
    print('Backup created at', dst)
    return dst


if __name__ == '__main__':
    backup_db()
