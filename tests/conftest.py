
import pytest
import os
import sqlite3
from fastapi.testclient import TestClient
from app.main import app
import app.db.database as db_module
from dotenv import load_dotenv
load_dotenv(dotenv_path="secret_key.env")

TEST_DB_PATH = "test_creds.db"

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Override the DB_PATH used in the database module
    db_module.DB_PATH = TEST_DB_PATH

    # Ensure the directory for the test DB exists
    os.makedirs(os.path.dirname(TEST_DB_PATH) or ".", exist_ok=True)

    # Initialize the test DB schema
    db_module.init_db()
    yield
    # Clean up after the test session
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

@pytest.fixture(autouse=True)
def clear_db_before_test():
    # Clear credentials table before each test
    conn = sqlite3.connect(TEST_DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM credentials")
    conn.commit()
    conn.close()

@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client
