"""Main entry point for the FastAPI backend application.

Initializes the FastAPI app, includes API routers, and starts
the background file watcher thread on startup.
"""
from fastapi import FastAPI
from app.api.ingest import router as ingest_router
from app.api.search import router as search_router
from app.api.auth import router as auth_router
from app.api.reports import router as reports_router
from app.ingestors.watcher import start_watcher
import threading

app = FastAPI(title="AI Content Organizer")

app.include_router(auth_router)
app.include_router(ingest_router)
app.include_router(search_router)
app.include_router(reports_router)

@app.on_event("startup")
def on_startup():
    """Start the background watcher thread when the app launches."""
    t = threading.Thread(target=start_watcher, daemon=True)
    t.start()
