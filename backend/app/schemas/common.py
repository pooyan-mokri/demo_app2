from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class DateRange(BaseModel):
    start: date = Field(default_factory=date.today)
    end: date = Field(default_factory=date.today)


class JalaliDateTime(BaseModel):
    value: datetime
