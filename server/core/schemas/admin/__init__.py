# mypy: disable-error-code="no-redef, assignment"
from typing import List, Union, Optional

from core.schemas.common import *
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
    tags: Optional[List[Union[IvolunteerPageTagsEnum, KhoahocTvPageTagsEnum]]]
