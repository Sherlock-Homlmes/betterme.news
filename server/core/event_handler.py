import signal
import asyncio

# libraries
import beanie

# local
from core.conf import app, settings
from core.database.mongodb import client
from core.models import (
    Users,
    Posts,
    DraftPosts,
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


runner = BackgroundRunner()


def stop_server(*args):
    global running
    running = False


async def connect_db() -> None:
    print("Connecting to database...")
    await beanie.init_beanie(
        database=client.betterme_news,
        document_models=[
            Users,
            Posts,
            DraftPosts,
        ],
    )
    print("Connect to database success")


@app.on_event("startup")
async def startup():
    global is_discord_bot_started, running

    # Set signal to detach when app stop
    signal.signal(signal.SIGTERM, stop_server)

    # CONNECT DB
    await connect_db()

    # RUN BOT
    asyncio.create_task(runner.run_discord_bot())

    print("Start up done")


@app.on_event("shutdown")
async def shutdown_event():
    if bot.is_ready():
        await bot.close()
