# default

# library
import discord

# local
from .conf import server_info
from core.schemas.admin import (
    GetCrawlersIvolunteerDataResponse,
)


# TODO:
# -> rename func
# ->.pass post description
# -> revert deadline
# -> tags
# -> button more info
async def send_news(data: GetCrawlersIvolunteerDataResponse, is_testing: bool = True) -> int:
    # for tag in server_info.news_channel.available_tags:
    #     print(tag)

    embed = discord.Embed(
        title=data.title,
        color=discord.Colour.yellow(),
        description=f"**{data.description}**",
    )
    embed.add_field(name="Deadline", value=data.deadline, inline=False)
    # TODO: post name
    # embed.add_field(
    #     name="More info", value=f"https://betterme.news/{data}", inline=False
    # )
    file = discord.File(f"scrap/data/media/{data.banner}", filename=data.banner)

    post: discord.Thread = None
    if is_testing is True:
        post = await server_info.test_news_channel.create_thread(
            name=data.title,
            file=file,
            embed=embed,
        )
    else:
        post = await server_info.news_channel.create_thread(
            name=data.title,
            file=file,
            embed=embed,
        )

    return post.thread.id
