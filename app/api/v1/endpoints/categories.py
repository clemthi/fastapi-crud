from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import exc
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import dependencies, security

router = APIRouter()


@router.get("/", response_model=List[schemas.Category])
async def read_categories(
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100
) -> List[schemas.Category]:
    """
    Retrieve categories.
    """
    categories = await crud.category.get_multi(db, skip=skip, limit=limit)

    return categories


@router.post("/", response_model=schemas.Category, dependencies=[Depends(security.is_current_user_admin)])
async def create_category(
    *,
    db: Session = Depends(dependencies.get_db),
    category_in: schemas.CategoryCreate
) -> schemas.Category:
    """
    Create new category.
    """
    category = await crud.category.create(db=db, obj_in=category_in)

    return category


@router.put("/{id}", response_model=schemas.Category, dependencies=[Depends(security.is_current_user_admin)])
async def update_category(
    *,
    db: Session = Depends(dependencies.get_db),
    id: int,  # pylint: disable=redefined-builtin
    category_in: schemas.CategoryUpdate
) -> schemas.Category:
    """
    Update an category.
    """
    category = await crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = await crud.category.update(db=db, db_obj=category, obj_in=category_in)

    return category


@router.get("/{id}", response_model=schemas.Category)
async def read_category(
    *,
    db: Session = Depends(dependencies.get_db),
    id: int  # pylint: disable=redefined-builtin
) -> schemas.Category:
    """
    Get category by ID.
    """
    category = await crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


@router.delete("/{id}", response_model=schemas.Category, dependencies=[Depends(security.is_current_user_admin)])
async def delete_score(
    *,
    db: Session = Depends(dependencies.get_db),
    id: int  # pylint: disable=redefined-builtin
) -> Any:
    """
    Delete an score.
    """
    category = await crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = await crud.category.remove(db=db, id=id)

    return category
