from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from .common import IDModel, TimestampedModel


class Role(IDModel, SQLModel, table=True):
    name: str = Field(index=True, unique=True)
    description: str | None = None

    users: list["User"] = Relationship(back_populates="role")


class User(IDModel, TimestampedModel, table=True):
    email: str = Field(index=True, unique=True)
    full_name: str
    hashed_password: str
    is_active: bool = Field(default=True)
    role_id: int | None = Field(default=None, foreign_key="role.id")

    role: Optional[Role] = Relationship(back_populates="users")


class Customer(IDModel, TimestampedModel, table=True):
    first_name: str
    last_name: str
    phone: str | None = Field(default=None, index=True)


class Supplier(IDModel, TimestampedModel, table=True):
    name: str
    phone: str | None = None
    currency_code: str = Field(default="IRR")


class Category(IDModel, TimestampedModel, table=True):
    name: str = Field(index=True, unique=True)


class Warehouse(IDModel, TimestampedModel, table=True):
    name: str
    code: str = Field(index=True, unique=True)
    address: str | None = None


class Product(IDModel, TimestampedModel, table=True):
    sku: str = Field(index=True, unique=True)
    name: str
    brand: str | None = None
    color: str | None = None
    category_id: int | None = Field(default=None, foreign_key="category.id")
    barcode: str | None = Field(default=None, index=True)
    image_url: str | None = None

    category: Optional[Category] = Relationship()


class StockBalance(IDModel, TimestampedModel, table=True):
    product_id: int = Field(foreign_key="product.id")
    warehouse_id: int = Field(foreign_key="warehouse.id")
    quantity: float = 0
    average_cost: float = 0


class StockMove(IDModel, TimestampedModel, table=True):
    product_id: int = Field(foreign_key="product.id")
    warehouse_id: int = Field(foreign_key="warehouse.id")
    reference: str
    quantity: float
    unit_cost: float
    move_type: str = Field(description="IN, OUT, ADJUSTMENT")


class SalesOrder(IDModel, TimestampedModel, table=True):
    order_number: str = Field(unique=True, index=True)
    customer_id: int | None = Field(default=None, foreign_key="customer.id")
    warehouse_id: int = Field(foreign_key="warehouse.id")
    order_date: datetime = Field(default_factory=datetime.utcnow)
    channel: str = Field(default="POS")
    currency_code: str = Field(default="IRR")
    fx_rate: float = Field(default=1)
    discount_total: float = Field(default=0)
    shipping_cost: float = Field(default=0)
    notes: str | None = None

    lines: list["SalesOrderLine"] = Relationship(back_populates="order")
    payments: list["Payment"] = Relationship(back_populates="order")


class SalesOrderLine(IDModel, TimestampedModel, table=True):
    order_id: int = Field(foreign_key="salesorder.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: float
    unit_price: float
    discount_line: float = 0

    order: SalesOrder = Relationship(back_populates="lines")


class Payment(IDModel, TimestampedModel, table=True):
    order_id: int = Field(default=None, foreign_key="salesorder.id")
    method: str
    amount: float
    currency_code: str = Field(default="IRR")

    order: Optional[SalesOrder] = Relationship(back_populates="payments")


class Purchase(IDModel, TimestampedModel, table=True):
    supplier_id: int = Field(foreign_key="supplier.id")
    warehouse_id: int = Field(foreign_key="warehouse.id")
    reference: str = Field(unique=True, index=True)
    purchase_date: datetime = Field(default_factory=datetime.utcnow)
    currency_code: str = Field(default="IRR")
    fx_rate: float = Field(default=1)
    freight_cost: float = 0
    customs_cost: float = 0
    insurance_cost: float = 0
    other_cost: float = 0

    lines: list["PurchaseLine"] = Relationship(back_populates="purchase")


class PurchaseLine(IDModel, TimestampedModel, table=True):
    purchase_id: int = Field(foreign_key="purchase.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: float
    unit_cost: float
    discount_line: float = 0

    purchase: Purchase = Relationship(back_populates="lines")


class AccountingEntry(IDModel, TimestampedModel, table=True):
    entry_date: date = Field(default_factory=date.today)
    description: str

    lines: list["AccountingLine"] = Relationship(back_populates="entry")


class AccountingLine(IDModel, SQLModel, table=True):
    entry_id: int = Field(foreign_key="accountingentry.id")
    account_code: str
    debit: float = 0
    credit: float = 0

    entry: AccountingEntry = Relationship(back_populates="lines")


class ExchangeRate(IDModel, TimestampedModel, table=True):
    currency_code: str = Field(index=True)
    rate_date: date = Field(default_factory=date.today, index=True)
    rate: float
