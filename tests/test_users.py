import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200

def test_register_user():
    response = client.post(
        "/users/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser2026@example.com"
        }
    )
    assert response.status_code == 200
