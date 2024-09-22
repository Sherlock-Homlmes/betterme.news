import signal
import asyncio

# libraries
import beanie

# local
from core.conf import app, settings, is_user_portal, is_test_env
from core.models import document_models
from core.database.mongodb import client
from services.discord_bot.conf import bot
from services.facebook_bot.conf import connect_to_facebook_api


running = True


# background task on startup
class BackgroundRunner:
    def __init__(self):
        self.value = 0

    async def run_discord_bot(self):
        print("Starting discord bot...")
        await bot.start(settings.DISCORD_BOT_TOKEN)


runner = BackgroundRunner()


def stop_server(*args):
    global running
    running = False


async def connect_db() -> None:
    print("Connecting to database...")
    await beanie.init_beanie(
        database=client.betterme_news,
        document_models=document_models,
    )
    print("Connect to database success")


@app.on_event("startup")
async def startup():
    global is_discord_bot_started, running

    # Set signal to detach when app stop
    signal.signal(signal.SIGTERM, stop_server)

    # CONNECT DB
    await connect_db()

    if is_test_env:
        return

    if not is_user_portal:
        # RUN BOT
        asyncio.create_task(runner.run_discord_bot())
        # CONNECT FACEBOOK API
        # await encode_new_fb_access_key()
        await connect_to_facebook_api()

    print("Start up done")


@app.on_event("shutdown")
async def shutdown_event():
    if bot.is_ready():
        await bot.close()
