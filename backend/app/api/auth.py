"""Authentication API routes.

Provides endpoints for user login and JWT token generation.
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from app.core.security import create_access_token, decode_token
from app.models.schemas import User
from passlib.hash import bcrypt
from datetime import timedelta

router = APIRouter(prefix="/api/auth", tags=["auth"])

USERS = {
    "admin": {"password": bcrypt.hash("adminpass"), "roles": ["admin"]}
}

@router.post("/login")
def login(payload: User):
    """Authenticate a user and return an access token."""
    u = USERS.get(payload.username)
    if not u or not bcrypt.verify(payload.password, u["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": payload.username})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(authorization: str = Header(None)):
    """Validate the provided JWT access token."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing auth header")
    token = authorization.split("Bearer ")[-1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload.get("sub")
