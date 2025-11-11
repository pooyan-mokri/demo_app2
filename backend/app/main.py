from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, products, purchases, reports, sales, sync
from .core.config import get_settings
from .core.db import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


settings = get_settings()
app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(products.router, prefix=settings.api_prefix)
app.include_router(sales.router, prefix=settings.api_prefix)
app.include_router(purchases.router, prefix=settings.api_prefix)
app.include_router(reports.router, prefix=settings.api_prefix)
app.include_router(sync.router, prefix=settings.api_prefix)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "TheMoak ERP API"}
