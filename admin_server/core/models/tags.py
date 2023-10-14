# default

# libraries
from beanie import Document


class Tags(Document):
    name: str
    # children: List[Tags]
    # parents: List[Tags]

    class Settings:
        validate_on_save = True
