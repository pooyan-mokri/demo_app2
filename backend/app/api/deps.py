from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from ..core.db import get_session
from ..core.security import decode_token
from ..models.entities import User
from ..utils.security import verify_password

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db() -> Session:
    yield from get_session()


def get_current_user(token: str = Depends(reuseable_oauth), session: Session = Depends(get_db)) -> User:
    try:
        payload = decode_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token نامعتبر است") from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="دسترسی غیرمجاز")

    user = session.get(User, int(user_id))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="کاربر یافت نشد")
    return user


def authenticate_user(*, session: Session, email: str, password: str) -> User | None:
    statement = select(User).where(User.email == email)
    user = session.exec(statement).one_or_none()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
