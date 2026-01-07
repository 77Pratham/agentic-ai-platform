import sqlite3
import json
from datetime import datetime

DB_PATH = "execution.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS executions (
            id TEXT PRIMARY KEY,
            plan TEXT,
            current_step INTEGER,
            status TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_execution(exec_id, plan, current_step, status):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO executions
        VALUES (?, ?, ?, ?, ?)
    """, (
        exec_id,
        json.dumps(plan),
        current_step,
        status,
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()

def load_execution(exec_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT plan, current_step, status FROM executions WHERE id=?", (exec_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "plan": json.loads(row[0]),
        "current_step": row[1],
        "status": row[2]
    }
