# default

# libraries
from fastapi import APIRouter, HTTPException

# local
from core.models import Posts
from core.schemas.admin import (
    # params
    # payload
    # responses
    # enums
    ResponseStatusEnum,
)
from services.tebi import delete_image
from services.discord_bot.news import delete_news


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.delete(
    "/posts/{post_id}",
    tags=["Admin-backend-scrap"],
    status_code=ResponseStatusEnum.NO_CONTENT.value,
)
async def get_crawler(post_id: str) -> None:
    post = await Posts.get(post_id)
    if not post:
        raise HTTPException(
            status_code=ResponseStatusEnum.NOT_FOUND.value,
            detail="Post not found",
        )

    if post.discord_post_id:
        await delete_news(post.discord_post_id)
    if post.banner_img:
        delete_image(post.banner_img)
    if post.thumbnail_img:
        delete_image(post.thumbnail_img)
    await post.delete()

    return
