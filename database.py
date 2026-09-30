"""SQLite setup for the job application tracker."""

from __future__ import annotations

import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "database" / "jobs.db"


def get_connection(database_path: str | Path | None = None) -> sqlite3.Connection:
    """Return a connection, creating the containing database directory if needed."""
    path = Path(database_path) if database_path is not None else DATABASE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def create_table(database_path: str | Path | None = None) -> None:
    """Create the application table when it does not yet exist."""
    with get_connection(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS job_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                location TEXT,
                application_date TEXT NOT NULL,
                status TEXT NOT NULL,
                interview_date TEXT,
                salary REAL,
                notes TEXT
            )
            """
        )


if __name__ == "__main__":
    create_table()
    print(f"Database ready at {DATABASE_PATH}")
