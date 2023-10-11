# TODO: Solve ignore
# mypy: disable-error-code="attr-defined"
# default
import json
import os
from typing import Annotated

# library
from fastapi import APIRouter, Depends, status, HTTPException

# local
from core.schemas import (
    ScrapPostParams,
    OriginCrawlPagesEnum,
    IvolunteerVnScrapDiscordPostResponse,
    IvolunteerVnScrapHtmlPostResponse,
    KhoahocTvScrapDiscordPostResponse,
    KhoahocTvScrapHtmlPostResponse,
    ScrapDataResponseTypeEnum,
    ScrapPostResponse,
)

router = APIRouter(
    prefix="/admin",
    responses={404: {"description": "Not found"}},
)


# TODO: These function to models
def check_if_crawl_success(origin: OriginCrawlPagesEnum, post_name: str) -> bool:
    if os.path.exists(f"scrap/data/{origin.value}/posts/{post_name}.json"):
        return True
    return False


# TODO: fix return type
def get_scrap_post_data(origin: OriginCrawlPagesEnum, post_name: str) -> dict:
    with open(
        f"scrap/data/{origin.value}/discord/{post_name}.json", encoding="utf-8"
    ) as discord_json_file:
        discord_data = json.load(discord_json_file)
    with open(
        f"scrap/data/{origin.value}/posts/{post_name}.json", encoding="utf-8"
    ) as html_json_file:
        html_data = json.load(html_json_file)

    # map return data to exact type
    data_map = {
        OriginCrawlPagesEnum.KHOAHOC_TV: {
            ScrapDataResponseTypeEnum.HTML: KhoahocTvScrapHtmlPostResponse,
            ScrapDataResponseTypeEnum.DISCORD: KhoahocTvScrapDiscordPostResponse,
        },
        OriginCrawlPagesEnum.IVOLUNTEER_VN: {
            ScrapDataResponseTypeEnum.HTML: IvolunteerVnScrapHtmlPostResponse,
            ScrapDataResponseTypeEnum.DISCORD: IvolunteerVnScrapDiscordPostResponse,
        },
    }

    return ScrapPostResponse(
        html=data_map[origin][ScrapDataResponseTypeEnum.HTML](**html_data),
        discord=data_map[origin][ScrapDataResponseTypeEnum.DISCORD](**discord_data),
    )


def scrap_post_data(origin: OriginCrawlPagesEnum, post_name: str) -> dict | None:
    # crawl post data
    os.system(f"python3 scrap/{origin.value}/__init__.py {post_name}")
    # check if
    if check_if_crawl_success(origin=origin, post_name=post_name):
        return get_scrap_post_data(origin=origin, post_name=post_name)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Not found post"
    )


@router.get(
    "crawlers/{post_name}",
    tags=["Admin-scrap"],
    status_code=201,
    response_model=ScrapPostResponse,
)
def crawl_post_content(
    post_name: str, params: Annotated[dict, Depends(ScrapPostParams)]
):
    if params.origin in OriginCrawlPagesEnum:
        return scrap_post_data(origin=params.origin, post_name=post_name)
