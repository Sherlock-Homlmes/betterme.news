# mypy: disable-error-code="no-redef, assignment"
from .types import *
from .enums import *


class ScrapPostParams(ScrapPostParams):
    origin: OriginCrawlPagesEnum


class ScrapListPostParams(ScrapListPostParams):
    origin: OriginCrawlPagesEnum
