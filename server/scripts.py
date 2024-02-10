# This file to run pre-deploy commands
# It is typically used for tasks like running a database migration or uploading assets to a CDN.

import asyncio


# TODO
async def change_post_deadline_type_from_str_to_date():
    pass
    # post = await Posts.find_one(
    #     Not(Type(Posts.other_information.deadline, "date"))
    # )
    # print(post.id, post.title, post.other_information)
    # print(str_to_date(post.other_information.deadline))
    # await Posts.update_all({
    #     Posts.other_information.deadline:
    # })


async def main() -> None:
    # await connect_db()
    pass


if __name__ == "__main__":
    asyncio.run(main())
