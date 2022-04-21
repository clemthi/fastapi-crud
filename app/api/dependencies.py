from typing import Generator

from fastapi import Depends
from pydantic import Json

from app.db.session import SessionLocal
from app.resources.catalog import ResourceCatalog, catalog
from app.api.security import get_auth


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user_id(token_data: Json = Depends(get_auth)) -> str:
    return token_data.get('sub', '')


def get_resource_catalog() -> ResourceCatalog:
    yield catalog
