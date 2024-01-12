# default
from typing import Annotated, Union

# libraries
from fastapi import APIRouter, Depends

# local
from core.models import Posts
from core.schemas.admin import (
    # params
    CrawlersDataParams,
    # payload
    PostCrawlersDataPayload,
    PatchCrawlersDataPayload,
    PostCrawlersPreviewDiscordDataPayload,
    # responses
    GetCrawlersIvolunteerDataResponse,
    GetCrawlersKhoahocTvDataResponse,
    # enums
    ResponseStatusEnum,
    CrawlerDataResponseTypeEnum,
)
from scrap.func import scrap_post_data, get_scrap_post_data, save_crawler_data
from services.discord_bot.news import send_news
from services.facebook_bot.func import post_to_fb
from services.time_modules import Time

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/crawlers/{post_name}",
    tags=["Admin-backend-scrap"],
    status_code=ResponseStatusEnum.OK.value,
)
def get_crawler(
    post_name: str, params: Annotated[dict, Depends(CrawlersDataParams)]
) -> Union[GetCrawlersIvolunteerDataResponse, GetCrawlersKhoahocTvDataResponse]:
    return scrap_post_data(origin=params.origin, post_name=post_name)


@router.post(
    "/crawlers",
    tags=["Admin-backend-scrap"],
    status_code=ResponseStatusEnum.CREATED.value,
)
async def post_crawler(body: PostCrawlersDataPayload):
    current_data = get_scrap_post_data(origin=body.origin, title=body.title)
    banner = body.banner if body.banner else current_data.banner
    now = Time().now
    # TODO: fix discord data
    discord_post_id = await send_news(title=body.title, is_testing=body.is_testing)
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
    save_crawler_data(post_name=post_name, data=body)
    return


# Preview
@router.post(
    "/crawlers/{post_name}/preview",
    tags=["Admin-backend-scrap"],
    status_code=ResponseStatusEnum.CREATED.value,
)
async def post_crawler_preview(post_name: str, body: PostCrawlersPreviewDiscordDataPayload):
    current_data = get_scrap_post_data(origin=body.origin, post_name=post_name)
    if CrawlerDataResponseTypeEnum.DISCORD in body.preview_source:
        await send_news(data=current_data, is_testing=True)
    elif CrawlerDataResponseTypeEnum.FACEBOOK in body.preview_source:
        post_to_fb(
            origin=body.origin,
            content=current_data.discord.title,
            comment="test comment",
            hashtags=["hashtag1", "hashtag2"],
        )
    elif CrawlerDataResponseTypeEnum.WEB in body.preview_source:
        pass

    return
