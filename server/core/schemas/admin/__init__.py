# mypy: disable-error-code="no-redef, assignment"
from typing import List, Union, Optional

from pydantic import Field

from core.schemas.user.enums import *
from core.schemas.common.enums import *
from .responses import *
from .enums import *


class CrawlersDataParams(CrawlersDataParams):
    origin: OriginCrawlPagesEnum


class CrawlerListParams(CrawlerListParams):
    origin: OriginCrawlPagesEnum


class PostCrawlersDataPayload(PostCrawlersDataPayload):
    origin: OriginCrawlPagesEnum


class PostCrawlersPreviewDiscordDataPayload(PostCrawlersPreviewDiscordDataPayload):
    origin: OriginCrawlPagesEnum
    preview_source: List[CrawlerDataResponseTypeEnum]


class GetCrawlersIvolunteerDataResponse(GetCrawlersIvolunteerDataResponse):
    tags: List[IvolunteerPageTagsEnum]


class GetTagsParams(GetTagsParams):
    origin: OriginCrawlPagesEnum


class PatchCrawlersDataPayload(PatchCrawlersDataPayload):
    tags: Optional[List[Union[IvolunteerPageTagsEnum, KhoahocTvPageTagsEnum]]] = Field(
        min_items=1, default=None
    )


class PatchPostPayload(PatchPostPayload):
    tags: Optional[List[Union[IvolunteerPageTagsEnum, KhoahocTvPageTagsEnum]]] = Field(
        min_items=1, default=None
    )


class GetDraftPostListResponse(GetDraftPostListResponse):
    source: OriginCrawlPagesEnum
