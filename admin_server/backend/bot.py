# libraries
from fastapi import APIRouter

# local
from core.conf import settings
from core.schemas import (
    # enums
    ResponseStatusEnum,
)
from services.discord_bot.conf import bot

router = APIRouter(
    responses={404: {"description": "Not found"}},
)
is_discord_bot_started = False


@router.get("/bot", tags=["Admin-backend-bot"], status_code=ResponseStatusEnum.OK.value)
async def bot_status():
    return {
        "bot_status": bot.status,
        "is_ws_rate_limited": bot.is_ws_ratelimited(),
        "is_ready": bot.is_ready(),
    }


@router.post(
    "/bot", tags=["Admin-backend-bot"], status_code=ResponseStatusEnum.CREATED.value
)
async def start_bot():
    global is_discord_bot_started

    if not is_discord_bot_started:
        is_discord_bot_started = True
        await bot.start(settings.DISCORD_BOT_TOKEN)
