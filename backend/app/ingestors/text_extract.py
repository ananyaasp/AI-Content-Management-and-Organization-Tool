import os
from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document

def extract_text_from_file(path: str) -> str:
    _, ext = os.path.splitext(path.lower())
    if ext == ".txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    if ext == ".pdf":
        try:
            return pdf_extract_text(path) or ""
        except Exception:
            return ""
    if ext in (".docx",):
        try:
            doc = Document(path)
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception:
            return ""
    # fallback
    return ""
