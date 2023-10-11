# libraries
from fastapi import APIRouter

# local
from backend import crawl

# from frontent import

# create all api routers(for include in app and testing)
api_router = APIRouter()
for service in [
    crawl,
]:
    api_router.include_router(
        service.router,
        prefix="/api",
        responses={404: {"description": "Not found"}},
    )
