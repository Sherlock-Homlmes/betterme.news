# default
from enum import Enum

# libraries
from fastapi import status

# local


# COMMON
class ResponseStatusEnum(Enum):
    OK = status.HTTP_200_OK
    CREATED = status.HTTP_201_CREATED
    NO_CONTENT = status.HTTP_204_NO_CONTENT

    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED
    FORBIDDEN = status.HTTP_403_FORBIDDEN
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    RATE_LIMIT = status.HTTP_429_TOO_MANY_REQUESTS


# CRAWL
class OriginCrawlPagesEnum(Enum):
    KHOAHOC_TV = "khoahoc_tv"
    IVOLUNTEER_VN = "ivolunteer_vn"


class IvolunteerPageTagsEnum(Enum):
    VOLUNTEER = "tinh-nguyen"
    CLUB = "clb"
    COURSE = "khoa-hoc"
    SKILL = "ki-nang"
    SCHORLARSHIP = "hoc-bong"
    EVENT = "su-kien"
    WORK = "viec-lam"


class KhoahocTvPageTagsEnum(Enum):
    SOMETHING1 = "something1"
    SOMETHING2 = "something2"


# OriginCrawlPageTagsEnum = Enum(
#     'OriginCrawlPageTagsEnum',
#     [*list(map(lambda c: c.value, IvolunteerPageTagsEnum)),
#     *list(map(lambda c: c.value, KhoahocTvPageTagsEnum))]
# )


# class OriginCrawlPageTagsEnum(IvolunteerPageTagsEnum, KhoahocTvPageTagsEnum):
#     pass


class CrawlerDataResponseTypeEnum(Enum):
    HTML = "html"
    DISCORD = "discord"
    FACEBOOK = "facebook"
