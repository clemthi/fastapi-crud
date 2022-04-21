from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import exc
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import dependencies, security

router = APIRouter()


@router.get("/", response_model=List[schemas.Score])
async def read_scores(
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100
) -> List[schemas.Score]:
    """
    Retrieve scores.
    """
    scores = await crud.score.get_multi(db, skip=skip, limit=limit)

    return scores


@router.post("/", response_model=schemas.Score, dependencies=[Depends(security.is_current_user_admin)])
async def create_score(
    *,
    db: Session = Depends(dependencies.get_db),
    score_in: schemas.ScoreCreate
) -> schemas.Score:
    """
    Create new score.
    """
    city = await crud.city.get(db=db, id=score_in.city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    try:
        score = await crud.score.create(db=db, obj_in=score_in)
        return score
    except exc.IntegrityError as ex:
        raise HTTPException(status_code=409, detail="Score aready exists with same city and year") from ex
    except Exception as ex:
        raise ex


@router.put("/{id}", response_model=schemas.Score, dependencies=[Depends(security.is_current_user_admin)])
async def update_score(
    *,
    db: Session = Depends(dependencies.get_db),
    id: int,  # pylint: disable=redefined-builtin
    score_in: schemas.ScoreUpdate
) -> schemas.Score:
    """
    Update an score.
    """
    score = await crud.score.get(db=db, id=id)
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    if score_in.city_id is not None:
        city = await crud.city.get(db=db, id=score_in.city_id)
        if not city:
            raise HTTPException(status_code=404, detail="City not found")

    score = await crud.score.update(db=db, db_obj=score, obj_in=score_in)

    return score


@router.get("/{id}", response_model=schemas.Score)
async def read_score(
    *,
    db: Session = Depends(dependencies.get_db),
    id: int  # pylint: disable=redefined-builtin
) -> schemas.Score:
    """
    Get score by ID.
    """
    score = await crud.score.get(db=db, id=id)
    if not score:
        return JSONResponse(status_code=404, content={'msg': "Score not found"})

    return score


@router.delete("/{id}", response_model=schemas.Score, dependencies=[Depends(security.is_current_user_admin)])
async def delete_score(
    *,
    db: Session = Depends(dependencies.get_db),
    id: int  # pylint: disable=redefined-builtin
) -> Any:
    """
    Delete an score.
    """
    score = await crud.score.get(db=db, id=id)
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    score = await crud.score.remove(db=db, id=id)

    return score
