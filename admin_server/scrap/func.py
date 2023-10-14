# default
import json
import os

# libraries
from fastapi import HTTPException

# local
from core.schemas import (
    # payload
    PatchCrawlersDataPayload,
    # response
    IvolunteerDiscordPost,
    IvolunteerHtmlPost,
    KhoahocTvDiscordPost,
    KhoahocTvHtmlPost,
    GetCrawlersDataResponse,
    # enums
    CrawlerDataResponseTypeEnum,
    OriginCrawlPagesEnum,
    ResponseStatusEnum,
)


def check_if_crawl_success(origin: OriginCrawlPagesEnum, post_name: str) -> bool:
    if os.path.exists(f"scrap/data/{origin.value}/posts/{post_name}.json"):
        return True
    return False


def get_scrap_post_data(
    origin: OriginCrawlPagesEnum, post_name: str
) -> GetCrawlersDataResponse:
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
            CrawlerDataResponseTypeEnum.HTML: KhoahocTvHtmlPost,
            CrawlerDataResponseTypeEnum.DISCORD: KhoahocTvDiscordPost,
        },
        OriginCrawlPagesEnum.IVOLUNTEER_VN: {
            CrawlerDataResponseTypeEnum.HTML: IvolunteerHtmlPost,
            CrawlerDataResponseTypeEnum.DISCORD: IvolunteerDiscordPost,
        },
    }

    return GetCrawlersDataResponse(
        html=data_map[origin][CrawlerDataResponseTypeEnum.HTML](**html_data),
        discord=data_map[origin][CrawlerDataResponseTypeEnum.DISCORD](**discord_data),
    )


def scrap_post_data(
    origin: OriginCrawlPagesEnum, post_name: str
) -> GetCrawlersDataResponse:
    # crawl post data
    os.system(f"python3 scrap/{origin.value}/__init__.py {post_name}")
    # check if
    if check_if_crawl_success(origin=origin, post_name=post_name):
        return get_scrap_post_data(origin=origin, post_name=post_name)
    raise HTTPException(
        status_code=ResponseStatusEnum.BAD_REQUEST.value, detail="Not found post"
    )


def srap_post_data_find_or_create(
    origin: OriginCrawlPagesEnum, post_name: str
) -> GetCrawlersDataResponse:
    if check_if_crawl_success(origin=origin, post_name=post_name):
        return get_scrap_post_data(origin=origin, post_name=post_name)
    return scrap_post_data(origin=origin, post_name=post_name)


def save_crawler_data(payload: PatchCrawlersDataPayload) -> None:
    pass
