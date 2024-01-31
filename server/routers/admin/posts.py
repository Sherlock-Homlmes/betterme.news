# default

# libraries
from fastapi import APIRouter, HTTPException, Depends

# local
from core.models import Posts, Users
from core.schemas.admin import (
    # params
    # payload
    PatchPostPayload,
    # responses
    # enums
    ResponseStatusEnum,
)
from routers.auth import auth_handler
from services.tebi import delete_image
from services.discord_bot.news import delete_news


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.patch(
    "/posts/{post_id}",
    tags=["Admin-posts"],
    status_code=ResponseStatusEnum.NO_CONTENT.value,
)
async def get_post(
    post_id: str, payload: PatchPostPayload, user: Users = Depends(auth_handler.auth_wrapper)
):
    try:
        post = await Posts.get(post_id)
    except Exception:
        raise HTTPException(
            status_code=ResponseStatusEnum.NOT_FOUND.value,
            detail="Post not found",
        )
    # TODO: refactor this
    update_fields = {}
    for key, value in payload.model_dump().items():
        if value is not None:
            update_fields[key] = value

    await post.update({"$set": update_fields})

    return


@router.delete(
    "/posts/{post_id}",
    tags=["Admin-posts"],
    status_code=ResponseStatusEnum.NO_CONTENT.value,
)
async def get_crawler(post_id: str, user: Users = Depends(auth_handler.auth_wrapper)) -> None:
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
