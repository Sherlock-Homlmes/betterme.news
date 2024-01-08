# default
import json

# library
import discord

# local
from core.schemas.admin import OriginCrawlPagesEnum
from .conf import server_info


# TODO:
# -> rename func
# ->.pass post description
# -> revert deadline
# -> tags
# -> button more info
async def send_news(
    origin: OriginCrawlPagesEnum, post_name: str, is_testing: bool = True
) -> int:
    # for tag in server_info.news_channel.available_tags:
    #     print(tag)

    # open json file to get data
    try:
        with open(
            f"scrap/data/{origin.value}/discord/{post_name}.json", encoding="utf-8"
        ) as json_file:
            data = json.load(json_file)
    except Exception as e:
        raise e
    embed = discord.Embed(
        title=data["title"],
        color=discord.Colour.yellow(),
        description=data["description"],
    )
    embed.add_field(name="Deadline", value=data["deadline"], inline=False)
    embed.add_field(
        name="More info", value=f"https://betterme.news/{post_name}", inline=False
    )

    post: discord.Thread = None
    if is_testing is True:
        post = await server_info.test_news_channel.create_thread(
            name=data["title"],
            # file=data["banner"],
            embed=embed,
        )
    else:
        post = await server_info.news_channel.create_thread(
            name=data["title"],
            # file=data["banner"],
            embed=embed,
        )

    return post.thread.id
