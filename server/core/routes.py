# libraries
from fastapi import APIRouter, Depends

# local
from .conf import settings, ENVEnum
from routers.auth import auth, discord_oauth, auth_handler
from routers.admin import crawlers, posts as admin_posts
from routers.user import posts as user_posts, tags

# create all api routers
api_router = APIRouter()
auth_routers = [auth, discord_oauth]
admin_routers = [crawlers, admin_posts]
user_routers = [user_posts, tags]


def include_auth_routers():
    global auth_routers, api_router

    for auth_router in auth_routers:
        api_router.include_router(
            auth_router.router,
            prefix="/api/auth",
            responses={404: {"description": "Not found"}},
        )


def include_admin_routers():
    global admin_routers, api_router

    for admin_router in admin_routers:
        api_router.include_router(
            admin_router.router,
            prefix="/api/admin",
            responses={404: {"description": "Not found"}},
            dependencies=[Depends(auth_handler.auth_wrapper)],
        )


def include_user_routers():
    global admin_routers, api_router

    for user_router in user_routers:
        api_router.include_router(
            user_router.router,
            prefix="/api",
            responses={404: {"description": "Not found"}},
        )


include_auth_routers()
if settings.ENV == ENVEnum.DEV.value:
    include_admin_routers()
    include_user_routers()
elif settings.ENV == ENVEnum.ADMIN.value:
    include_admin_routers()
    include_user_routers()
elif settings.ENV == ENVEnum.USER.value:
    include_user_routers()
