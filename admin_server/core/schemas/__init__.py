# mypy: disable-error-code="no-redef, assignment"
from .responses import *
from .enums import *


class CrawlersDataParams(CrawlersDataParams):
    origin: OriginCrawlPagesEnum


class CrawlerListParams(CrawlerListParams):
    origin: OriginCrawlPagesEnum


class PostCrawlersDataPayload(PostCrawlersDataPayload):
    origin: OriginCrawlPagesEnum


class PatchCrawlersDataPayload(PatchCrawlersDataPayload):
    origin: OriginCrawlPagesEnum
