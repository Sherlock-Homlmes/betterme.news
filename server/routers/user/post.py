# default

# libraries
from fastapi import APIRouter

# local
from core.models import Posts
from core.schemas.user import (
    # responses
    GetPostResponse,
    # enums
    ResponseStatusEnum,
)

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


# @router.get(
#     "/posts",
#     tags=["Post"],
#     status_code=ResponseStatusEnum.OK.value,
# )
# async def get_post(
#     post_name: str,
# ) -> GetPostResponse:
#     post_id = post_name.split("_")[-1]
#     post = await Posts.get(post_id)
#     print(post)
#     return post


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
