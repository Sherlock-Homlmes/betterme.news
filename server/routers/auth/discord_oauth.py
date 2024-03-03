# fastapi

# libraries
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_discord import User, DiscordOAuthClient
import aiohttp
from beanie.odm.operators.update.general import Set

# local
from .auth_handler import auth_handler
from core.conf import settings, is_dev_env
from core.models import Users, UserRoleEnum
from services.time_modules import Time


router = APIRouter(
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)


discord_oauth = DiscordOAuthClient(
    settings.DISCORD_CLIENT_ID,
    settings.DISCORD_CLIENT_SECRET,
    settings.DISCORD_REDIRECT_URL,
    ("identify", "guilds", "email"),
)  # scopes


# start
@router.on_event("startup")
async def on_startup():
    await discord_oauth.init()
    print("Discord oauth start done")


@router.get("/discord-oauth")
async def get_discord_oauth(code: str, request: Request):
    # discord oauth and get JWT token
    self_url = str(request.url).split("/api/")[0]
    token, refresh_token = await discord_oauth.get_access_token(code)

    headersList = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        res = await session.get(url=f"{self_url}/api/auth/discord/users/self", headers=headersList)
        try:
            discord_user = await res.json()
        except Exception:
            raise HTTPException(status_code=404, detail="Invalid code")

    await Users.find_one(Users.discord_id == discord_user["id"]).upsert(
        Set(
            {
                Users.email: discord_user["email"],
                Users.last_logged_in_at: Time().now,
                Users.name: discord_user["username"],
                Users.avatar_url: discord_user["avatar_url"],
            }
        ),
        on_insert=Users(
            email=discord_user["email"],
            user_type="discord",
            locale=discord_user["locale"],
            name=discord_user["username"],
            avatar_url=discord_user["avatar_url"],
            discord_id=discord_user["id"],
            last_logged_in_at=Time().now,
            created_at=Time().now,
            roles=[UserRoleEnum.ADMIN] if is_dev_env else [UserRoleEnum.USER],
        ),
    )
    user = await Users.find_one(Users.discord_id == discord_user["id"])

    user_info = user.get_info()
    token = auth_handler.encode_token(user_info)
    return {"token": token}


@router.get(
    "/discord/users/self",
    dependencies=[Depends(discord_oauth.requires_authorization)],
    response_model=User,
)
async def get_user(user: User = Depends(discord_oauth.user)):
    return user
