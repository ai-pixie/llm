from __future__ import annotations

from pathlib import Path
import sqlite3


class Database:
    def __init__(self, path: str = ":memory:") -> None:
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row

    def migrate(self) -> None:
        migrations_dir = Path(__file__).resolve().parent.parent / "migrations"
        for migration in sorted(migrations_dir.glob("*.sql")):
            self.connection.executescript(migration.read_text())
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()
