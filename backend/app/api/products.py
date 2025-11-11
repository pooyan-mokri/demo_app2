from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..models.entities import Category, Product, Warehouse
from ..schemas.products import (
    CategoryCreate,
    CategoryRead,
    ProductCreate,
    ProductRead,
    ProductUpdate,
    WarehouseCreate,
    WarehouseRead,
)
from .deps import get_current_user, get_db

router = APIRouter(prefix="/products", tags=["products"], dependencies=[Depends(get_current_user)])


@router.post("/categories", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, session: Session = Depends(get_db)) -> Category:
    existing = session.exec(select(Category).where(Category.name == payload.name)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="دسته بندی تکراری است")
    category = Category(**payload.model_dump())
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.get("/categories", response_model=list[CategoryRead])
def list_categories(session: Session = Depends(get_db)) -> list[Category]:
    return session.exec(select(Category)).all()


@router.post("/warehouses", response_model=WarehouseRead, status_code=status.HTTP_201_CREATED)
def create_warehouse(payload: WarehouseCreate, session: Session = Depends(get_db)) -> Warehouse:
    warehouse = Warehouse(**payload.model_dump())
    session.add(warehouse)
    session.commit()
    session.refresh(warehouse)
    return warehouse


@router.get("/warehouses", response_model=list[WarehouseRead])
def list_warehouses(session: Session = Depends(get_db)) -> list[Warehouse]:
    return session.exec(select(Warehouse)).all()


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, session: Session = Depends(get_db)) -> Product:
    existing = session.exec(select(Product).where(Product.sku == payload.sku)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="SKU تکراری است")
    product = Product(**payload.model_dump())
    session.add(product)
    session.commit()
    session.refresh(product)
    if product.category_id:
        product.category = session.get(Category, product.category_id)
    return product


@router.get("", response_model=list[ProductRead])
def list_products(session: Session = Depends(get_db)) -> list[Product]:
    products = session.exec(select(Product)).all()
    for product in products:
        if product.category_id:
            product.category = session.get(Category, product.category_id)
    return products


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, payload: ProductUpdate, session: Session = Depends(get_db)) -> Product:
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="محصول یافت نشد")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    session.add(product)
    session.commit()
    session.refresh(product)
    if product.category_id:
        product.category = session.get(Category, product.category_id)
    return product
