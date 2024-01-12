# default
import json
import os
import io
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


def check_if_crawl_success(post_name: str) -> bool:
    if os.path.exists(f"scrap/data/general/{post_name}.json"):
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
    origin: OriginCrawlPagesEnum, post_name: str
) -> Union[GetCrawlersIvolunteerDataResponse, GetCrawlersKhoahocTvDataResponse]:
    # crawl post data
    os.system(f"python3 scrap/{origin.value}/__init__.py {post_name}")
    # check if
    if check_if_crawl_success(post_name=post_name):
        return get_scrap_post_data(origin=origin, post_name=post_name)
    raise HTTPException(status_code=ResponseStatusEnum.BAD_REQUEST.value, detail="Not found post")


def srap_post_data_find_or_create(
    origin: OriginCrawlPagesEnum, post_name: str
) -> Union[GetCrawlersIvolunteerDataResponse, GetCrawlersKhoahocTvDataResponse]:
    if check_if_crawl_success(post_name=post_name):
        return get_scrap_post_data(origin=origin, post_name=post_name)
    return scrap_post_data(origin=origin, post_name=post_name)


def save_crawler_data(post_name: str, data: PatchCrawlersDataPayload) -> None:
    if check_if_crawl_success(post_name=post_name):
        # open file to get old data
        with open(f"scrap/data/general/{post_name}.json", encoding="utf-8") as general_json_file:
            general_data = json.load(general_json_file)

        # update if key match
        update_data = data.dict()
        for key, value in update_data.items():
            name = general_data.get(key, None) if value is not None else None
            if name:
                general_data[key] = update_data[key]

        # write to js file
        with io.open(
            f"scrap/data/general/{post_name}.json", "w", encoding="utf8"
        ) as html_json_file:
            json.dump(general_data, html_json_file, ensure_ascii=False, indent=4)

    else:
        raise HTTPException(
            status_code=ResponseStatusEnum.BAD_REQUEST.value, detail="Not found post"
        )


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
