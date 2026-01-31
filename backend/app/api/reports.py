"""Report generation endpoints.

Creates and returns downloadable PDF reports containing ingested file metadata.
"""

from fastapi import APIRouter, Depends
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from fastapi.responses import StreamingResponse
from app.db.store import load_all
from app.api.auth import get_current_user

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/export/all")
def export_all(user=Depends(get_current_user)):
    """Generate and return a consolidated PDF report of all stored files."""
    data = load_all()["files"]
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    y = 750
    c.setFont("Helvetica", 12)
    c.drawString(30, y+20, "Files Report")
    for f in data:
        c.drawString(30, y, f"ID: {f['id']} | Name: {f['filename']}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 750
    c.save()
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=report.pdf"})
