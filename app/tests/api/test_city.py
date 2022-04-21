import pytest

from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.config import settings

from app.tests.utils.dependency_overrider import DependencyOverrider
from app.tests.utils.faker import create_random_city_db, create_random_city_data

from app.api.dependencies import get_auth
from app.tests.overrides import override_get_auth_admin


@pytest.mark.asyncio
async def test_create_city_as_admin(client: AsyncClient) -> None:
    with DependencyOverrider(app, overrides={get_auth: override_get_auth_admin}):
        data = create_random_city_data()
        response = await client.post(f'{settings.API_V1_STR}/cities/', json=data)
        assert response.status_code == 200
        content = response.json()
        assert content['name'] == data['name']
        assert content['insee_code'] == data['insee_code']
        assert content['zip_code'] == data['zip_code']
        assert content['latitude'] == data['latitude']
        assert content['longitude'] == data['longitude']
        assert 'id' in content


@pytest.mark.asyncio
async def test_create_city_as_user(client: AsyncClient) -> None:
    data = create_random_city_data()
    response = await client.post(f'{settings.API_V1_STR}/cities/', json=data)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_read_city(client: AsyncClient, db: Session) -> None:
    city = await create_random_city_db(db)

    response = await client.get(f'{settings.API_V1_STR}/cities/{city.id}')
    assert response.status_code == 200
    content = response.json()
    assert content['id'] == city.id
    assert content['name'] == city.name
    assert content['insee_code'] == city.insee_code
    assert content['zip_code'] == city.zip_code
    assert content['latitude'] == city.latitude
    assert content['longitude'] == city.longitude


@pytest.mark.asyncio
async def test_delete_city_as_admin(client: AsyncClient, db: Session) -> None:
    with DependencyOverrider(app, overrides={get_auth: override_get_auth_admin}):
        city = await create_random_city_db(db)

        response = await client.delete(f'{settings.API_V1_STR}/cities/{city.id}')
        assert response.status_code == 200
        content = response.json()
        assert content['id'] == city.id
        assert content['name'] == city.name
        assert content['insee_code'] == city.insee_code
        assert content['zip_code'] == city.zip_code

        response = await client.get(f'{settings.API_V1_STR}/cities/{city.id}')
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_city_as_user(client: AsyncClient, db: Session) -> None:
    city = await create_random_city_db(db)

    response = await client.delete(f'{settings.API_V1_STR}/cities/{city.id}')
    assert response.status_code == 403
