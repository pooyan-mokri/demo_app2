from __future__ import annotations

from typing import Any

import httpx

from ..core.config import get_settings


async def fetch_woocommerce(endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    settings = get_settings()
    if not settings.woo_base_url or not settings.woo_consumer_key or not settings.woo_consumer_secret:
        raise RuntimeError("WooCommerce تنظیم نشده است")

    auth_params = {
        "consumer_key": settings.woo_consumer_key,
        "consumer_secret": settings.woo_consumer_secret,
    }
    async with httpx.AsyncClient(base_url=settings.woo_base_url) as client:
        response = await client.get(endpoint, params={**auth_params, **(params or {})})
        response.raise_for_status()
        return response.json()
