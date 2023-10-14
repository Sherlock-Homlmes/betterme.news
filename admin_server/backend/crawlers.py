# TODO: Solve ignore
# mypy: disable-error-code="attr-defined"
# default
from typing import Annotated

# libraries
from fastapi import APIRouter, Depends

# local
from core.schemas import (
    # params
    CrawlersDataParams,
    # responses
    GetCrawlersDataResponse,
    PostCrawlersDataPayload,
    PatchCrawlersDataPayload,
    # enums
    ResponseStatusEnum,
)
from scrap.func import scrap_post_data

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/crawlers/{post_name}",
    tags=["Admin-backend-scrap"],
    status_code=ResponseStatusEnum.OK.value,
    response_model=GetCrawlersDataResponse,
)
def get_crawler(post_name: str, params: Annotated[dict, Depends(CrawlersDataParams)]):
    return scrap_post_data(origin=params.origin, post_name=post_name)


@router.post(
    "/crawlers",
    tags=["Admin-backend-scrap"],
    status_code=ResponseStatusEnum.CREATED.value,
)
def post_crawler(payload: PostCrawlersDataPayload):
    print("---------------", payload)
    return


@router.patch(
    "/crawlers/{post_name}",
    tags=["Admin-backend-scrap"],
    status_code=ResponseStatusEnum.CREATED.value,
)
def patch_crawler(post_name: str, payload: PatchCrawlersDataPayload):
    print(payload)
    return
