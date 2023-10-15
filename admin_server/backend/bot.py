# libraries
from fastapi import APIRouter, BackgroundTasks

# local
from core.conf import settings
from core.schemas import (
    # payloads
    PatchBotPayload,
    # enums
    ResponseStatusEnum,
)
from services.discord_bot.conf import bot

router = APIRouter(
    responses={404: {"description": "Not found"}},
)
is_discord_bot_started = False


async def start_bot():
    global is_discord_bot_started
    is_discord_bot_started = True

    try:
        await bot.start(settings.DISCORD_BOT_TOKEN)
    except AttributeError:
        print("Bot stop successfully")


@router.get("/bot", tags=["Admin-backend-bot"], status_code=ResponseStatusEnum.OK.value)
async def bot_status():
    return {
        "bot_status": bot.status,
        "is_ws_rate_limited": bot.is_ws_ratelimited(),
        "is_ready": bot.is_ready(),
    }


@router.patch(
    "/bot", tags=["Admin-backend-bot"], status_code=ResponseStatusEnum.ACCEPTED.value
)
async def bot_actions(payloads: PatchBotPayload, background_tasks: BackgroundTasks):
    global is_discord_bot_started

    # if bot not start, start bot
    # *Notice that start bot will block API so start bot background task
    if not is_discord_bot_started and payloads.start:
        background_tasks.add_task(start_bot)
        return {"message": "Bot will start in seconds..."}
    # if bot start, stop bot
    elif is_discord_bot_started and not payloads.start:
        is_discord_bot_started = False
        bot.clear()
        return {"message": "Bot close"}

    return
