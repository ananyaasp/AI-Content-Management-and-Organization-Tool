from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_report_download():
    login = client.post("/api/auth/login", json={"username": "admin", "password": "adminpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.get("/api/reports/export/all", headers=headers)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
