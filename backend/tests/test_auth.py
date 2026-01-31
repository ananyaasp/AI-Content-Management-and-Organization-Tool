from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    resp = client.post("/api/auth/login", json={"username": "admin", "password": "adminpass"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()

def test_login_failure():
    resp = client.post("/api/auth/login", json={"username": "wrong", "password": "bad"})
    assert resp.status_code == 401
