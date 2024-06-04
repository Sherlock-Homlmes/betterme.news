# default
from typing import Optional

# libraries
from beanie import Document, Link

# local
from core.schemas.admin import OriginCrawlPagesEnum, GetCrawlersIvolunteerDataResponse
from .posts import Posts
from .users import Users


class DraftPosts(Document):
    source: OriginCrawlPagesEnum
    name: str
    original_data: GetCrawlersIvolunteerDataResponse
    # TODO: delete this field and link to post field
    draft_data: GetCrawlersIvolunteerDataResponse
    post: Optional[Link[Posts]] = None
    deleted_by: Optional[Link[Users]] = None
