import sqlite3
import time

DB = "events.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_event(level, message):
    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT INTO events (level, message, timestamp) VALUES (?, ?, ?)",
        (level, message, time.strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def get_logs(limit=50):
    conn = sqlite3.connect(DB)
    cursor = conn.execute(
        "SELECT level, message, timestamp FROM events ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = [{"level": r[0], "message": r[1], "timestamp": r[2]} for r in cursor.fetchall()]
    conn.close()
    return rows
