# default
import datetime
from typing import List, Optional, Union

# libraries
from pydantic import BaseModel, Field


# TODO: remove duplicate code(using project beanie)
class OtherPostInfo(BaseModel):
    deadline: Optional[Union[datetime.date, None]] = None


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
    use_cache: bool = True


class CrawlersListDataParams(BaseModel):
    origin: str
    page: int = 1
    content_type: str


# Payloads
class PostCrawlersDataPayload(BaseModel):
    origin: str
    post_name: str


class PatchCrawlersDataPayload(BaseModel):
    title: Optional[str] = Field(min_length=1, default=None)
    description: Optional[str] = Field(min_length=1, default=None)
    banner: Optional[str] = None
    content: Optional[str] = Field(min_length=1, default=None)
    tags: Optional[List[str]] = Field(min_items=1, default=None)
    keywords: Optional[List[str]] = Field(min_items=1, default=None)


class PostCrawlersPreviewDiscordDataPayload(BaseModel):
    origin: str
    preview_source: List[str]


# Responses
class GetCrawlersKhoahocTvDataResponse(BaseModel):
    title: str
    description: str
    tags: List[str]
    banner: str
    thumbnail: str
    content: str
    keywords: List[str]


class GetCrawlersIvolunteerDataResponse(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    tags: List[str]
    banner: str
    deadline: Union[datetime.date, None]
    content: str
    keywords: List[str]


class PostCrawlersResponse(BaseModel):
    id: str


### bot.py
class PatchBotPayload(BaseModel):
    action: str


### tags.py
# Params
class GetTagsParams(BaseModel):
    origin: str


### posts.py
# Payload
class PostPostPayload(BaseModel):
    title: str = Field(min_length=1, default=None)
    description: str = Field(min_length=1, default=None)
    banner: str
    deadline: Optional[datetime.date] = None
    content: str = Field(min_length=1, default=None)
    tags: List[str] = Field(min_items=1, default=None)
    keywords: List[str] = Field(min_items=1, default=None)


class PatchPostPayload(BaseModel):
    title: Optional[str] = Field(min_length=1, default=None)
    description: Optional[str] = Field(min_length=1, default=None)
    banner: Optional[str] = None
    other_information: Optional[OtherPostInfo] = None
    content: Optional[str] = Field(min_length=1, default=None)
    tags: Optional[List[str]] = Field(min_items=1, default=None)
    keywords: Optional[List[str]] = Field(min_items=1, default=None)


### draftposts.py
class GetDraftPostListResponse(BaseModel):
    id: str
    source: str
    name: str
    original_data: GetCrawlersIvolunteerDataResponse
    draft_data: GetCrawlersIvolunteerDataResponse
    post: Union[str, None]


# ai.py
class PostAIPromtPayload(BaseModel):
    prompt_type: str
    context: str = Field(max_length=6000)
