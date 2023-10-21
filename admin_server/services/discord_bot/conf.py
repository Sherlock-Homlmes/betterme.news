# default
import asyncio
from dataclasses import dataclass

# library
import discord
from discord.ext import commands

# local
from core.conf import settings
from services.discord_bot.func import get_channel

is_app_running = True


####### BOT #######
class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        global is_app_running

        print(f"We have logged in as {self.user} news bot")
        if settings.IS_DEV_ENV:
            # Stop bot when reload
            while is_app_running:
                from core.event_handler import running

                if running:
                    await asyncio.sleep(1)
                else:
                    await self.close()
                    is_app_running = False

    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral=True)


@dataclass
class ServerInfo:
    # ids
    guild_id: int = 880360143768924210
    admin_role_id: int = 890244740174467082
    # guild
    guild: discord.Guild = None
    # role
    admin_role: discord.Role = None
    # news channels
    test_news_channel: discord.ForumChannel = None
    news_channel: discord.ForumChannel = None


async def get_server_info():
    global bot, server_info

    ### Get server info
    server_info_data = {
        "test_news_channel": 1098594858450554940,
        "news_channel": 1094468765527330918,
    }

    # get guild
    server_info.guild = await bot.fetch_guild(server_info.guild_id)

    # get roles
    server_info.admin_role = server_info.guild.get_role(server_info.admin_role_id)

    channels = (
        "test_news_channel",
        "news_channel",
    )
    (
        server_info.test_news_channel,
        server_info.news_channel,
    ) = await asyncio.gather(
        *[
            get_channel(server_info.guild, server_info_data[channel])
            for channel in channels
        ]
    )


### START
prefix = "news!"
bot = Bot(command_prefix=prefix, intents=discord.Intents.all())
server_info = ServerInfo()


@bot.listen()
async def on_ready():
    global server_info
    await get_server_info()
    print("News bot startup done")
