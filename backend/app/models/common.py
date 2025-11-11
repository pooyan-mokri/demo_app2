from __future__ import annotations

from datetime import datetime

from sqlmodel import Field, SQLModel


class TimestampedModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class IDModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
