"""DB migration helper — boardgame-v1.

Usage:
    python3 db/migrate.py [--db-path PATH]

Creates the SQLite database from schema.sql.
Default path: db/boardgame.db
"""

import sqlite3
import argparse
import pathlib


SCHEMA = pathlib.Path(__file__).parent / "schema.sql"
DEFAULT_DB = pathlib.Path(__file__).parent / "boardgame.db"


def migrate(db_path: pathlib.Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    sql = SCHEMA.read_text()
    with sqlite3.connect(db_path) as conn:
        conn.executescript(sql)
    print(f"[migrate] OK — {db_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-path", type=pathlib.Path, default=DEFAULT_DB)
    args = parser.parse_args()
    migrate(args.db_path)
