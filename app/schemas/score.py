from typing import Optional

from pydantic import BaseModel


# Shared properties
class ScoreBase(BaseModel):
    year: Optional[int] = None
    city_id: Optional[int] = None
    air_quality: Optional[float] = None
    water_pollution: Optional[float] = None


# Properties to receive on Score creation
class ScoreCreate(ScoreBase):
    year: str
    city_id: int


# Properties to receive on Score update
class ScoreUpdate(ScoreBase):
    pass


# Properties shared by models stored in DB
class ScoreInDBBase(ScoreBase):
    id: int
    year: int
    city_id: int
    air_quality: Optional[float]
    water_pollution: Optional[float]

    class Config:  # pylint: disable=too-few-public-methods
        orm_mode = True


# Properties to return to client
class Score(ScoreInDBBase):
    pass


# Properties properties stored in DB
class ScoreInDB(ScoreInDBBase):
    pass
