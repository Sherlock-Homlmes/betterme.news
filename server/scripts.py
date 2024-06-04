# This file is to run pre-deploy commands
# Typically used for tasks like running a database migration or uploading assets to a CDN.

import asyncio
from core.models import Posts, DraftPosts
from core.event_handler import connect_db
from beanie import PydanticObjectId
from beanie.operators import Exists


async def something():
    draft_posts = await DraftPosts.find(
        DraftPosts.draft_data.id != None, fetch_links=True
    ).to_list()
    original_post_data = [
        {
            "draft_post_id": draft_post.id,
            "post_id": draft_post.draft_data.id,
            "original_link": draft_post.name,
        }
        for draft_post in draft_posts
    ]

    for x in original_post_data:
        await Posts.find_one(Posts.id == PydanticObjectId(x["post_id"])).update(
            {"$set": {Posts.author_link: x["original_link"]}}
        )
    await Posts.find(Exists(Posts.author_link, False)).update({"$set": {Posts.author_link: None}})


async def main() -> None:
    await connect_db()
    await something()
    pass


if __name__ == "__main__":
    asyncio.run(main())
