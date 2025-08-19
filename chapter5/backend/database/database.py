"""Database setup and functions for the TTRPG GM Assistant."""
import json
import os
import sqlite3
from contextlib import closing
from typing import List, Dict, Any

DB_FILE = "messages.db"


def create_db_and_tables():
    """
    Creates the SQLite database and the messages table.
    Deletes the old database file first to ensure a fresh start.
    """
    # Delete the old database file if it exists to ensure a fresh schema
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    with closing(sqlite3.connect(DB_FILE)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    thread_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    parts TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            conn.commit()


def add_message_to_db(thread_id: str, message: Dict[str, Any]):
    """Adds a message (as a dict) to the database."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        with closing(conn.cursor()) as cursor:
            # The 'parts' of a message are stored as a JSON string
            parts_json = json.dumps(message.get("parts", ""))
            cursor.execute(
                "INSERT INTO messages (thread_id, role, parts) VALUES (?, ?, ?)",
                (thread_id, message.get("role"), parts_json),
            )
            conn.commit()


def get_messages_from_db(thread_id: str) -> List[Dict[str, Any]]:
    """Retrieves all messages for a given thread_id from the database."""
    messages = []
    with closing(sqlite3.connect(DB_FILE)) as conn:
        conn.row_factory = sqlite3.Row
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                "SELECT role, parts FROM messages WHERE thread_id = ? ORDER BY timestamp ASC",
                (thread_id,),
            )
            rows = cursor.fetchall()
            for row in rows:
                messages.append({"role": row["role"], "parts": json.loads(row["parts"])})
    return messages
