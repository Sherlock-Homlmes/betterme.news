# default
from typing import Annotated, List, Union

# libraries
from fastapi import APIRouter, Depends

# local
from core.schemas.admin import (
    # params
    GetTagsParams,
    # responses
    ResponseStatusEnum,
    # enums
    OriginCrawlPagesEnum,
    IvolunteerPageTagsEnum,
    KhoahocTvPageTagsEnum,
)

# from services.time_modules import Time

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/tags",
    tags=["Tags"],
    status_code=ResponseStatusEnum.OK.value,
)
def get_tags(
    params: Annotated[dict, Depends(GetTagsParams)],
) -> List[Union[IvolunteerPageTagsEnum, KhoahocTvPageTagsEnum]]:
    origin = params.origin
    # TODO: refactor: conditions, better enum class, multi tags
    if origin == OriginCrawlPagesEnum.IVOLUNTEER_VN:
        return [item.value for item in IvolunteerPageTagsEnum]
    if origin == OriginCrawlPagesEnum.KHOAHOC_TV:
        return [item.value for item in KhoahocTvPageTagsEnum]
    return []
