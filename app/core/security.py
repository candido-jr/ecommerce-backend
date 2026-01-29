from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(*, subject: str, secret: str, expires_minutes: int) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def create_refresh_token(*, subject: str, secret: str, expires_days: int) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=expires_days)).timestamp()),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_token(token: str, *, secret: str) -> dict[str, Any]:
    return jwt.decode(token, secret, algorithms=["HS256"])
