# mypy: disable-error-code="no-redef, assignment"
from typing import Optional, Union

from .responses import *
from .enums import *


class GetPostListParams(GetPostListParams):
    match_tag: Optional[Union[IvolunteerPageTagsEnum, KhoahocTvPageTagsEnum]] = None
