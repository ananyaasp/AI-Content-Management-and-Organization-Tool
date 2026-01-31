from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import settings

ALGORITHM = "HS256"

def create_access_token(data: dict, expires_minutes: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes or settings.jwt_exp_minutes)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)
    return encoded

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
