from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base


if TYPE_CHECKING:
    from .score import Score  # noqa: F401


class City(Base):  # pylint: disable=too-few-public-methods
    id = Column('cit_id', Integer, primary_key=True)
    name = Column('cit_name', String(300), index=True, nullable=False)
    insee_code = Column('cit_codeinsee', String(300), index=True, nullable=False)
    zip_code = Column('cit_zipcode', String(10), index=True, nullable=False)
    latitude = Column('cit_lat', Float, nullable=True)
    longitude = Column('cit_lon', Float, nullable=True)

    scores = relationship('Score', back_populates='city', passive_deletes=True)

    __table_args__ = (
        UniqueConstraint('cit_name', 'cit_codeinsee', name='ux_cit_name_codeinsee'),
    )
