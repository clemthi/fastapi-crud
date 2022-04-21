import random
import string

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.city import CityCreate
from app.schemas.score import ScoreCreate


def random_lower_string(length=30) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def random_latitude() -> float:
    return random.uniform(-90, 90)


def random_longitude() -> float:
    return random.uniform(-180, 180)


def random_score() -> float:
    return random.uniform(0, 100)


def create_random_city_db(db: Session) -> models.City:
    city = CityCreate(
        name=random_lower_string(),
        insee_code=random_lower_string(10),
        zip_code=random_lower_string(10),
        latitude=random_latitude(),
        longitude=random_longitude()
    )
    return crud.city.create(db=db, obj_in=city)


def create_random_city_data() -> dict:
    return {
        'name': random_lower_string(),
        'insee_code': random_lower_string(10),
        'zip_code': random_lower_string(10),
        'latitude': random_latitude(),
        'longitude': random_longitude()
    }


def create_random_score_db(db: Session, city_id: int) -> models.Score:
    city = ScoreCreate(
        city_id=city_id,
        year=random.randrange(1980, 2020),
        air_quality=random_score(),
        water_pollution=random_score()
    )
    return crud.score.create(db=db, obj_in=city)


def create_random_score_data(city_id: int) -> dict:
    return {
        'city_id': city_id,
        'year': random.randrange(1980, 2020),
        'air_quality': random_score(),
        'water_pollution': random_score()
    }
