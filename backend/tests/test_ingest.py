import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_file():
    # login first to get token
    login = client.post("/api/auth/login", json={"username": "admin", "password": "adminpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    file_data = io.BytesIO(b"Sample text for testing")
    resp = client.post("/api/ingest/upload", files={"file": ("sample.txt", file_data, "text/plain")}, headers=headers)
    
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
