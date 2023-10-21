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
from scrap.func import scrap_post_data, get_scrap_post_data
from services.discord_bot.news import send_news

# from services.time_modules import Time

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
async def post_crawler(body: PostCrawlersDataPayload):
    # TODO: facebook post -> save data
    current_data = get_scrap_post_data(origin=body.origin, post_name=body.post_name)
    banner = body.banner if body.banner else current_data.discord.banner
    print("---------------title", current_data.discord.title)
    print("---------------pre banner", banner)
    print("---------------description", body.discord_description)
    print("---------------is tesing", body.is_testing)
    # banner = image_process(origin=body.origin, post_name=body.post_name)
    # print("---------------after banner", banner)
    # now = Time().now
    discord_post_id = await send_news(
        origin=body.origin, post_name=body.post_name, is_testing=body.is_testing
    )
    print(discord_post_id)

    return


@router.patch(
    "/crawlers/{post_name}",
    tags=["Admin-backend-scrap"],
    status_code=ResponseStatusEnum.CREATED.value,
)
def patch_crawler(post_name: str, body: PatchCrawlersDataPayload):
    print(body)
    return
