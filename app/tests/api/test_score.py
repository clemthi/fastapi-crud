import pytest

from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.config import settings

from app.tests.utils.dependency_overrider import DependencyOverrider
from app.tests.utils.faker import create_random_city_db, create_random_score_db, create_random_score_data

from app.api.dependencies import get_auth
from app.tests.overrides import override_get_auth_admin


@pytest.mark.asyncio
async def test_create_score_as_admin(client: AsyncClient, db: Session) -> None:
    with DependencyOverrider(app, overrides={get_auth: override_get_auth_admin}):
        city = await create_random_city_db(db)
        data = create_random_score_data(city.id)

        response = await client.post(f'{settings.API_V1_STR}/scores/', json=data)
        assert response.status_code == 200
        content = response.json()
        assert content['city_id'] == data['city_id']
        assert content['year'] == data['year']
        assert content['air_quality'] == data['air_quality']
        assert content['water_pollution'] == data['water_pollution']
        assert 'id' in content


@pytest.mark.asyncio
async def test_create_score_as_user(client: AsyncClient, db: Session) -> None:
    city = await create_random_city_db(db)
    data = create_random_score_data(city.id)
    response = await client.post(f'{settings.API_V1_STR}/scores/', json=data)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_read_score(client: AsyncClient, db: Session) -> None:
    city = await create_random_city_db(db)
    score = await create_random_score_db(db, city.id)

    response = await client.get(f'{settings.API_V1_STR}/scores/{score.id}')
    assert response.status_code == 200
    content = response.json()
    assert content['id'] == score.id
    assert content['city_id'] == score.city_id
    assert content['year'] == score.year
    assert content['air_quality'] == score.air_quality
    assert content['water_pollution'] == score.water_pollution


@pytest.mark.asyncio
async def test_delete_score_as_admin(client: AsyncClient, db: Session) -> None:
    with DependencyOverrider(app, overrides={get_auth: override_get_auth_admin}):
        city = await create_random_city_db(db)
        score = await create_random_score_db(db, city.id)

        response = await client.delete(f'{settings.API_V1_STR}/scores/{score.id}')
        assert response.status_code == 200
        content = response.json()
        assert content['id'] == score.id
        assert content['city_id'] == score.city_id
        assert content['year'] == score.year
        assert content['air_quality'] == score.air_quality
        assert content['water_pollution'] == score.water_pollution

        response = await client.get(f'{settings.API_V1_STR}/scores/{score.id}')
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_score_as_user(client: AsyncClient, db: Session) -> None:
    city = await create_random_city_db(db)
    score = await create_random_score_db(db, city.id)

    response = await client.delete(f'{settings.API_V1_STR}/scores/{score.id}')
    assert response.status_code == 403
