from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from ..core.security import create_access_token, create_refresh_token
from ..models.entities import User
from ..schemas.auth import LoginRequest, TokenPair
from ..utils.security import get_password_hash
from .deps import authenticate_user, get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenPair)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)) -> TokenPair:
    user = authenticate_user(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="ایمیل یا رمز عبور نادرست است")
    return TokenPair(access_token=create_access_token(user.id), refresh_token=create_refresh_token(user.id))


@router.post("/signup", response_model=TokenPair, status_code=status.HTTP_201_CREATED)
def signup(payload: LoginRequest, session: Session = Depends(get_db)) -> TokenPair:
    existing = session.exec(select(User).where(User.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="کاربر موجود است")
    user = User(email=payload.email, full_name=payload.email.split("@")[0], hashed_password=get_password_hash(payload.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return TokenPair(access_token=create_access_token(user.id), refresh_token=create_refresh_token(user.id))
