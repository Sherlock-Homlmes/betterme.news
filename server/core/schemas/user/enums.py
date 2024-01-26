# default
from enum import Enum

# libraries
from fastapi import status


class ResponseStatusEnum(Enum):
    OK = status.HTTP_200_OK
    CREATED = status.HTTP_201_CREATED
    ACCEPTED = status.HTTP_202_ACCEPTED
    NO_CONTENT = status.HTTP_204_NO_CONTENT

    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED
    FORBIDDEN = status.HTTP_403_FORBIDDEN
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    RATE_LIMIT = status.HTTP_429_TOO_MANY_REQUESTS


class IvolunteerPageTagsEnum(Enum):
    VOLUNTEER = "Tình nguyện"
    CLUB = "CLB"
    COURSE = "Khoa hoc"
    SKILL = "Kĩ năng"
    SCHORLARSHIP = "Học bổng"
    EVENT = "Sự kiện"


class KhoahocTvPageTagsEnum(Enum):
    SOMETHING1 = "something1"
    SOMETHING2 = "something2"
