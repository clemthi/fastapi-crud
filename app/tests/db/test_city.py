import pytest

from sqlalchemy.orm import Session

from app import crud
from app.schemas.city import CityCreate, CityUpdate
from app.schemas.score import ScoreCreate
from app.tests.utils.faker import create_random_city_data, create_random_score_data


@pytest.mark.asyncio
async def test_create_city(db: Session) -> None:
    data = create_random_city_data()
    city_in = CityCreate(
        name=data['name'],
        insee_code=data['insee_code'],
        zip_code=data['zip_code'],
        latitude=data['latitude'],
        longitude=data['longitude']
    )
    city = await crud.city.create(db=db, obj_in=city_in)

    assert city.name == data['name']
    assert city.insee_code == data['insee_code']
    assert city.zip_code == data['zip_code']
    assert city.latitude == data['latitude']
    assert city.longitude == data['longitude']


@pytest.mark.asyncio
async def test_get_city(db: Session) -> None:
    data = create_random_city_data()
    city_in = CityCreate(
        name=data['name'],
        insee_code=data['insee_code'],
        zip_code=data['zip_code'],
        latitude=data['latitude'],
        longitude=data['longitude']
    )
    city = await crud.city.create(db=db, obj_in=city_in)
    stored_city = await crud.city.get(db=db, id=city.id)

    assert stored_city
    assert city.id == stored_city.id
    assert city.name == stored_city.name
    assert city.insee_code == stored_city.insee_code
    assert city.zip_code == stored_city.zip_code
    assert city.latitude == stored_city.latitude
    assert city.longitude == stored_city.longitude


@pytest.mark.asyncio
async def test_update_city(db: Session) -> None:
    data = create_random_city_data()
    city_in = CityCreate(
        name=data['name'],
        insee_code=data['insee_code'],
        zip_code=data['zip_code']
    )
    city = await crud.city.create(db=db, obj_in=city_in)

    data_new = create_random_city_data()
    city_update = CityUpdate(name=data_new['name'])
    city_new = await crud.city.update(db=db, db_obj=city, obj_in=city_update)

    assert city.id == city_new.id
    assert city.name == city_new.name
    assert city_new.name == data_new['name']


@pytest.mark.asyncio
async def test_delete_city(db: Session) -> None:
    data = create_random_city_data()
    city_in = CityCreate(
        name=data['name'],
        insee_code=data['insee_code'],
        zip_code=data['zip_code']
    )
    city = await crud.city.create(db=db, obj_in=city_in)
    city_deleted = await crud.city.remove(db=db, id=city.id)
    city_removed = await crud.city.get(db=db, id=city.id)
    assert city_removed is None
    assert city_deleted.id == city.id
    assert city_deleted.name == data['name']
    assert city_deleted.insee_code == data['insee_code']
    assert city_deleted.zip_code == data['zip_code']


@pytest.mark.asyncio
async def test_delete_city_cascade(db: Session) -> None:
    city_data = create_random_city_data()
    city_in = CityCreate(
        name=city_data['name'],
        insee_code=city_data['insee_code'],
        zip_code=city_data['zip_code']
    )
    city = await crud.city.create(db=db, obj_in=city_in)
    assert city.name == city_data['name']
    assert city.insee_code == city_data['insee_code']

    score_data = create_random_score_data(city.id)
    score_in = ScoreCreate(
        city_id=score_data['city_id'],
        year=score_data['year'],
        air_quality=score_data['air_quality'],
        water_pollution=score_data['water_pollution']
    )
    score = await crud.score.create(db=db, obj_in=score_in)
    assert score.city_id == city.id

    city_deleted = await crud.city.remove(db=db, id=city.id)
    city_removed = await crud.city.get(db=db, id=city.id)

    assert city_removed is None
    assert city_deleted.id == city.id
