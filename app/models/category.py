from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Category(Base):  # pylint: disable=too-few-public-methods
    id = Column('cat_id', Integer, primary_key=True)
    code = Column('cat_code', String(20), index=True, nullable=False)
    name = Column('cat_name', String(300), nullable=False)
    description = Column('cat_description', String(1000), nullable=True)

    __table_args__ = (
        UniqueConstraint('cat_code', name='ux_cat_code'),
        UniqueConstraint('cat_name', name='ux_cat_name'),
    )
