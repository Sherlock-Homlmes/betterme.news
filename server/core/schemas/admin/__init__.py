# mypy: disable-error-code="no-redef, assignment"
from typing import List
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
