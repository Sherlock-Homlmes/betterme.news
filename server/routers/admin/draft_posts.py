# default
from typing import List

# libraries
from fastapi import APIRouter, Depends
from beanie import PydanticObjectId

# local
from core.models import Users, DraftPosts
from core.schemas.admin import (
    # params
    # payload
    # responses
    GetDraftPostListResponse,
    # enums
    ResponseStatusEnum,
)
from routers.auth import auth_handler
from services.beanie_odm import get_projections_from_model

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


class DraftPostListProject(GetDraftPostListResponse):
    id: PydanticObjectId

    class Settings:
        projection = get_projections_from_model(
            GetDraftPostListResponse,
        )


# TODO: projection, pagination
@router.get(
    "/draft_posts",
    tags=["Admin-draft-posts"],
    status_code=ResponseStatusEnum.OK.value,
)
async def get_crawler(
    user: Users = Depends(auth_handler.auth_wrapper),
) -> List[GetDraftPostListResponse]:
    draft_posts = await DraftPosts.find(
        DraftPosts.draft_data.id == None,  # noqa: E711
        projection_model=DraftPostListProject,
    ).to_list()
    draft_posts = [draft_post.model_dump(mode="json") for draft_post in draft_posts]
    return draft_posts
