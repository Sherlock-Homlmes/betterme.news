# default
import datetime
from typing import List, Optional, Union

# libraries
from pydantic import BaseModel


# TODO: remove duplicate code(using project beanie)
class OtherPostInfo(BaseModel):
    deadline: Optional[Union[datetime.date, None]] = None


# responses
class GetPostListResponse(BaseModel):
    id: str
    # custom data
    slug: str = ""
    # info
    updated_at: Union[datetime.datetime, None]
    created_at: datetime.datetime
    # content
    title: str
    description: str
    thumbnail_img: Optional[str] = None
    banner_img: Optional[str] = None
    tags: List[str]
    deadline: Optional[str] = datetime.date
    # SEO
    keywords: List[str]
    # other info
    view: int


class GetPostResponse(BaseModel):
    id: str
    # info
    created_at: datetime.datetime
    updated_at: Optional[str] = None

    # content
    title: str
    slug: str = ""
    description: str
    thumbnail_img: Optional[str] = None
    banner_img: Optional[str] = None
    content: str
    author: str
    author_link: Optional[str] = None
    other_information: Optional[OtherPostInfo] = None
    view: int
    tags: List[str]

    # SEO
    keywords: List[str]
    og_img: str


# reponses
class GetPostListParams(BaseModel):
    page: Optional[int] = 1
    per_page: Optional[int] = 10
    match_tags: Optional[str] = None
    match_search: Optional[str] = None


class GetPostParams(BaseModel):
    increase_view: Optional[bool] = True
