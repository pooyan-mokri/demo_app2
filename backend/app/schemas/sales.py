from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PaymentCreate(BaseModel):
    method: str
    amount: float
    currency_code: str = "IRR"


class SalesOrderLineCreate(BaseModel):
    product_id: int
    quantity: float
    unit_price: float
    discount_line: float = 0


class SalesOrderCreate(BaseModel):
    order_number: str
    customer_id: Optional[int] = None
    warehouse_id: int
    order_date: Optional[datetime] = None
    channel: str = "POS"
    currency_code: str = "IRR"
    fx_rate: float = 1
    discount_total: float = 0
    shipping_cost: float = 0
    notes: Optional[str] = None
    lines: list[SalesOrderLineCreate]
    payments: list[PaymentCreate]


class SalesOrderRead(BaseModel):
    id: int
    order_number: str
    total_amount: float
    currency_code: str
    order_date: datetime
