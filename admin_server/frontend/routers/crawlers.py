# TODO: Solve ignore
# mypy: disable-error-code="attr-defined"
# default
from typing import Annotated

# libraries
from fastapi import APIRouter, Depends, Request

# local
from core.conf import TemplateResponse
from core.schemas import (
    ScrapPostParams,
    ResponseStatusEnum,
)
from scrap.func import srap_post_data_find_or_create

router = APIRouter()


@router.get(
    "/crawlers/{post_name}",
    tags=["Admin-frontend-scrap"],
    status_code=ResponseStatusEnum.OK.value,
)
def get_crawl_post(
    request: Request, post_name: str, params: Annotated[dict, Depends(ScrapPostParams)]
):
    data = srap_post_data_find_or_create(origin=params.origin, post_name=post_name)
    if data is not None:
        return TemplateResponse(
            f"{params.origin.value}_post.html",
            {"request": request, "data": data.dict()},
        )
    return
