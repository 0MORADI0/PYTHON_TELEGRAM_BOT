import sqlite3
from datetime import datetime, timezone


def connect_db():
    return sqlite3.connect("tasks.db")

def create_tables():
    with connect_db() as conn:
        conn.execute("""
CREATE TABLE IF NOT EXISTS tasks (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
title TEXT NOT NULL,
due_date TEXT,
priority TEXT DEFAULT 'medium',
is_done INTEGER DEFAULT 0,
created_at TEXT NOT NULL
)
""")

def add_task(user_id, title):
    with connect_db() as conn:
        cursor = conn.execute(
"""
INSERT INTO tasks (
user_id,
title,
created_at
)
VALUES (?, ?, ?)
""",
(
user_id,
title,
datetime.now(timezone.utc).isoformat()
)
)
        return cursor.lastrowid
def get_tasks(user_id):
    with connect_db() as conn:
        cursor = conn.execute(
"""
SELECT id, title, is_done
FROM tasks
WHERE user_id = ?
ORDER BY id DESC
""",
(user_id,)
)
        return cursor.fetchall()
def complete_task(user_id, task_id):
    with connect_db() as conn:
        cursor = conn.execute(
"""
UPDATE tasks
SET is_done = 1
WHERE id = ? AND user_id = ?
""",
(task_id, user_id)
)
        return cursor.rowcount > 0
def delete_task(user_id, task_id):
    with connect_db() as conn:
        cursor = conn.execute(
            """
            DELETE FROM tasks
            WHERE id = ? AND user_id = ?
            """,
            (task_id, user_id)
        )

        return cursor.rowcount > 0
if __name__ == "__main__":
    create_tables()
    print("Database created successfully!")