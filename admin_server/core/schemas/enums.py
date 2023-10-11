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


class OriginCrawlPageTagsEnum(Enum):
    KHOAHOC_TV_TAGS = ()
    IVOLUNTEER_VN_TAGS = (
        "tinh-nguyen",
        "clb",
        "khoa-hoc",
        "ki-nang",
        "hoc-bong",
        "su-kien",
        "viec-lam",
    )


class ScrapDataResponseTypeEnum(Enum):
    HTML = "html"
    DISCORD = "discord"
    FACEBOOK = "facebook"
