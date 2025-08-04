# tests/test_routes.py

from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv
load_dotenv(dotenv_path="secret_key.env")
client = TestClient(app)




def test_admin_login_page():
    # First, POST to login route
    response = client.post("/admin/login", data={"password": "letmein"})
    assert response.status_code in (302, 200)

    # Then, GET the dashboard with session already set
    response = client.get("/admin/login")
    assert response.status_code == 200

# tests/routes/test_admin.py
def test_admin_login_valid(client):
    response = client.post("/admin/login", data={"username": "admin", "password": "admin"})
    assert response.status_code in (200, 302)

def test_admin_dashboard_redirect():
    response = client.get("/admin/dashboard")
    assert response.status_code in (200, 302, 403)
