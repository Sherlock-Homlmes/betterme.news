# libraries
from beanie import Document, Link

# locals
from core.schemas import TagsEnum
from .posts import Posts


class PostTags(Document):
    post: Link[Posts]
    tag: TagsEnum

    class Settings:
        validate_on_save = True
