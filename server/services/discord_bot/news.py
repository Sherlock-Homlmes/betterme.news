# default

# library
import discord

# local
from .conf import server_info
from core.schemas.admin import GetCrawlersIvolunteerDataResponse, IvolunteerPageTagsEnum
from services.text_convertion import rewrite_title


# TODO:
# -> rename func
# ->.pass post description
# -> revert deadline
# -> tags
# -> button more info
map_tags = {
    IvolunteerPageTagsEnum.CLUB: 1094471174701994055,
    IvolunteerPageTagsEnum.VOLUNTEER: 1094471174701994055,
    IvolunteerPageTagsEnum.COURSE: 1094471213587374100,
    IvolunteerPageTagsEnum.SKILL: 1094471213587374100,
    IvolunteerPageTagsEnum.SCHORLARSHIP: 1094471259695366245,
    IvolunteerPageTagsEnum.EVENT: 1094471278062215218,
    IvolunteerPageTagsEnum.WORK: 1094472047217889310,
}

test_map_tags = {
    IvolunteerPageTagsEnum.CLUB: 1195438617259155486,
    IvolunteerPageTagsEnum.VOLUNTEER: 1195438617259155486,
    IvolunteerPageTagsEnum.COURSE: 1195438712864124999,
    IvolunteerPageTagsEnum.SKILL: 1195438712864124999,
    IvolunteerPageTagsEnum.SCHORLARSHIP: 1195438775153737758,
    IvolunteerPageTagsEnum.EVENT: 1195438832846389280,
    IvolunteerPageTagsEnum.WORK: 1195438889846964396,
}


async def send_news(
    data: GetCrawlersIvolunteerDataResponse,
    is_testing: bool = True,
    post_id: int = None,
) -> int:
    # TODO: refactor tags logic
    tags = (
        [test_map_tags[tag] for tag in data.tags]
        if is_testing
        else [map_tags[tag] for tag in data.tags]
    )
    applied_tags = []
    if is_testing:
        for x in server_info.test_news_channel.available_tags:
            if x.id in tags:
                applied_tags.append(x)
    else:
        for x in server_info.news_channel.available_tags:
            if x.id in tags:
                applied_tags.append(x)

    embed = discord.Embed(
        title=data.title,
        color=discord.Colour.yellow(),
        description=f"_{data.description}_",
    )
    # from yyyy-mm-dd -> dd/mm/yyy
    embed.add_field(name="Deadline", value=data.deadline.strftime("%d/%m/%Y"), inline=False)
    # TODO: post name
    if is_testing is False and post_id is not None:
        embed.add_field(
            name="Xem thêm",
            value=f"https://betterme.news/{rewrite_title(name=data.title)}_{post_id}",
            inline=False,
        )
    file = discord.File(f"scrap/data/media/{data.banner}", filename=data.banner)

    post: discord.Thread = None
    if is_testing is True:
        post = await server_info.test_news_channel.create_thread(
            name=data.title, file=file, embed=embed, applied_tags=applied_tags
        )
    else:
        post = await server_info.news_channel.create_thread(
            name=data.title, file=file, embed=embed, applied_tags=applied_tags
        )

    return post.thread.id
