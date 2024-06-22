# default
import datetime
from typing import Optional, List, Union, Any, Tuple


# libraries
from beanie import Document, Link
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

# locals
from core.conf import settings, ENVEnum
from .users import Users
from core.schemas.admin import ResponseStatusEnum


class FacebookPostInfo(BaseModel):
    post_id: str
    comment_id: str


class OtherPostInfo(BaseModel):
    # TODO: remove str type when lib support get date in projection
    deadline: Optional[Union[datetime.date, str, None]] = None


# TODO: after create process: change title, insert to search engine, caching
class Posts(Document):
    # info
    created_at: datetime.datetime
    # TODO: remove optional and None
    created_by: Optional[Link[Users]] = None
    updated_at: Optional[datetime.datetime] = None
    updated_by: Optional[Link[Users]] = None

    # other service
    facebook_post: Optional[FacebookPostInfo] = None
    discord_post_id: int

    # content
    title: str
    description: str
    thumbnail_img: Optional[str] = None
    banner_img: Optional[str] = None
    content: str
    author: str
    author_link: Optional[str] = None
    # TODO: convert this to primary fields
    other_information: Optional[OtherPostInfo] = None
    view: Optional[int] = Field(default=1, gt=0)
    tags: Optional[List[str]] = []

    # SEO
    keywords: List[str]
    og_img: str

    class Settings:
        validate_on_save = True
        # only use cache in user api
        use_cache = True if settings.ENV == ENVEnum.USER.value else False
        cache_expiration_time = datetime.timedelta(seconds=30)
        cache_capacity = 100

    ### Validate
    # TODO: check if working or not
    @field_validator("thumbnail_img")
    @classmethod
    def validate_thumbnail_banner(cls, thumbnail_img: str) -> int:
        if thumbnail_img or cls.banner_img:
            return thumbnail_img
        raise HTTPException(
            status_code=ResponseStatusEnum.BAD_REQUEST.value,
            detail="Thumbnail or banner must be exist",
        )

    # TODO: make this as general model
    @classmethod
    def build_query(self, params: BaseModel) -> Tuple[List[Any]]:
        find_queries = {}
        agg_queries = []
        if isinstance(params, BaseModel):
            param_fields = params.__fields__.keys()
            for pfield in param_fields:
                if pfield == "match_search" and params.match_search is not None:
                    agg_queries.insert(
                        0,
                        {
                            "$search": {
                                "index": "SearchNews",
                                "text": {"query": params.match_search, "path": {"wildcard": "*"}},
                            }
                        },
                    )
                elif pfield.startswith("match_"):
                    match_values = getattr(params, pfield)
                    if match_values:
                        # TODO: fix this
                        # if len(values := match_values.split(",")) > 1:
                        find_queries[pfield.replace("match_", "")] = {
                            "$elemMatch": {"$in": match_values.split(",")}
                        }
                        # else:
                        #     agg_queries.append({pfield.replace("match_", ""): match_values})
        return find_queries, agg_queries

    ### Method
    async def increase_view(self):
        self.view += 1
        await self.save()

    ### Event
    # TODO: social posts to this func
    async def after_create(self):
        pass
