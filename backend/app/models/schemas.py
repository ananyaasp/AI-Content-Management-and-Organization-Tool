from pydantic import BaseModel
from typing import Optional, List

# ==============================
# User Authentication Models
# ==============================
class User(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ==============================
# File Upload & Ingestion Models
# ==============================
class FileMetadata(BaseModel):
    filename: str
    content_type: Optional[str] = None
    size: Optional[int] = None


class IngestRequest(BaseModel):
    files: List[FileMetadata]
    user_id: Optional[str] = None


# ==============================
# General Response Model
# ==============================
class MessageResponse(BaseModel):
    message: str
