from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.category import Category

from app.schemas.category import CategoryCreate, CategoryUpdate


class CRUDScore(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass


category = CRUDScore(Category)
