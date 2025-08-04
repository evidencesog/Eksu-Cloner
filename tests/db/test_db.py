# tests/db/test_db.py
# tests/db/test_db.py

import sqlite3
import pytest
from app.db.database import init_db, save_credentials

@pytest.fixture(scope="function")

def memory_db():
    conn = sqlite3.connect(":memory:")
    init_db(conn)  # Initialize tables in-memory
    yield conn
    conn.close()

def test_save_and_fetch(memory_db):
    test_username = "admin"
    test_password = "secret"
    test_ip = "127.0.0.1"

    print("[TEST] Saving credentials using save_credentials...")
    save_credentials(test_username, test_password, test_ip, conn=memory_db)

    cursor = memory_db.cursor()
    cursor.execute("SELECT username, password, ip_address FROM credentials ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()

    print(f"[TEST] Fetched from DB: {result}")
    assert result == (test_username, test_password, test_ip)

def test_direct_insert(memory_db):
    cursor = memory_db.cursor()
    cursor.execute(
        "INSERT INTO credentials (username, password, timestamp, ip_address) VALUES (?, ?, datetime('now'), ?)",
        ("admin", "secret", "127.0.0.1")
    )
    memory_db.commit()

    cursor.execute("SELECT username, password, ip_address FROM credentials ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()

    print(f"[TEST] Fetched from direct insert: {result}")
    assert result == ("admin", "secret", "127.0.0.1")

