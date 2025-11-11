from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class JournalLine(BaseModel):
    account_code: str
    debit: float = 0
    credit: float = 0


class JournalEntryCreate(BaseModel):
    entry_date: date
    description: str
    lines: list[JournalLine]


class ProfitLossRow(BaseModel):
    account: str
    amount: float


class ProfitLossReport(BaseModel):
    start: date
    end: date
    rows: list[ProfitLossRow]
    net_income: float
