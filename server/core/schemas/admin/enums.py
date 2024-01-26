# default
from enum import Enum

# local


# CRAWL
class OriginCrawlPagesEnum(Enum):
    KHOAHOC_TV = "khoahoc_tv"
    IVOLUNTEER_VN = "ivolunteer_vn"


class CrawlerDataResponseTypeEnum(Enum):
    WEB = "html"
    DISCORD = "discord"
    FACEBOOK = "facebook"
