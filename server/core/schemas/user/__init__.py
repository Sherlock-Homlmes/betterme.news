# mypy: disable-error-code="no-redef, assignment"
from typing import Optional, Union

from pydantic import model_validator

# local
from .responses import *
from .enums import *
from services.text_convertion import gen_slug_from_title

# TODO
# class GetPostListParams(GetPostListParams):
#     match_tag: Optional[Union[IvolunteerPageTagsEnum, KhoahocTvPageTagsEnum]] = None


class GetPostResponse(GetPostResponse):
    slug: str = ""

    @model_validator(mode="after")
    def gen_slug_from_title(cls, values):
        if not len(values.slug) and values.title:
            values.slug = gen_slug_from_title(values.title)
        return values
