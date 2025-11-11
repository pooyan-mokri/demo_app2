from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class PurchaseLineCreate(BaseModel):
    product_id: int
    quantity: float
    unit_cost: float
    discount_line: float = 0


class PurchaseCreate(BaseModel):
    supplier_id: int
    warehouse_id: int
    reference: str
    purchase_date: datetime | None = None
    currency_code: str = "IRR"
    fx_rate: float = 1
    freight_cost: float = 0
    customs_cost: float = 0
    insurance_cost: float = 0
    other_cost: float = 0
    lines: list[PurchaseLineCreate]
