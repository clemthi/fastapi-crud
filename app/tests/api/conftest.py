from typing import Generator

import pytest

from httpx import AsyncClient

from app.main import app
from app.api.dependencies import get_auth, get_db
from app.tests.overrides import override_get_db, override_get_auth


@pytest.fixture(scope="module")
def client() -> Generator:
    # global overrides
    app.dependency_overrides = {
        get_db: override_get_db,
        get_auth: override_get_auth
    }

    try:
        async_client = AsyncClient(app=app, base_url="http://test")
        yield async_client
    finally:
        pass
