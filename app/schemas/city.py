from typing import Optional

from pydantic import BaseModel


# Shared properties
class CityBase(BaseModel):
    name: Optional[str] = None
    insee_code: Optional[str] = None
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


# Properties to receive on item creation
class CityCreate(CityBase):
    name: str
    insee_code: str
    zip_code: str
    latitude: Optional[float]
    longitude: Optional[float]


# Properties to receive on item update
class CityUpdate(CityBase):
    pass


# Properties shared by models stored in DB
class CityInDBBase(CityBase):
    id: int
    name: str
    insee_code: str
    zip_code: str
    latitude: Optional[float]
    longitude: Optional[float]

    class Config:  # pylint: disable=too-few-public-methods
        orm_mode = True


# Properties to return to client
class City(CityInDBBase):
    pass


# Properties properties stored in DB
class CityInDB(CityInDBBase):
    pass
