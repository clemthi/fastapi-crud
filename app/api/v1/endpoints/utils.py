from typing import Any, List

from fastapi import APIRouter, Depends

from app import schemas
from app.api import dependencies
from app.resources.catalog import ResourceCatalog

router = APIRouter()


@router.get("/health-check/", response_model=schemas.Msg)
async def health_check() -> Any:
    """
    Test API status
    """
    return {'msg': 'OK'}


@router.get("/score-descriptions/", response_model=List[schemas.ScoreDescription])
async def scores_descriptions(
    *,
    catalog: ResourceCatalog = Depends(dependencies.get_resource_catalog)
) -> Any:
    """
    Returns score types description
    """
    return catalog.get_score_description()
