# default
import json
import os
from PIL import Image

# libraries
from fastapi import HTTPException

# local
from core.schemas.admin import (
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


def check_if_crawl_success(post_name: str) -> bool:
    if os.path.exists(f"scrap/data/web/{post_name}.json"):
        return True
    return False


def get_scrap_post_data(origin: OriginCrawlPagesEnum, post_name: str) -> GetCrawlersDataResponse:
    with open(f"scrap/data/discord/{post_name}.json", encoding="utf-8") as discord_json_file:
        discord_data = json.load(discord_json_file)
    with open(f"scrap/data/web/{post_name}.json", encoding="utf-8") as html_json_file:
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


def scrap_post_data(origin: OriginCrawlPagesEnum, post_name: str) -> GetCrawlersDataResponse:
    # crawl post data
    os.system(f"python3 scrap/{origin.value}/__init__.py {post_name}")
    # check if
    if check_if_crawl_success(post_name=post_name):
        return get_scrap_post_data(origin=origin, post_name=post_name)
    raise HTTPException(status_code=ResponseStatusEnum.BAD_REQUEST.value, detail="Not found post")


def srap_post_data_find_or_create(
    origin: OriginCrawlPagesEnum, post_name: str
) -> GetCrawlersDataResponse:
    if check_if_crawl_success(post_name=post_name):
        return get_scrap_post_data(origin=origin, post_name=post_name)
    return scrap_post_data(origin=origin, post_name=post_name)


def save_crawler_data(payload: PatchCrawlersDataPayload) -> None:
    pass


def image_process(origin: OriginCrawlPagesEnum, image: str) -> None:
    # Opens a image
    if origin == OriginCrawlPagesEnum.IVOLUNTEER_VN:
        frame_img = Image.open("scrap/media/betterme_news_ivolunteer.png")
    else:
        frame_img = Image.open("scrap/media/betterme_news.png")
    img = Image.open(f"scrap/data/{origin.value}/media/{image}")

    # Add foreground
    img.paste(frame_img, (0, 0), frame_img)

    # Save the image
    img.save(f"scrap/data/{origin.value}/media/{image}")
