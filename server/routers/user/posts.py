# default
from typing import List, Optional, Annotated

# libraries
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from beanie import PydanticObjectId
from beanie.operators import ElemMatch

# TODO: to error handler
from pydantic_core._pydantic_core import ValidationError

# local
from core.models import Posts
from core.schemas.user import (
    # responses
    GetPostListResponse,
    GetPostResponse,
    # payload
    GetPostListParams,
    # enums
    ResponseStatusEnum,
)
from services.beanie_odm import get_projections_from_model, return_with_pagination
from services.text_convertion import gen_slug_from_title

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
async def get_list_post(
    params: Annotated[dict, Depends(GetPostListParams)],
) -> List[GetPostListResponse]:
    queries = {}
    if params.match_tag:
        queries = ElemMatch(Posts.tags, {"$eq": params.match_tag})
    cursor = Posts.find(queries).project(PostListProject)
    posts = (
        await cursor.sort(-Posts.id)
        .skip(params.per_page * (params.page - 1))
        .limit(params.per_page)
        .to_list()
    )

    for post in posts:
        post.slug = gen_slug_from_title(post.title)

    # TODO: better pagination solution
    # model -> json
    posts = [post.model_dump() for post in posts]

    response = JSONResponse(content=posts)
    await return_with_pagination(cursor, response, params.page, params.per_page)
    return response


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
