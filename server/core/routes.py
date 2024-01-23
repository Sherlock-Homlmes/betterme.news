# libraries
from fastapi import APIRouter

# local
from routers.admin import crawlers as be_crawlers, tags
from routers.user import posts

# create all api routers
api_router = APIRouter()
for admin_be_service in [be_crawlers, tags]:
    api_router.include_router(
        admin_be_service.router,
        prefix="/api/admin",
        responses={404: {"description": "Not found"}},
    )

for user_be_service in [posts]:
    api_router.include_router(
        user_be_service.router,
        prefix="/api",
        responses={404: {"description": "Not found"}},
    )
