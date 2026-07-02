import sqlite3
from pathlib import Path


# Run from backend for this relative path to work
DB_PATH: Path = Path("ghostline.db")


def get_conn() -> sqlite3.Connection:
    # If the file doesn't exist, sqlite creates it
    conn = sqlite3.connect(DB_PATH)
    # This makes sqlite treat rows as dictionaries instead of tuples.
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_conn()

    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rooms (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            )
            """
        )

        conn.commit() # Persists the schema change
    finally:
        conn.close()


def insert_room(room_id: str, created_at: str) -> None:
    conn = get_conn()

    try:
        conn.execute(
            """
            INSERT INTO rooms (id, created_at)
            VALUES (?, ?)
            """,
            (room_id, created_at),
        )

        conn.commit()
    finally:
        conn.close()
