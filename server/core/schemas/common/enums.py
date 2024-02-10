from enum import Enum


class BeanieWriteRulesEnum(Enum):
    # The next call will insert a new field(link) and replace the Object instance with updated data
    WRITE = "WRITE"
    # The next call will just replace the Object instance with new data, but the field(linked) will not be synced
    DO_NOTHING = "DO_NOTHING"
