# default
import datetime
from typing import List, Optional, Union

# libraries
from pydantic import BaseModel, Field


### CrawlersData.PY
# Types
DiscordContentType = List[Union[str, List[str]]]
HtmlContentType = str
# Models


class DiscordContent(BaseModel):
    content: DiscordContentType


class HtmlContent(BaseModel):
    content: HtmlContentType


class CrawlersData(BaseModel):
    title: str
    deadline: datetime.date
    banner: str
    description: str


class IvolunteerDiscordPost(CrawlersData, DiscordContent):
    pass


class IvolunteerHtmlPost(CrawlersData, HtmlContent):
    pass


class KhoahocTvDiscordPost(CrawlersData, DiscordContent):
    pass


class KhoahocTvHtmlPost(CrawlersData, HtmlContent):
    pass


# Params
class CrawlerListParams(BaseModel):
    origin: str
    page: int = Field(default=1, gt=0)


class CrawlersDataParams(BaseModel):
    origin: str


# Payloads
class PostCrawlersDataPayload(BaseModel):
    origin: str
    post_name: str

    banner: Optional[str]
    thumbnail: Optional[str]

    discord_content: DiscordContentType
    discord_description: str

    html_content: HtmlContentType
    html_description: str

    is_testing: Optional[bool] = False


class PatchCrawlersDataPayload(BaseModel):
    origin: str

    banner: Optional[str]
    thumbnail: Optional[str]

    discord_content: DiscordContentType
    discord_description: str

    html_content: HtmlContentType
    html_description: str


# Responses
class GetCrawlersDataResponse(BaseModel):
    discord: Union[KhoahocTvDiscordPost, IvolunteerDiscordPost]
    html: Union[KhoahocTvHtmlPost, IvolunteerHtmlPost]


### bot.py
class PatchBotPayload(BaseModel):
    start: bool = False
    stop: bool = True
