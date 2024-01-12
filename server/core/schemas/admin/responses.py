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


# Params
class CrawlerListParams(BaseModel):
    origin: str
    page: int = Field(default=1, gt=0)


class CrawlersDataParams(BaseModel):
    origin: str


# Payloads
class PostCrawlersDataPayload(BaseModel):
    origin: str
    title: str

    banner: Optional[str]
    thumbnail: Optional[str]

    discord_content: DiscordContentType
    discord_description: str

    html_content: HtmlContentType
    html_description: str

    is_testing: bool = False


class PatchCrawlersDataPayload(BaseModel):
    origin: str

    banner: Optional[str]
    thumbnail: Optional[str]

    discord_content: DiscordContentType
    discord_description: str

    html_content: HtmlContentType
    html_description: str


class PostCrawlersPreviewDiscordDataPayload(BaseModel):
    origin: str
    preview_source: List[str]


# Responses
class GetCrawlersKhoahocTvDataResponse(BaseModel):
    title: str
    description: str
    banner: str
    thumbnail: str
    content: str


class GetCrawlersIvolunteerDataResponse(BaseModel):
    title: str
    description: str
    banner: str
    deadline: datetime.date
    content: str


### bot.py
class PatchBotPayload(BaseModel):
    action: str
