import asyncio

from sqlalchemy.orm import Session

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
from app.db import base
from app import crud, schemas, models


def init_db(db: Session, create_dataset: bool = False) -> None:
    # uncomment this line if you don't use alembic to create the db schema
    # create_db_schema(db)
    if create_dataset:
        asyncio.get_event_loop().run_until_complete(create_inital_dataset(db))


def create_db_schema(db: Session) -> None:
    base.Base.metadata.create_all(bind=db.get_bind())  # pylint: disable=no-member


async def create_inital_dataset(db: Session) -> None:
    # TODO replace this place holder code to create a real initial dataset mandatory for the app to work
    # maybe with a CSV as datasource or something like that

    # only insert data is table is empty
    if db.query(models.City).first() is None:
        # dummy data
        city_1 = await crud.city.create(
            db, obj_in=schemas.CityCreate(name='TOULOUSE', insee_code='31555', zip_code='31000', latitude=43.5963814303, longitude=1.43167293364))
        city_2 = await crud.city.create(
            db, obj_in=schemas.CityCreate(name='BORDEAUX', insee_code='33063', zip_code='33000', latitude=44.8572445351, longitude=-0.57369678116))
        await crud.city.create(
            db, obj_in=schemas.CityCreate(name='NANTES', insee_code='44109', zip_code='44000', latitude=47.2316356767, longitude=-1.54831008605))

        await crud.score.create(db, obj_in=schemas.ScoreCreate(year=2000, city_id=city_1.id, environmental=100))
        await crud.score.create(db, obj_in=schemas.ScoreCreate(year=2001, city_id=city_1.id, environmental=95))
        await crud.score.create(db, obj_in=schemas.ScoreCreate(year=2000, city_id=city_2.id, environmental=90))

    if db.query(models.Category).first() is None:
        await crud.category.create(db, obj_in=schemas.CategoryCreate(code='PORT', name='Port facilities'))
        await crud.category.create(db, obj_in=schemas.CategoryCreate(code='HIGH DENSITY', name='High density city'))
        await crud.category.create(db, obj_in=schemas.CategoryCreate(code='TOURIST', name='Touristic city'))
