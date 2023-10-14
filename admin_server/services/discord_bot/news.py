# default
import json

# library
import discord

# local
from services.discord_bot.conf import server_info


async def send_news(origin: str, post_name: str, is_testing: bool = True):
    for tag in server_info.news_channel.available_tags:
        print(tag)

    # open json file to get data
    try:
        with open(
            f"scrap/data/{origin}/discord/{post_name}.json", encoding="utf-8"
        ) as json_file:
            data = json.load(json_file)
    except Exception as e:
        raise e
    embed = discord.Embed(
        title=data["title"],
        color=discord.Colour.yellow(),
        description=data["description"],
    )
    embed.add_field(name="DEADLINE", value=data["deadline"], inline=False)

    is_end_description = False
    for index, cont in enumerate(data["content"]):
        if type(cont) == list:
            field_content = ""
            for li in cont:
                field_content += f"- {li}\n"
            embed.add_field(name="", value=field_content, inline=False)
        elif "**" in cont:
            # try:
            #     if type(data["content"][index+1]) == list:
            #         field_content = ""
            #         for li in data["content"][index+1]:
            #             field_content += f"- {li}\n"
            #         embed.add_field(name=cont, value=field_content, inline=False)
            #     elif type(data["content"][index+1]) == str:
            #         embed.add_field(name=cont, value="", inline=False)
            # except IndexError:
            embed.add_field(name=cont, value="", inline=False)
            is_end_description = True
        elif is_end_description is False:
            embed.description += f"\n{cont}"

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
    print(post)

    return {"message": "Success"}
