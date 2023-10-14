# libraries
from fastapi import APIRouter

# local
from backend import (
    crawlers as be_crawlers,
    bot as be_bot,
)
from frontend.routers import crawlers as fe_crawlers

# create all api routers
api_router = APIRouter()
for be_service in [be_crawlers, be_bot]:
    api_router.include_router(
        be_service.router,
        prefix="/api",
        responses={404: {"description": "Not found"}},
    )

for fe_service in [
    fe_crawlers,
]:
    api_router.include_router(
        fe_service.router,
        responses={404: {"description": "Not found"}},
    )
