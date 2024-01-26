# default
from typing import List

# libraries
from pydantic import BaseModel


def get_projections_from_model(pydantic_model: BaseModel, exclude_fields: List[str]) -> dict:
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
