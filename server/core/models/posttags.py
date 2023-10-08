# libraries
from beanie import Document, Link

# locals
from .posts import Posts
from .tags import Tags


class PostTags(Document):
    post: Link[Posts]
    tag: Link[Tags]

    class Settings:
        validate_on_save = True
