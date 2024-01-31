import signal
import asyncio

# libraries
import beanie
import aiohttp

# local
from core.conf import app, settings, ENVEnum
from core.database.mongodb import client
from core.models import (
    Posts,
    Users,
)
from services.discord_bot.conf import bot

running = True


# background task on startup
class BackgroundRunner:
    def __init__(self):
        self.value = 0

    async def run_discord_bot(self):
        print("Starting discord bot...")
        await bot.start(settings.DISCORD_BOT_TOKEN)

    async def run_keep_alive(self):
        if settings.ENV == ENVEnum.ADMIN.value:
            while True:
                async with aiohttp.ClientSession() as session:
                    await session.get(url="http://localhost:8080/api/auth/self")
                await asyncio.sleep(60)


runner = BackgroundRunner()


def stop_server(*args):
    global running
    running = False


@app.on_event("startup")
async def startup():
    global is_discord_bot_started, running

    # Set signal to detach when app stop
    signal.signal(signal.SIGTERM, stop_server)

    # CONNECT DB
    print("Connecting to database...")
    await beanie.init_beanie(
        database=client.betterme_news,
        document_models=[
            Posts,
            Users,
        ],
    )
    print("Connect to database success")

    # RUN BOT
    asyncio.create_task(runner.run_discord_bot())
    asyncio.create_task(runner.run_keep_alive())

    print("Start up done")


@app.on_event("shutdown")
async def shutdown_event():
    if bot.is_ready():
        await bot.close()
