from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str


class CategoryRead(CategoryCreate):
    id: int


class WarehouseCreate(BaseModel):
    name: str
    code: str
    address: Optional[str] = None


class WarehouseRead(WarehouseCreate):
    id: int


class ProductBase(BaseModel):
    sku: str
    name: str
    brand: Optional[str] = None
    color: Optional[str] = None
    category_id: Optional[int] = None
    barcode: Optional[str] = None
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    color: Optional[str] = None
    category_id: Optional[int] = None
    barcode: Optional[str] = None
    image_url: Optional[str] = None


class ProductRead(ProductBase):
    id: int
    category: Optional[CategoryRead] = None
