# default
import datetime
from typing import List

# libraries
from pydantic import BaseModel, Field


# CRAWL
class ScrapListPostParams(BaseModel):
    origin: str
    page: int = Field(default=1, gt=0)


class ScrapPostParams(BaseModel):
    origin: str


class KhoahocTvScrapPostResponse(BaseModel):
    pass


class KhoahocTvScrapDiscordPostResponse(KhoahocTvScrapPostResponse):
    pass


class KhoahocTvScrapHtmlPostResponse(KhoahocTvScrapPostResponse):
    pass


class IvolunteerVnScrapPostResponse(BaseModel):
    title: str
    deadline: datetime.date
    banner: str
    description: str


class IvolunteerVnScrapDiscordPostResponse(IvolunteerVnScrapPostResponse):
    content: List[str | List[str]]


class IvolunteerVnScrapHtmlPostResponse(IvolunteerVnScrapPostResponse):
    content: str


class ScrapPostResponse(BaseModel):
    discord: KhoahocTvScrapDiscordPostResponse | IvolunteerVnScrapDiscordPostResponse
    html: KhoahocTvScrapHtmlPostResponse | IvolunteerVnScrapHtmlPostResponse
