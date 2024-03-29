# default
import asyncio
from typing import Union

# lib
import discord
from bson.int64 import Int64


async def get_channel(guild: discord.Guild, channel_ids: Union[int, Int64, list]):
    if isinstance(channel_ids, (int, Int64)):
        return await guild.fetch_channel(channel_ids)
    elif isinstance(channel_ids, list):
        return await asyncio.gather(*[get_channel(guild, channel_id) for channel_id in channel_ids])
