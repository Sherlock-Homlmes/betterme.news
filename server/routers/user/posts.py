# default
from typing import List, Annotated, Optional

# libraries
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from beanie import PydanticObjectId
from beanie.operators import ElemMatch

# TODO: to error handler

# local
from core.models import Posts
from core.schemas.user import (
    # responses
    GetPostListResponse,
    GetPostResponse,
    # payload
    GetPostListParams,
    GetPostParams,
    # enums
    ResponseStatusEnum,
)
from services.beanie_odm import get_projections_from_model, return_with_pagination
from services.text_convertion import gen_slug_from_title

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


class PostListProject(GetPostListResponse):
    id: PydanticObjectId
    slug: Optional[str] = ""

    class Settings:
        projection = get_projections_from_model(
            GetPostListResponse,
            exclude_fields=["slug"],
            map_fields={
                "deadline": "other_information.deadline",
            },
        )


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
    # TODO: refactor change to class method
    cursor = Posts.find(queries, projection_model=PostListProject)
    posts = (
        await cursor.sort(-Posts.id)
        .skip(params.per_page * (params.page - 1))
        .limit(params.per_page)
        .to_list()
    )

    for post in posts:
        post.slug = gen_slug_from_title(post.title)

    # model -> json
    posts = [post.model_dump(mode="json") for post in posts]

    # TODO: better pagination solution
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
    params: Annotated[dict, Depends(GetPostParams)],
    background_tasks: BackgroundTasks,
) -> GetPostResponse:
    post_id: str = post_name.split("_")[-1]
    try:
        post = await Posts.get(post_id)
        if params.increase_view:
            background_tasks.add_task(post.increase_view)
        return post
    except AttributeError:
        raise HTTPException(
            status_code=ResponseStatusEnum.NOT_FOUND.value,
            detail="Post not found",
        )
