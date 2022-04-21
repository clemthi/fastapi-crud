from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate


class CRUDCity(CRUDBase[City, CityCreate, CityUpdate]):
    async def get_by_insee(
        self, db: Session, *, insee_code: str
    ) -> City:
        return (
            db.query(self.model)
            .filter(City.insee_code == insee_code)
            .first()
        )

    async def get_multi_by_name(
        self, db: Session, *, city_name: str, skip: int = 0, limit: int = 100
    ) -> List[City]:
        return (
            db.query(self.model)
            .filter(City.name.ilike(f'{city_name}%'))
            .offset(skip)
            .limit(limit)
            .all()
        )


city = CRUDCity(City)
