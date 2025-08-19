"""Database setup and functions for the TTRPG GM Assistant."""
import sqlite3
from contextlib import closing
from typing import List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

DB_FILE = "messages.db"

def create_db_and_tables():
    """Creates the SQLite database and the messages table."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    thread_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

def add_message_to_db(thread_id: str, message: BaseMessage):
    """Adds a message to the database."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO messages (thread_id, role, content) VALUES (?, ?, ?)",
                (thread_id, message.type, message.content),
            )
            conn.commit()

def get_messages_from_db(thread_id: str) -> List[BaseMessage]:
    """Retrieves all messages for a given thread_id from the database."""
    messages = []
    with closing(sqlite3.connect(DB_FILE)) as conn:
        conn.row_factory = sqlite3.Row
        with closing(conn.cursor()) as cursor:
            cursor.execute("SELECT role, content FROM messages WHERE thread_id = ? ORDER BY timestamp ASC", (thread_id,))
            rows = cursor.fetchall()
            for row in rows:
                if row["role"] == "human":
                    messages.append(HumanMessage(content=row["content"]))
                elif row["role"] == "ai":
                    messages.append(AIMessage(content=row["content"]))
    return messages
