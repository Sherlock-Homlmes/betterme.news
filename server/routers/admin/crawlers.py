# default
from typing import Annotated

# libraries
from fastapi import APIRouter, Depends

# local
from core.models import Posts
from core.schemas.admin import (
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
from services.facebook_bot.func import post_to_fb
from services.time_modules import Time

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
    current_data = get_scrap_post_data(origin=body.origin, post_name=body.post_name)
    banner = body.banner if body.banner else current_data.discord.banner
    # banner = image_process(origin=body.origin, post_name=body.post_name)
    # print("---------------after banner", banner)
    now = Time().now
    # TODO: fix discord data
    discord_post_id = await send_news(
        origin=body.origin, post_name=body.post_name, is_testing=body.is_testing
    )
    facebook_post = post_to_fb(
        origin=body.origin,
        content=current_data.discord.title,
        comment="test comment",
        hashtags=["hashtag1", "hashtag2"],
    )
    # TODO: fix html data -> fix this data
    post = Posts(
        # info
        created_at=now,
        raw_data=None,
        # other service
        facebook_post=facebook_post,
        discord_post_id=discord_post_id,
        # content
        title=current_data.discord.title,
        thumbnail_img="abc",
        banner_img=banner,
        content=current_data.html.content,
        author="Ivolunteer.vn",
        # writed_at = datetime.date(2023, 3, 24),
        # SEO
        description=current_data.html.description,
        keywords=["keyword 1", "keyword 2", "keyword 3"],
        og_img=banner,
    )
    await post.insert()

    return post.id


@router.patch(
    "/crawlers/{post_name}",
    tags=["Admin-backend-scrap"],
    status_code=ResponseStatusEnum.CREATED.value,
)
def patch_crawler(post_name: str, body: PatchCrawlersDataPayload):
    print(body)
    return
