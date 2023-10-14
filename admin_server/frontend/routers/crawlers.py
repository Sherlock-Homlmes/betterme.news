# TODO: Solve ignore
# mypy: disable-error-code="attr-defined"
# default
from typing import Annotated

# libraries
from fastapi import APIRouter, Depends, Request

# local
from core.conf import TemplateResponse
from core.schemas import (
    CrawlersDataParams,
    ResponseStatusEnum,
)
from scrap.func import srap_post_data_find_or_create

router = APIRouter()


@router.get(
    "/crawlers/{post_name}",
    tags=["Admin-frontend-scrap"],
    status_code=ResponseStatusEnum.OK.value,
)
def get_crawler_fe(
    request: Request,
    post_name: str,
    params: Annotated[dict, Depends(CrawlersDataParams)],
):
    data = srap_post_data_find_or_create(origin=params.origin, post_name=post_name)
    return TemplateResponse(
        f"{params.origin.value}_post.html",
        {
            "request": request,
            "origin": params.origin.value,
            "post_name": post_name,
            "data": data.dict(),
        },
    )
