# libraries
from fastapi import APIRouter

# local
from routers import users

# create all api routers(for include in app and testing)
api_router = APIRouter()
for router in [
    users,
]:
    api_router.include_router(
        router.router,
        prefix="/api",
        responses={404: {"description": "Not found"}},
    )
