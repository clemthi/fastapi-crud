from fastapi import APIRouter, Depends

from app.api.v1.endpoints import cities, scores, utils
from app.api import security


api_router = APIRouter()
api_router.include_router(utils.router, prefix='/utils', tags=['utils'])
api_router.include_router(cities.router, prefix='/cities', tags=['cities'], dependencies=[Depends(security.get_auth)])
api_router.include_router(scores.router, prefix='/scores', tags=['scores'], dependencies=[Depends(security.get_auth)])
