# default
from typing import List, Optional

# libraries
from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId

# TODO: to error handler
from pydantic_core._pydantic_core import ValidationError

# local
from core.models import Posts
from core.schemas.user import (
    # responses
    GetPostListResponse,
    GetPostResponse,
    # enums
    ResponseStatusEnum,
)
from services.beanie_odm import get_projections_from_model
from services.text_convertion import rewrite_title

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


class PostListProject(GetPostListResponse):
    id: Optional[PydanticObjectId] = None
    slug: Optional[str] = None

    class Settings:
        projection = get_projections_from_model(GetPostListResponse, exclude_fields=["slug"])


@router.get(
    "/posts",
    tags=["Post"],
    status_code=ResponseStatusEnum.OK.value,
)
async def get_list_post(page: int, per_page: int) -> List[GetPostListResponse]:
    posts = (
        await Posts.find()
        .project(PostListProject)
        .sort(-Posts.id)
        .skip(page - 1)
        .limit(per_page)
        .to_list()
    )

    # TODO: refactor this
    for post in posts:
        post.id = str(post.id)
        post.slug = rewrite_title(post.title)

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
    try:
        post = await Posts.get(post_id)
        return post
    except ValidationError:
        raise HTTPException(
            status_code=ResponseStatusEnum.BAD_REQUEST.value,
            detail="Post not found",
        )
