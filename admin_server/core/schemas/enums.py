# default
from enum import Enum

# libraries
# from fastapi import status
# local

# COMMON
# class ErrorRequest(Enum):
#     BAD_REQUEST: status.HTTP_400_
#     NOT_FOUND:
#     PERMISSION_DENIED:


# CRAWL
class OriginCrawlPagesEnum(Enum):
    KHOAHOC_TV = "khoahoc_tv"
    IVOLUNTEER_VN = "ivolunteer_vn"


# TODO: REWRITE
class OriginCrawlPageTagsEnum(Enum):
    KHOAHOC_TV_TAGS = ["something1", "something2"]
    IVOLUNTEER_VN_TAGS = [
        "tinh-nguyen",
        "clb",
        "khoa-hoc",
        "ki-nang",
        "hoc-bong",
        "su-kien",
        "viec-lam",
    ]


class ScrapDataResponseTypeEnum(Enum):
    HTML = "html"
    DISCORD = "discord"
    FACEBOOK = "facebook"
