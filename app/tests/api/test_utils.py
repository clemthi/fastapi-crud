import pytest

from httpx import AsyncClient

from app.core.config import settings
from app.resources.catalog import catalog


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    response = await client.get(f'{settings.API_V1_STR}/utils/health-check/')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_score_description(client: AsyncClient) -> None:
    score_cat = catalog.get_score_description()

    response = await client.get(f'{settings.API_V1_STR}/utils/score-descriptions/')

    assert response.status_code == 200
    content = response.json()
    assert score_cat == content
