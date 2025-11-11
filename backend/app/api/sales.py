from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..models.entities import AccountingLine, Payment, Product, SalesOrder, SalesOrderLine
from ..schemas.sales import SalesOrderCreate, SalesOrderRead
from ..services.accounting import create_journal_entry
from ..services.inventory import adjust_stock
from .deps import get_current_user, get_db

router = APIRouter(prefix="/sales", tags=["sales"], dependencies=[Depends(get_current_user)])


def _generate_order_total(session: Session, order: SalesOrder) -> float:
    lines = session.exec(select(SalesOrderLine).where(SalesOrderLine.order_id == order.id)).all()
    line_total = sum((line.quantity * line.unit_price) - line.discount_line for line in lines)
    return line_total - order.discount_total + order.shipping_cost


@router.post("", response_model=SalesOrderRead, status_code=status.HTTP_201_CREATED)
def create_sales_order(payload: SalesOrderCreate, session: Session = Depends(get_db)) -> SalesOrderRead:
    existing = session.exec(select(SalesOrder).where(SalesOrder.order_number == payload.order_number)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="شماره فاکتور تکراری است")

    order = SalesOrder(
        order_number=payload.order_number,
        customer_id=payload.customer_id,
        warehouse_id=payload.warehouse_id,
        order_date=payload.order_date or datetime.utcnow(),
        channel=payload.channel,
        currency_code=payload.currency_code,
        fx_rate=payload.fx_rate,
        discount_total=payload.discount_total,
        shipping_cost=payload.shipping_cost,
        notes=payload.notes,
    )
    session.add(order)
    session.flush()

    for line_payload in payload.lines:
        product = session.get(Product, line_payload.product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="محصول یافت نشد")
        line = SalesOrderLine(
            order_id=order.id,
            product_id=line_payload.product_id,
            quantity=line_payload.quantity,
            unit_price=line_payload.unit_price,
            discount_line=line_payload.discount_line,
        )
        session.add(line)
        adjust_stock(
            session=session,
            product_id=line_payload.product_id,
            warehouse_id=payload.warehouse_id,
            quantity=line_payload.quantity,
            unit_cost=line_payload.unit_price,
            reference=order.order_number,
            move_type="OUT",
        )

    for payment_payload in payload.payments:
        payment = Payment(
            order_id=order.id,
            method=payment_payload.method,
            amount=payment_payload.amount,
            currency_code=payment_payload.currency_code,
        )
        session.add(payment)

    session.commit()
    session.refresh(order)

    total = _generate_order_total(session, order)
    total_payments = sum(payment.amount for payment in payload.payments)
    lines = [
        AccountingLine(account_code="4000", credit=total),
        AccountingLine(account_code="1100", debit=total_payments),
    ]
    create_journal_entry(session=session, description=f"فروش {order.order_number}", lines=lines, entry_date=order.order_date.date())
    session.commit()

    return SalesOrderRead(
        id=order.id,
        order_number=order.order_number,
        total_amount=total,
        currency_code=order.currency_code,
        order_date=order.order_date,
    )


@router.get("", response_model=list[SalesOrderRead])
def list_orders(session: Session = Depends(get_db)) -> list[SalesOrderRead]:
    orders = session.exec(select(SalesOrder)).all()
    result: list[SalesOrderRead] = []
    for order in orders:
        total = _generate_order_total(session, order)
        result.append(
            SalesOrderRead(
                id=order.id,
                order_number=order.order_number,
                total_amount=total,
                currency_code=order.currency_code,
                order_date=order.order_date,
            )
        )
    return result
