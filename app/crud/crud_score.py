from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.score import Score

from app.schemas.score import ScoreCreate, ScoreUpdate


class CRUDScore(CRUDBase[Score, ScoreCreate, ScoreUpdate]):
    async def get_multi_by_city(
        self, db: Session, *, city_id: int, skip: int = 0, limit: int = 100
    ) -> List[Score]:
        return (
            db.query(self.model)
            .filter(Score.city.has(id=city_id))
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def get_by_city_year(
        self, db: Session, *, city_id: int, year: int
    ) -> List[Score]:
        return (
            db.query(self.model)
            .filter(and_(Score.city.has(id=city_id), Score.year == year))
            .first()
        )


score = CRUDScore(Score)
