"""Semantic search API endpoints.

Supports vector-based text search using FAISS and SentenceTransformer embeddings.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.core.embeddings import get_model, get_index
from app.db.store import load_all
from app.api.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/api/search", tags=["search"])

class Query(BaseModel):
    q: str
    k: int = 5

@router.post("/query")
def query(q: Query, user=Depends(get_current_user)):
    """Request schema for search queries containing text and result count."""
    model = get_model()
    vec = model.encode(q.q)
    idx = get_index()
    results = idx.search(vec, k=q.k)
    files = load_all()["files"]
    id_map = {f["id"]: f for f in files}
    out = []
    for id_str, dist in results:
        meta = id_map.get(id_str)
        if meta:
            out.append({"id": id_str, "filename": meta["filename"],
                        "snippet": meta.get("content_snippet"), "score": dist})
    return {"results": out}

@router.get("/preview/{file_id}")
def preview(file_id: str, user=Depends(get_current_user)):
    """Return semantically similar files for the provided search query."""
    files = load_all()["files"]
    for f in files:
        if f["id"] == file_id:
            return {"id": f["id"], "filename": f["filename"],
                    "snippet": f.get("content_snippet")}
    raise HTTPException(status_code=404, detail="file not found")
