# mypy: disable-error-code="no-redef, assignment"
from typing import Optional, Union

from pydantic import model_validator

# local
from .responses import *
from .enums import *
from utils.text_convertion import gen_slug

# TODO
# class GetPostListParams(GetPostListParams):
#     match_tag: Optional[Union[IvolunteerPageTagsEnum, KhoahocTvPageTagsEnum]] = None


class GetPostResponse(GetPostResponse):
    slug: str = ""

    @model_validator(mode="after")
    def gen_slug(cls, values):
        if not len(values.slug) and values.title:
            values.slug = gen_slug(values.title)
        return values
