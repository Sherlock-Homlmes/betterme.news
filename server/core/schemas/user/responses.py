# default
import datetime
from typing import List, Optional

# libraries
from pydantic import BaseModel


# TODO: duplicate code
class OtherPostInfo(BaseModel):
    deadline: datetime.date


# reponses
class GetPostResponse(BaseModel):
    # info
    created_at: datetime.datetime

    # content
    title: str
    description: str
    thumbnail_img: Optional[str] = None
    banner_img: Optional[str] = None
    content: str
    author: str
    other_information: Optional[OtherPostInfo] = None
    view: int
    tags: List[str]

    # SEO
    keywords: List[str]
    og_img: str
