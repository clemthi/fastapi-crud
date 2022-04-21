from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base


if TYPE_CHECKING:
    from .city import City  # noqa: F401


class Score(Base):  # pylint: disable=too-few-public-methods
    id = Column('sco_id', Integer, primary_key=True)
    city_id = Column('sco_idcity', Integer, ForeignKey('city.cit_id', ondelete="CASCADE"), nullable=False, index=True)
    year = Column('sco_year', Integer, nullable=False, index=True)
    air_quality = Column('sco_airquality', Float, nullable=True)
    water_pollution = Column('sco_waterpollution', Float, nullable=True)

    city = relationship('City', back_populates='scores')

    __table_args__ = (
        UniqueConstraint('sco_idcity', 'sco_year', name='ix_sco_year_idcity'),
    )
