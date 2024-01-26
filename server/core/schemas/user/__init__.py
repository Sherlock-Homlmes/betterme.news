# mypy: disable-error-code="no-redef, assignment"
from typing import Optional, List, Union

from core.schemas.common import *
from .responses import *
from .enums import *


class GetPostListParams(GetPostListParams):
    match_tag: Optional[Union[IvolunteerPageTagsEnum, KhoahocTvPageTagsEnum]] = None
