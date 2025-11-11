from __future__ import annotations

from sqlmodel import Session, select

from ..models.entities import Product, StockBalance, StockMove


def adjust_stock(
    *,
    session: Session,
    product_id: int,
    warehouse_id: int,
    quantity: float,
    unit_cost: float,
    reference: str,
    move_type: str,
) -> None:
    balance = session.exec(
        select(StockBalance).where(
            StockBalance.product_id == product_id,
            StockBalance.warehouse_id == warehouse_id,
        )
    ).one_or_none()

    if balance is None:
        balance = StockBalance(product_id=product_id, warehouse_id=warehouse_id, quantity=0, average_cost=unit_cost)
        session.add(balance)

    if move_type == "IN":
        total_cost = balance.average_cost * balance.quantity + unit_cost * quantity
        balance.quantity += quantity
        balance.average_cost = total_cost / balance.quantity if balance.quantity else unit_cost
    else:
        balance.quantity -= quantity

    move = StockMove(
        product_id=product_id,
        warehouse_id=warehouse_id,
        reference=reference,
        quantity=quantity,
        unit_cost=unit_cost,
        move_type=move_type,
    )
    session.add(move)

    product = session.get(Product, product_id)
    if product is None:
        raise ValueError("Product not found")

    session.add(balance)
