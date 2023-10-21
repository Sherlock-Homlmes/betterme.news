# default
import datetime
from typing import Optional, List

# libraries
from beanie import Document, Link
from pydantic import BaseModel

# locals
from .users import Users


class FacebookPostInfo(BaseModel):
    post_id: str
    comment_id: str


class DiscordPostInfo(BaseModel):
    post_id: str
    comment_id: str


class Posts(Document):
    # info
    created_at: datetime.datetime
    # TODO: remove optional and None
    created_by: Optional[Link[Users]] = None
    updated_at: datetime.datetime
    # TODO: remove optional and None
    updated_by: Optional[Link[Users]] = None
    raw_data: None

    # other service
    facebook_post: FacebookPostInfo
    discord_post: DiscordPostInfo

    # content
    title: str
    thumbnail_img: str
    banner_img: Optional[str]
    content: str
    author: str
    writed_at: datetime.date
    view: int

    # SEO
    description: str
    keywords: List[str]
    og_img: str

    class Settings:
        validate_on_save = True

    # event
