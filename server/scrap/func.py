# default
import json
import os
from PIL import Image
from typing import Union

# libraries
from fastapi import HTTPException

# local
from core.schemas.admin import (
    # payload
    PatchCrawlersDataPayload,
    # response
    GetCrawlersKhoahocTvDataResponse,
    GetCrawlersIvolunteerDataResponse,
    # enums
    OriginCrawlPagesEnum,
    ResponseStatusEnum,
)


def check_if_crawl_success(title: str) -> bool:
    if os.path.exists(f"scrap/data/general/{title}.json"):
        return True
    return False


def get_scrap_post_data(
    origin: OriginCrawlPagesEnum, post_name: str
) -> Union[GetCrawlersIvolunteerDataResponse, GetCrawlersKhoahocTvDataResponse]:
    with open(f"scrap/data/general/{post_name}.json", encoding="utf-8") as general_json_file:
        general_data = json.load(general_json_file)

    if origin == OriginCrawlPagesEnum.IVOLUNTEER_VN:
        return GetCrawlersIvolunteerDataResponse(
            title=general_data["title"],
            banner=general_data["banner"],
            description=general_data["description"],
            deadline=general_data["deadline"],
            content=general_data["content"],
        )
    elif origin == OriginCrawlPagesEnum.KHOAHOC_TV:
        return
        # return GetCrawlersKhoahocTvDataResponse(
        #     **general_data,
        #     html=data_map[origin][CrawlerDataResponseTypeEnum.HTML](**html_data),
        #     discord=data_map[origin][CrawlerDataResponseTypeEnum.DISCORD](**discord_data),
        # )


def scrap_post_data(
    origin: OriginCrawlPagesEnum, title: str
) -> Union[GetCrawlersIvolunteerDataResponse, GetCrawlersKhoahocTvDataResponse]:
    # crawl post data
    os.system(f"python3 scrap/{origin.value}/__init__.py {title}")
    # check if
    if check_if_crawl_success(title=title):
        return get_scrap_post_data(origin=origin, title=title)
    raise HTTPException(status_code=ResponseStatusEnum.BAD_REQUEST.value, detail="Not found post")


def srap_post_data_find_or_create(
    origin: OriginCrawlPagesEnum, title: str
) -> Union[GetCrawlersIvolunteerDataResponse, GetCrawlersKhoahocTvDataResponse]:
    if check_if_crawl_success(title=title):
        return get_scrap_post_data(origin=origin, title=title)
    return scrap_post_data(origin=origin, title=title)


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
