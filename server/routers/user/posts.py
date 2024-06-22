# default
from typing import List, Annotated, Optional

# libraries
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import ORJSONResponse
from beanie import PydanticObjectId
from beanie.operators import ElemMatch
from pydantic_core._pydantic_core import ValidationError
from pydantic import model_validator

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
from utils.beanie_odm import get_projections_from_model, return_with_pagination
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

    @model_validator(mode="after")
    def gen_slug_from_title(cls, values):
        if not len(values.slug) and values.title:
            values.slug = gen_slug_from_title(values.title)
        return values


@router.get(
    "/posts",
    tags=["Post"],
    status_code=ResponseStatusEnum.OK.value,
)
async def get_list_post(
    params: Annotated[dict, Depends(GetPostListParams)],
) -> List[GetPostListResponse]:
    queries = {}
    # TODO: better match filter
    if params.match_tag:
        match_tags = params.match_tag.split(",")
        queries = ElemMatch(Posts.tags, {"$in": match_tags})
    # TODO: refactor change to class method
    cursor = Posts.find(queries, projection_model=PostListProject)
    posts = (
        await cursor.sort(-Posts.id)
        .skip(params.per_page * (params.page - 1))
        .limit(params.per_page)
        .to_list()
    )

    # model -> json
    posts = [post.model_dump(mode="json") for post in posts]

    # TODO: better pagination solution
    response = ORJSONResponse(content=posts)
    await return_with_pagination(cursor, response, params.page, params.per_page)
    return response


@router.get(
    "/posts/_search",
    tags=["Post"],
    status_code=ResponseStatusEnum.OK.value,
)
async def get_list_post_search(match_keyword: str):
    posts = (
        await Posts.find(
            {},
            projection_model=PostListProject,
        )
        .aggregate(
            [
                {
                    "$search": {
                        "index": "SearchNews",
                        "text": {"query": match_keyword, "path": {"wildcard": "*"}},
                    }
                },
                {"$skip": 0},
                {"$limit": 10},
                {"$sort": {"_id": -1}},
            ],
            projection_model=PostListProject,
        )
        .to_list()
    )
    return posts


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
    # TODO: remove this to get only by id
    post_id: str = post_name.split("_")[-1]
    try:
        post = await Posts.get(post_id)
        post.id = str(post.id)
        if params.increase_view:
            background_tasks.add_task(post.increase_view)
        return post
    except (AttributeError, ValidationError):
        raise HTTPException(
            status_code=ResponseStatusEnum.NOT_FOUND.value,
            detail="Post not found",
        )


@router.get(
    "/posts/{post_name}/_related",
    tags=["Post"],
    status_code=ResponseStatusEnum.OK.value,
)
async def get_related_post(
    post_name: str,
) -> List[GetPostListResponse]:
    post_id: str = post_name.split("_")[-1]
    try:
        post = await Posts.get(post_id)
        # TODO: only get not expired posts(when lib support datetime.date)
        posts = await (
            Posts
            # find post that have same tags
            .find(ElemMatch(Posts.tags, {"$in": post.tags}))
            .aggregate([{"$sample": {"size": 3}}], projection_model=PostListProject)
            .to_list()
        )
        return [post.model_dump(mode="json") for post in posts]
    except (AttributeError, ValidationError):
        raise HTTPException(
            status_code=ResponseStatusEnum.NOT_FOUND.value,
            detail="Post not found",
        )
