# libraries
from fastapi import APIRouter

# local
from routers.admin import crawlers as be_crawlers, tags

# create all api routers
api_router = APIRouter()
for admin_be_service in [be_crawlers, tags]:
    api_router.include_router(
        admin_be_service.router,
        prefix="/api/admin",
        responses={404: {"description": "Not found"}},
    )
