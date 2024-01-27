# libraries
from fastapi import APIRouter

# local
from .conf import settings, ENVEnum
from routers.admin import crawlers, posts as admin_posts
from routers.user import posts as user_posts, tags

# create all api routers
api_router = APIRouter()
admin_routers = [crawlers, admin_posts]
user_routers = [user_posts, tags]


def include_admin_routers():
    global admin_routers, api_router

    for admin_router in admin_routers:
        api_router.include_router(
            admin_router.router,
            prefix="/api/admin",
            responses={404: {"description": "Not found"}},
        )


def include_user_routers():
    global admin_routers, api_router

    for user_router in user_routers:
        api_router.include_router(
            user_router.router,
            prefix="/api",
            responses={404: {"description": "Not found"}},
        )


if settings.ENV == ENVEnum.DEV.value:
    include_admin_routers()
    include_user_routers()
elif settings.ENV == ENVEnum.ADMIN.value:
    include_admin_routers()
    include_user_routers()
elif settings.ENV == ENVEnum.USER.value:
    include_user_routers()
