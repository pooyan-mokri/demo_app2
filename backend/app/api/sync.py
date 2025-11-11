from __future__ import annotations

from fastapi import APIRouter, Depends

from ..services.woocommerce import fetch_woocommerce
from .deps import get_current_user

router = APIRouter(prefix="/sync", tags=["sync"], dependencies=[Depends(get_current_user)])


@router.get("/woocommerce/products")
async def sync_products(page: int = 1) -> dict[str, object]:
    data = await fetch_woocommerce("/wp-json/wc/v3/products", params={"page": page})
    return {"message": "محصولات دریافت شد", "data": data}
