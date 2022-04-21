from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __display_name__, __version__, __description__
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=__display_name__,
    description=__description__,
    version=__version__,
    openapi_url=f'{settings.API_V1_STR}/openapi.json'
)

if settings.ALLOWED_ORIGINS:
    allow_origins = [str(o) for o in settings.ALLOWED_ORIGINS]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(api_router, prefix=settings.API_V1_STR)
