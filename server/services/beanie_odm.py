# default
from typing import List, Optional

# libraries
from pydantic import BaseModel


def get_projections_from_model(
    pydantic_model: BaseModel, exclude_fields: Optional[List[str]] = []
) -> dict:
    something = pydantic_model.__fields__.keys()
    projections = {}
    for some in something:
        if some in exclude_fields:
            continue
        if some == "id":
            projections[some] = f"$_{some}"
        else:
            projections[some] = f"${some}"
    return projections


async def return_with_pagination(
    cursor,
    response,
    page: int,
    per_page: int,
):
    total_count = await cursor.count()
    response.headers["x-total-count"] = str(total_count)
    response.headers["x-current-page"] = str(page)
    response.headers["x-per-page"] = str(per_page)
