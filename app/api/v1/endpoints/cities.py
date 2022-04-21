from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import dependencies, security

router = APIRouter()


@router.get("/", response_model=List[schemas.City])
async def read_cities(
    *,
    db: Session = Depends(dependencies.get_db),
    insee_code: Optional[str] = None,
    city_name: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[schemas.City]:
    """
    Retrieve cities.
    """
    if insee_code:
        city = await crud.city.get_by_insee(db, insee_code=insee_code)
        cities = [city]
    elif city_name:
        cities = await crud.city.get_multi_by_name(db, city_name=city_name, skip=skip, limit=limit)
    else:
        cities = await crud.city.get_multi(db, skip=skip, limit=limit)
    return cities


@router.post("/", response_model=schemas.City, dependencies=[Depends(security.is_current_user_admin)])
async def create_city(
    *,
    db: Session = Depends(dependencies.get_db),
    city_in: schemas.CityCreate
) -> schemas.City:
    """
    Create new city.
    """
    try:
        city = await crud.city.create(db=db, obj_in=city_in)
        return city
    except exc.IntegrityError as ex:
        raise HTTPException(status_code=409, detail="City aready exists with same name and Insee code") from ex
    except Exception as ex:
        raise ex


@router.put("/{id}", response_model=schemas.City, dependencies=[Depends(security.is_current_user_admin)])
async def update_city(
    *,
    db: Session = Depends(dependencies.get_db),
    id: int,  # pylint: disable=redefined-builtin
    city_in: schemas.CityUpdate
) -> schemas.City:
    """
    Update a city.
    """
    city = await crud.city.get(db=db, id=id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    city = await crud.city.update(db=db, db_obj=city, obj_in=city_in)
    return city


@router.get("/{id}", response_model=schemas.City)
async def read_city(
    *,
    db: Session = Depends(dependencies.get_db),
    id: int  # pylint: disable=redefined-builtin
) -> schemas.City:
    """
    Get city by ID.
    """
    city = await crud.city.get(db=db, id=id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.get("/insee/{insee_code}", response_model=schemas.City)
async def read_city_by_insee(
    *,
    db: Session = Depends(dependencies.get_db),
    insee_code: str,
) -> schemas.City:
    """
    Retrieve city by INSEE code.
    """
    city = await crud.city.get_by_insee(db, insee_code=insee_code)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.delete("/{id}", response_model=schemas.City, dependencies=[Depends(security.is_current_user_admin)])
async def delete_city(
    *,
    db: Session = Depends(dependencies.get_db),
    id: int  # pylint: disable=redefined-builtin
) -> schemas.City:
    """
    Delete a city.
    """
    city = await crud.city.get(db=db, id=id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    city = await crud.city.remove(db=db, id=id)
    return city


@router.get("/{id}/scores", response_model=List[schemas.Score])
async def read_city_scores(
    *,
    db: Session = Depends(dependencies.get_db),
    id: int,  # pylint: disable=redefined-builtin
    skip: int = 0,
    limit: int = 100
) -> List[schemas.Score]:
    """
    Get scores by city ID.
    """
    city = await crud.city.get(db=db, id=id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    scores = await crud.score.get_multi_by_city(db=db, city_id=id, skip=skip, limit=limit)
    return scores


@router.get("/{id}/scores/{year}", response_model=schemas.Score)
async def read_city_yearly_score(
    *,
    db: Session = Depends(dependencies.get_db),
    id: int,  # pylint: disable=redefined-builtin
    year: int
) -> schemas.Score:
    """
    Get yearly score by city ID.
    """
    city = await crud.city.get(db=db, id=id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    score = await crud.score.get_by_city_year(db=db, city_id=id, year=year)
    if not score:
        raise HTTPException(status_code=404, detail="Yearly score not found")
    return score
