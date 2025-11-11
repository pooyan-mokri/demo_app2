from __future__ import annotations

from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from .config import get_settings

settings = get_settings()
DATABASE_URL = settings.database_url

if not DATABASE_URL:
    msg = "THEMOAK_DATABASE_URL environment variable must be set before using the database engine."
    raise RuntimeError(msg)

engine = create_engine(DATABASE_URL, echo=settings.debug, pool_pre_ping=True)


def init_db() -> None:
    """Create database tables."""

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
