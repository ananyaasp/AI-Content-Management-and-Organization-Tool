# backend/tests/test_integration.py
import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# --- a) Upload → Search → Report flow ---
def test_full_upload_search_report_flow(tmp_path):
    # Step 1: Login
    login = client.post("/api/auth/login", json={"username": "admin", "password": "adminpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 2: Upload file
    file_data = io.BytesIO(b"Artificial Intelligence is the future of technology.")
    resp = client.post("/api/ingest/upload", files={"file": ("ai.txt", file_data, "text/plain")}, headers=headers)
    assert resp.status_code == 200
    file_id = resp.json()["id"]

    # Step 3: Search for something related
    search_resp = client.post("/api/search/query", json={"q": "technology future", "k": 5}, headers=headers)
    assert search_resp.status_code == 200
    results = search_resp.json()["results"]
    assert any(file_id in r["id"] for r in results)

    # Step 4: Export report
    report_resp = client.get("/api/reports/export/all", headers=headers)
    assert report_resp.status_code == 200
    assert report_resp.headers["content-type"] == "application/pdf"


# --- b) Auth Protection Across Routes ---
def test_auth_protection():
    # No token
    resp = client.get("/api/reports/export/all")
    assert resp.status_code == 401

    # Wrong token
    bad_headers = {"Authorization": "Bearer fake.token.value"}
    resp = client.get("/api/reports/export/all", headers=bad_headers)
    assert resp.status_code == 401


# --- c) Multiple File Uploads + Search Ranking ---
def test_multiple_files_and_search(tmp_path):
    login = client.post("/api/auth/login", json={"username": "admin", "password": "adminpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Upload two files
    file1 = io.BytesIO(b"Machine learning is part of AI.")
    file2 = io.BytesIO(b"The ocean is vast and blue.")
    client.post("/api/ingest/upload", files={"file": ("ml.txt", file1, "text/plain")}, headers=headers)
    client.post("/api/ingest/upload", files={"file": ("ocean.txt", file2, "text/plain")}, headers=headers)

    # Search for AI-related term
    search_resp = client.post("/api/search/query", json={"q": "artificial intelligence"}, headers=headers)
    results = search_resp.json()["results"]

    filenames = [r["filename"] for r in results]

    # ✅ Only check relevant file presence
    assert "ml.txt" in filenames, "Expected 'ml.txt' (AI-related) to appear in search results"


