# fastapi
from fastapi import Depends, APIRouter, HTTPException

# default

# local
from .auth_handler import auth_handler

from core.models import Users, UserRoleEnum
from core.conf import settings


router = APIRouter(
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)


@router.get("/oauth-link")
async def get_oauth_link():
    return {"discord_link": settings.DISCORD_OAUTH_URL}


@router.get("/self", dependencies=[Depends(auth_handler.auth_wrapper)])
def protected(user: Users = Depends(auth_handler.auth_wrapper)):
    if UserRoleEnum.ADMIN.value not in user["roles"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    return user
