from typing import Tuple


import pytest

from sqlalchemy.orm import Session

from app import crud
from app.schemas.score import ScoreCreate, ScoreUpdate
from app.models import Score
from app.tests.utils.faker import create_random_city_db, create_random_score_data


async def create_score(db: Session) -> Tuple[dict, Score]:
    city = await create_random_city_db(db)

    data = create_random_score_data(city.id)
    score_in = ScoreCreate(
        city_id=data['city_id'],
        year=data['year'],
        air_quality=data['air_quality'],
        water_pollution=data['water_pollution']
    )
    score = await crud.score.create(db=db, obj_in=score_in)
    return data, score


@pytest.mark.asyncio
async def test_create_score(db: Session) -> None:
    data, score = await create_score(db)

    assert score.city_id == data['city_id']
    assert score.year == data['year']
    assert score.air_quality == data['air_quality']
    assert score.water_pollution == data['water_pollution']


@pytest.mark.asyncio
async def test_get_score(db: Session) -> None:
    _, score = await create_score(db)
    stored_score = await crud.score.get(db=db, id=score.id)

    assert stored_score
    assert score.city_id == stored_score.city_id
    assert score.year == stored_score.year
    assert score.air_quality == stored_score.air_quality
    assert score.water_pollution == stored_score.water_pollution


@pytest.mark.asyncio
async def test_update_score(db: Session) -> None:
    _, score = await create_score(db)

    data_new = create_random_score_data(score.city_id)
    score_update = ScoreUpdate(air_quality=data_new['air_quality'], water_pollution=data_new['water_pollution'])
    score_new = await crud.score.update(db=db, db_obj=score, obj_in=score_update)

    assert score.id == score_new.id
    assert score.air_quality == score_new.air_quality
    assert score_new.air_quality == data_new['air_quality']
    assert score_new.water_pollution == data_new['water_pollution']


@pytest.mark.asyncio
async def test_delete_score(db: Session) -> None:
    data, score = await create_score(db)

    score_deleted = await crud.score.remove(db=db, id=score.id)
    score_removed = await crud.score.get(db=db, id=score.id)
    assert score_removed is None
    assert score_deleted.id == score.id
    assert score_deleted.city_id == data['city_id']
    assert score_deleted.year == data['year']
