from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from .config import get_settings

settings = get_settings()


def create_token(subject: str | int, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode: dict[str, Any] = {"sub": str(subject), "exp": expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_access_token(subject: str | int) -> str:
    return create_token(subject, timedelta(minutes=settings.access_token_expire_minutes))


def create_refresh_token(subject: str | int) -> str:
    return create_token(subject, timedelta(minutes=settings.refresh_token_expire_minutes))


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError as exc:  # pragma: no cover - FastAPI handles the error
        raise ValueError("Invalid token") from exc
