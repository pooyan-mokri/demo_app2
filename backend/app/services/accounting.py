from __future__ import annotations

from datetime import date

from sqlmodel import Session, select

from ..models.entities import AccountingEntry, AccountingLine


def create_journal_entry(*, session: Session, description: str, lines: list[AccountingLine], entry_date: date | None = None) -> AccountingEntry:
    entry = AccountingEntry(entry_date=entry_date or date.today(), description=description)
    session.add(entry)
    session.flush()
    for line in lines:
        line.entry_id = entry.id  # type: ignore[assignment]
        session.add(line)
    return entry


def profit_and_loss(*, session: Session, start: date, end: date) -> dict[str, float]:
    rows = session.exec(
        select(AccountingLine.account_code, AccountingLine.debit, AccountingLine.credit)
        .join(AccountingEntry)
        .where(AccountingEntry.entry_date.between(start, end))
    ).all()

    totals: dict[str, float] = {}
    for account_code, debit, credit in rows:
        totals.setdefault(account_code, 0)
        totals[account_code] += debit - credit
    return totals
