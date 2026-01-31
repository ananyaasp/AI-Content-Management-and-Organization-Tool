# backend/tests/test_text_extract.py
import os
from app.ingestors.text_extract import extract_text_from_file

def test_extract_text_from_txt(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text("Hello World")
    result = extract_text_from_file(str(file))
    assert "Hello World" in result

def test_extract_text_from_unsupported(tmp_path):
    file = tmp_path / "image.jpg"
    file.write_bytes(b"\x00\x01")
    result = extract_text_from_file(str(file))
    assert result == ""
