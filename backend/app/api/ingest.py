"""File ingestion and text extraction endpoints.

Handles file uploads, saves them, extracts text content,
and stores embeddings for later search.
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import os, uuid
from app.core.config import settings
from app.ingestors.text_extract import extract_text_from_file
from app.db.store import add_file
from app.core.embeddings import embed_and_store
from app.api.auth import get_current_user

router = APIRouter(prefix="/api/ingest", tags=["ingest"])

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), user=Depends(get_current_user)):
    """Receive a file upload, extract its text, and store its embedding."""
    os.makedirs(settings.storage_dir, exist_ok=True)
    uid = str(uuid.uuid4())
    filename = f"{uid}_{file.filename}"
    dest = os.path.join(settings.storage_dir, filename)
    with open(dest, "wb") as f:
        content = await file.read()
        f.write(content)
    text = extract_text_from_file(dest)
    snippet = (text[:500] + "...") if len(text) > 500 else text
    meta = {"id": uid, "filename": file.filename, "path": dest, "content_snippet": snippet}
    add_file(meta)
    embed_and_store(uid, text)
    return {"status": "ok", "id": uid}
