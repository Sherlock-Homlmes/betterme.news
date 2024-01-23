# default
from typing import List

# libraries
from fastapi import APIRouter

# local
from core.models import Posts
from core.schemas.user import (
    # responses
    GetPostListResponse,
    GetPostResponse,
    # enums
    ResponseStatusEnum,
)

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/posts",
    tags=["Post"],
    status_code=ResponseStatusEnum.OK.value,
)
async def get_list_post(page: int, per_page: int) -> List[GetPostListResponse]:
    posts = await Posts.find().skip(page - 1).limit(per_page).to_list()
    # TODO: change model of post id
    for post in posts:
        post.id = str(post.id)
    return posts


@router.get(
    "/posts/{post_name}",
    tags=["Post"],
    status_code=ResponseStatusEnum.OK.value,
)
async def get_post(
    post_name: str,
) -> GetPostResponse:
    post_id: str = post_name.split("_")[-1]
    post = await Posts.get(post_id)
    return post
