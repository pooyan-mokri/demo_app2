from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..schemas.accounting import ProfitLossReport, ProfitLossRow
from ..services.accounting import profit_and_loss
from .deps import get_current_user, get_db

router = APIRouter(prefix="/reports", tags=["reports"], dependencies=[Depends(get_current_user)])


@router.get("/profit-loss", response_model=ProfitLossReport)
def get_profit_loss(start: date, end: date, session: Session = Depends(get_db)) -> ProfitLossReport:
    totals = profit_and_loss(session=session, start=start, end=end)
    rows = [ProfitLossRow(account=code, amount=amount) for code, amount in totals.items()]
    net_income = sum(row.amount for row in rows)
    return ProfitLossReport(start=start, end=end, rows=rows, net_income=net_income)
