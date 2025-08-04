# tests/test_routes.py

from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv
from app.db import database
load_dotenv(dotenv_path="secret_key.env")
client = TestClient(app)



def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "EKITI STATE UNIVERSITY" in response.text  # Adjust to match actual page

def test_static_file_serving():
    response = client.get("/static/css/new_login.css")  # Use a known static file path
    assert response.status_code == 200


def test_get_all_credentials():
    creds = database.fetch_all_credentials()
    assert isinstance(creds, list)


def test_login_submission():
    response = client.post("/login", data={
        "username": "test_user",
        "password": "test_pass"
    })
    # Accept 302 redirection status
    assert response.status_code in (200, 302)
