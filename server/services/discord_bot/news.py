# default

# library
import discord

# local
from .conf import server_info
from core.conf import settings, ENVEnum
from core.schemas.admin import GetCrawlersIvolunteerDataResponse, IvolunteerPageTagsEnum
from services.text_convertion import gen_slug_from_title


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
    # IvolunteerPageTagsEnum.SKILL: 1094471213587374100,
    IvolunteerPageTagsEnum.SCHORLARSHIP: 1094471259695366245,
    IvolunteerPageTagsEnum.EVENT: 1094471278062215218,
}

test_map_tags = {
    IvolunteerPageTagsEnum.CLUB: 1195438617259155486,
    IvolunteerPageTagsEnum.VOLUNTEER: 1195438617259155486,
    IvolunteerPageTagsEnum.COURSE: 1195438712864124999,
    # IvolunteerPageTagsEnum.SKILL: 1195438712864124999,
    IvolunteerPageTagsEnum.SCHORLARSHIP: 1195438775153737758,
    IvolunteerPageTagsEnum.EVENT: 1195438832846389280,
}

map_tag_reactions = {
    IvolunteerPageTagsEnum.CLUB: "💛",
    IvolunteerPageTagsEnum.VOLUNTEER: "💛",
    IvolunteerPageTagsEnum.COURSE: "💚",
    IvolunteerPageTagsEnum.SCHORLARSHIP: "💙",
    IvolunteerPageTagsEnum.EVENT: "💜",
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
    avaiable_tags = (
        server_info.test_news_channel.available_tags
        if is_testing
        else server_info.news_channel.available_tags
    )
    applied_tags = [x for x in avaiable_tags if x.id in tags]

    embed = discord.Embed(
        title=data.title,
        color=discord.Colour.yellow(),
        description=f"_{data.description}_",
    )
    # from yyyy-mm-dd -> dd/mm/yyy
    deadline = "ASAP" if data.deadline is None else data.deadline.strftime("%d/%m/%Y")
    embed.add_field(name="Deadline", value=deadline, inline=False)

    # TODO: post name
    if is_testing is False and post_id is not None:
        embed.add_field(
            name="Xem thêm",
            value=f"https://betterme.news/posts/{gen_slug_from_title(name=data.title)}_{post_id}",
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
        # add emoji reaction
        await post.message.add_reaction("❤️")
        if settings.ENV == ENVEnum.ADMIN.value:
            await send_noti_to_subcribers(data, embed)

    return post.thread.id


async def delete_news(
    post_id: int,
) -> None:
    try:
        post = await server_info.guild.fetch_channel(post_id)
        await post.delete()
    except discord.errors.NotFound:
        print("Thread not exist")


async def send_noti_to_subcribers(data, embed):
    tags = data.tags
    file = discord.File(f"scrap/data/media/{data.banner}", filename=data.banner)

    channel = await server_info.guild.fetch_channel(891909866355048548)
    message = await channel.fetch_message(1206679624059199520)
    noti_users = []
    for reaction in message.reactions:
        noti_users.extend(
            [
                user
                async for user in reaction.users()
                for tag in tags
                if map_tag_reactions[tag] == reaction.emoji and not user.bot
            ]
        )

    # TODO: refactor this for handle large amount of users
    for user in noti_users:
        try:
            await user.send(embed=embed, file=file, content=f"<@{user.id}>")
        except discord.errors.HTTPException:
            pass
