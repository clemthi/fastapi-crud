from typing import Optional

from pydantic import BaseModel


# Shared properties
class CategoryBase(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on Category creation
class CategoryCreate(CategoryBase):
    code: str
    name: str


# Properties to receive on Category update
class CategoryUpdate(CategoryBase):
    pass


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: int
    code: str
    name: str
    description: Optional[str]

    class Config:  # pylint: disable=too-few-public-methods
        orm_mode = True


# Properties to return to client
class Category(CategoryInDBBase):
    pass


# Properties properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass
