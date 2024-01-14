# default
from typing import Annotated, Union

# libraries
from fastapi import APIRouter, Depends

# local
from core.models import Posts, OtherPostInfo
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
    PostCrawlersResponse,
    # enums
    OriginCrawlPagesEnum,
    ResponseStatusEnum,
    CrawlerDataResponseTypeEnum,
)
from scrap.func import scrap_post_data, get_scrap_post_data, save_crawler_data
from services.discord_bot.news import send_news
from services.facebook_bot.func import post_to_fb
from services.tebi import upload_image
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
    status_code=ResponseStatusEnum.OK.value,
)
async def post_crawler(body: PostCrawlersDataPayload):
    current_data = get_scrap_post_data(origin=body.origin, post_name=body.post_name)
    banner_img = None
    if current_data.banner is not None:
        banner_img = upload_image(current_data.banner)
    # all_fields = current_data.__fields__.keys()
    # thumbnail_img = None
    # if "thumbnail" in all_fields and current_data.thumbnail is not None:
    #     thumbnail_img = upload_image(current_data.thumbnail)
    now = Time().now
    # facebook_post = post_to_fb(
    #     origin=body.origin,
    #     content=current_data.discord.title,
    #     comment="test comment",
    #     hashtags=["hashtag1", "hashtag2"],
    # )
    # TODO: fix html data -> fix this data
    if body.origin == OriginCrawlPagesEnum.IVOLUNTEER_VN:
        post = Posts(
            # info
            created_at=now,
            raw_data=None,
            # other service
            # facebook_post=facebook_post,
            discord_post_id=0,
            # content
            title=current_data.title,
            description=current_data.description,
            other_information=OtherPostInfo(deadline=current_data.deadline),
            banner_img=banner_img,
            content=current_data.content,
            author="Ivolunteer.vn",
            # SEO
            keywords=["keyword 1", "keyword 2", "keyword 3"],
            og_img=banner_img,
        )
    else:
        pass
    await post.insert()
    # create discord post
    discord_post_id = await send_news(data=current_data, is_testing=False, post_id=post.id)
    post.discord_post_id = discord_post_id
    await post.save()
    return PostCrawlersResponse(id=str(post.id))


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
    "/crawlers/{post_name}/_preview",
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
