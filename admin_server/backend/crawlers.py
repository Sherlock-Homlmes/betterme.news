# TODO: Solve ignore
# mypy: disable-error-code="attr-defined"
# default
from typing import Annotated

# library
from fastapi import APIRouter, Depends

# local
from core.schemas import (
    ScrapPostParams,
    OriginCrawlPagesEnum,
    ScrapPostResponse,
    ResponseStatusEnum,
)
from scrap.func import scrap_post_data

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get(
    "crawlers/{post_name}",
    tags=["Admin-backend-scrap"],
    status_code=ResponseStatusEnum.OK.value,
    response_model=ScrapPostResponse,
)
def crawl_post_content(
    post_name: str, params: Annotated[dict, Depends(ScrapPostParams)]
):
    if params.origin in OriginCrawlPagesEnum:
        return scrap_post_data(origin=params.origin, post_name=post_name)
