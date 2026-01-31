import streamlit as st
import requests
import io

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Content Organizer", layout="wide")

# --- Helper: Login ---
def login(username, password):
    resp = requests.post(f"{BACKEND_URL}/api/auth/login", json={"username": username, "password": password})
    if resp.status_code == 200:
        return resp.json()["access_token"]
    else:
        st.error("Login failed. Check credentials.")
        return None

# --- Helper: Auth header ---
def auth_header(token):
    return {"Authorization": f"Bearer {token}"}

# --- Sidebar Login ---
st.sidebar.header("🔐 Login")
username = st.sidebar.text_input("Username", "admin")
password = st.sidebar.text_input("Password", "adminpass", type="password")

if st.sidebar.button("Login"):
    token = login(username, password)
    if token:
        st.session_state["token"] = token
        st.success("✅ Logged in successfully!")

token = st.session_state.get("token")

if not token:
    st.warning("Please log in to access the app.")
    st.stop()

# --- Tabs ---
tabs = st.tabs(["📤 Upload & Ingest", "🔍 Search", "📄 Reports"])

# --- Upload & Ingest Tab ---
with tabs[0]:
    st.header("📤 Upload a Document")
    uploaded_file = st.file_uploader("Choose a file (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])

    if uploaded_file is not None:
        if st.button("Upload File"):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            resp = requests.post(f"{BACKEND_URL}/api/ingest/upload", files=files, headers=auth_header(token))
            if resp.status_code == 200:
                st.success(f"✅ File '{uploaded_file.name}' uploaded and ingested successfully!")
            else:
                st.error("Upload failed.")

# --- Search Tab ---
with tabs[1]:
    st.header("🔍 Search for Content")
    query = st.text_input("Enter a search query")

    if st.button("Search"):
        if query.strip():
            resp = requests.post(f"{BACKEND_URL}/api/search/query",
                                 json={"q": query, "k": 5},
                                 headers=auth_header(token))
            if resp.status_code == 200:
                results = resp.json()["results"]
                if not results:
                    st.info("No results found.")
                for res in results:
                    with st.expander(f"📄 {res['filename']} (Score: {res['score']:.2f})"):
                        st.write(res["snippet"])
            else:
                st.error("Error performing search.")
        else:
            st.warning("Enter a query first!")

# --- Reports Tab ---
with tabs[2]:
    st.header("📄 Download All Reports")
    if st.button("Generate Report"):
        resp = requests.get(f"{BACKEND_URL}/api/reports/export/all", headers=auth_header(token))
        if resp.status_code == 200:
            st.download_button("⬇️ Download Report (PDF)",
                               data=resp.content,
                               file_name="report.pdf",
                               mime="application/pdf")
        else:
            st.error("Failed to generate report.")
