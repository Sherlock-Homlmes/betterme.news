from enum import Enum


class SomethingEnum(Enum):
    something1 = 1
    something2 = 2
    something3 = 3


class SomethingEnum2(Enum):
    something1 = "10"
    something2 = "20"
    something3 = "30"


class ABCEnum2(Enum):
    abc1 = "abc1"
    abc2 = "abc2"
    abc3 = "abc3"
