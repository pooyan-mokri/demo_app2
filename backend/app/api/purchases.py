from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..models.entities import AccountingLine, Product, Purchase, PurchaseLine
from ..schemas.purchases import PurchaseCreate
from ..services.accounting import create_journal_entry
from ..services.inventory import adjust_stock
from .deps import get_current_user, get_db

router = APIRouter(prefix="/purchases", tags=["purchases"], dependencies=[Depends(get_current_user)])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_purchase(payload: PurchaseCreate, session: Session = Depends(get_db)) -> dict[str, str]:
    existing = session.exec(select(Purchase).where(Purchase.reference == payload.reference)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="شماره خرید تکراری است")

    purchase = Purchase(
        supplier_id=payload.supplier_id,
        warehouse_id=payload.warehouse_id,
        reference=payload.reference,
        purchase_date=payload.purchase_date or datetime.utcnow(),
        currency_code=payload.currency_code,
        fx_rate=payload.fx_rate,
        freight_cost=payload.freight_cost,
        customs_cost=payload.customs_cost,
        insurance_cost=payload.insurance_cost,
        other_cost=payload.other_cost,
    )
    session.add(purchase)
    session.flush()

    total_quantity = sum(line.quantity for line in payload.lines)
    extra_costs = payload.freight_cost + payload.customs_cost + payload.insurance_cost + payload.other_cost
    extra_per_unit = extra_costs / total_quantity if total_quantity else 0

    total_amount = 0.0
    for line_payload in payload.lines:
        product = session.get(Product, line_payload.product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="محصول یافت نشد")
        effective_cost = line_payload.unit_cost + extra_per_unit
        purchase_line = PurchaseLine(
            purchase_id=purchase.id,
            product_id=line_payload.product_id,
            quantity=line_payload.quantity,
            unit_cost=effective_cost,
            discount_line=line_payload.discount_line,
        )
        session.add(purchase_line)
        adjust_stock(
            session=session,
            product_id=line_payload.product_id,
            warehouse_id=payload.warehouse_id,
            quantity=line_payload.quantity,
            unit_cost=effective_cost,
            reference=purchase.reference,
            move_type="IN",
        )
        total_amount += effective_cost * line_payload.quantity

    session.commit()
    session.refresh(purchase)

    lines = [
        AccountingLine(account_code="5000", debit=total_amount),
        AccountingLine(account_code="2100", credit=total_amount),
    ]
    create_journal_entry(session=session, description=f"خرید {purchase.reference}", lines=lines, entry_date=purchase.purchase_date.date())
    session.commit()

    return {"message": "خرید ثبت شد"}
