# default
from typing import Optional

# libraries
from beanie import Document, Link

# local
from core.schemas.admin import OriginCrawlPagesEnum, GetCrawlersIvolunteerDataResponse
from .posts import Posts


class DraftPosts(Document):
    source: OriginCrawlPagesEnum
    name: str
    original_data: GetCrawlersIvolunteerDataResponse
    draft_data: GetCrawlersIvolunteerDataResponse
    post: Optional[Link[Posts]] = None
