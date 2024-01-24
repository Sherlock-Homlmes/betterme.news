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
from services.text_convertion import rewrite_title

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/posts",
    tags=["Post"],
    status_code=ResponseStatusEnum.OK.value,
)
async def get_list_post(page: int, per_page: int) -> List[GetPostListResponse]:
    # TODO: add projection
    posts = await Posts.find().sort(-Posts.id).skip(page - 1).limit(per_page).to_list()

    # TODO: refactor this
    results = []
    for post in posts:
        result = post.dict()
        result["id"] = str(result["id"])
        result["slug"] = rewrite_title(result["title"])
        results.append(result)

    return results


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
