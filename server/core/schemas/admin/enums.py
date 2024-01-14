# default
from enum import Enum

# local


# COMMON
class TagsEnum(Enum):
    SOMETHING1 = "SOMETHING1"
    SOMETHING2 = "SOMETHING2"
    SOMETHING3 = "SOMETHING3"


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
    WEB = "html"
    DISCORD = "discord"
    FACEBOOK = "facebook"
