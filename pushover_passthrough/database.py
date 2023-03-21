import sqlite3
from pathlib import Path


class Database:
    def __init__(self, path: Path):
        create = not path.exists()
        self.connection = sqlite3.connect(str(path))
        if create:
            with self.connection:
                self.connection.execute(
                    """
                    CREATE TABLE messages(hash TEXT PRIMARY KEY)
                    """
                )

    def exists(self, hash: str) -> bool:
        with self.connection:
            res = self.connection.execute(
                "SELECT hash FROM messages WHERE hash = ?", (hash,)
            )
            return res.fetchone() is not None

    def add(self, hash: str):
        with self.connection:
            self.connection.execute("INSERT INTO messages(hash) VALUES(?)", (hash,))
