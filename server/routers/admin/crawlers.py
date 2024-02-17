# default
from typing import Annotated, Union, List

# libraries
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

# local
from core.models import Posts, OtherPostInfo, Users, DraftPosts
from core.schemas.admin import (
    # params
    CrawlersDataParams,
    CrawlersListDataParams,
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
from routers.auth import auth_handler
from scrap.func import scrap_post_data, scrap_page_data
from services.discord_bot.news import send_news
from services.facebook_bot.func import post_to_fb
from services.tebi import upload_image
from services.time_modules import Time, date_to_str

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


class DraftPostNameProjection(BaseModel):
    name: str


@router.get(
    "/crawlers",
    tags=["Admin-backend-scrap"],
    status_code=ResponseStatusEnum.OK.value,
)
async def get_crawler_list(
    params: Annotated[dict, Depends(CrawlersListDataParams)],
) -> List[str]:
    # crawler
    page_data = scrap_page_data(params)
    # get exist crawler
    draft_posts = await DraftPosts.find().project(DraftPostNameProjection).to_list()
    draft_post_names = [x.name for x in draft_posts]
    # exclude exist crawler from return data
    page_data = [x for x in page_data if x not in draft_post_names]
    return page_data


@router.get(
    "/crawlers/{post_name}",
    tags=["Admin-backend-scrap"],
    status_code=ResponseStatusEnum.OK.value,
)
async def get_crawler(
    post_name: str,
    params: Annotated[dict, Depends(CrawlersDataParams)],
) -> Union[GetCrawlersIvolunteerDataResponse, GetCrawlersKhoahocTvDataResponse]:
    post_data = scrap_post_data(origin=params.origin, post_name=post_name)
    if post_data.deadline:
        post_data.deadline = post_data.deadline.strftime("%Y-%m-%d")
    await DraftPosts(
        source=params.origin,
        name=post_name,
        original_data=post_data,
        draft_data=post_data,
    ).insert()
    return post_data


# TODO: to /posts api
@router.post(
    "/crawlers",
    tags=["Admin-backend-scrap"],
    status_code=ResponseStatusEnum.OK.value,
)
async def post_crawler(
    body: PostCrawlersDataPayload, user: Users = Depends(auth_handler.auth_wrapper)
):
    draft_post_data = await DraftPosts.find_one(
        DraftPosts.name == body.post_name,
        DraftPosts.source == body.origin,
    )
    if not draft_post_data:
        raise HTTPException(
            status_code=ResponseStatusEnum.BAD_REQUEST.value, detail="Not found post"
        )
    elif draft_post_data.draft_data.id:
        raise HTTPException(
            status_code=ResponseStatusEnum.BAD_REQUEST.value, detail="Post already exist"
        )
    current_data = draft_post_data.draft_data
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
        # TODO: remove date_to_str when lib support
        other_info = OtherPostInfo()
        other_info.deadline = date_to_str(current_data.deadline) if current_data.deadline else None
        post = Posts(
            # info
            created_at=now,
            created_by=await Users.get(user["id"]),
            raw_data=None,
            # other service
            # facebook_post=facebook_post,
            discord_post_id=0,
            # content
            title=current_data.title,
            description=current_data.description,
            tags=current_data.tags,
            other_information=other_info,
            banner_img=banner_img,
            content=current_data.content,
            author="Ivolunteer.vn",
            # SEO
            keywords=current_data.keywords,
            og_img=banner_img,
        )
    else:
        pass
    await post.insert()
    # create discord post
    discord_post_id = await send_news(data=current_data, is_testing=False, post_id=post.id)
    #
    post.discord_post_id = discord_post_id
    await post.save()
    #
    await draft_post_data.set({DraftPosts.draft_data.id: str(post.id)})
    return PostCrawlersResponse(id=str(post.id))


# TODO: to /draftposts api
@router.patch(
    "/crawlers/{post_name}",
    tags=["Admin-backend-scrap"],
    status_code=ResponseStatusEnum.NO_CONTENT.value,
)
async def patch_crawler(
    post_name: str,
    body: PatchCrawlersDataPayload,
):
    draft_post_data = await DraftPosts.find_one(
        DraftPosts.name == post_name,
        # TODO: add this condition(low priority)
        # DraftPosts.source == body.origin,
    )
    if not draft_post_data:
        raise HTTPException(
            status_code=ResponseStatusEnum.BAD_REQUEST.value, detail="Not found post"
        )
    original_update_fields = body.model_dump(mode="json", exclude_unset=True)
    # TODO: refactor this
    update_fields = {}
    for key, value in original_update_fields.items():
        update_fields[f"draft_data.{key}"] = value

    await draft_post_data.set(update_fields)
    return


# Preview
@router.post(
    "/crawlers/{post_name}/_preview",
    tags=["Admin-backend-scrap"],
    status_code=ResponseStatusEnum.CREATED.value,
)
async def post_crawler_preview(
    post_name: str,
    body: PostCrawlersPreviewDiscordDataPayload,
    user: Users = Depends(auth_handler.auth_wrapper),
):
    draft_post_data = await DraftPosts.find_one(DraftPosts.name == post_name)
    # TODO: refactor raise error
    if not draft_post_data:
        raise HTTPException(
            status_code=ResponseStatusEnum.BAD_REQUEST.value, detail="Not found post"
        )
    current_data = draft_post_data.draft_data
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


# import os
# def abc():
#     # To check server restart or not
#     directory_path = "scrap/data/post"
#     contents = os.listdir(directory_path)
#     is_server_restarted = len(contents) == 1

#     if params.use_cache or not is_server_restarted:
#         draft_post_data = await DraftPosts.find_one(
#             DraftPosts.name == post_name,
#             DraftPosts.source == params.origin,
#         )
#         if draft_post_data:
#             return draft_post_data.draft_data
