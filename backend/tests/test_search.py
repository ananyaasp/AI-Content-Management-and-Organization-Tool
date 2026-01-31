from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_functionality():
    login = client.post("/api/auth/login", json={"username": "admin", "password": "adminpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post("/api/search/query", json={"q": "test", "k": 5}, headers=headers)
    assert resp.status_code == 200
    assert "results" in resp.json()
