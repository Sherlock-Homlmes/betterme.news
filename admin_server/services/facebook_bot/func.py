# mypy: disable-error-code="index"
# default
from typing import List, Optional

# local
from core.models import FacebookPostInfo
from .conf import fb_client


def post_to_fb(
    origin: str,
    content: str,
    comment: str,
    hashtags: Optional[List[str]] = [],
    image_name: Optional[str] = None,
) -> FacebookPostInfo:
    # add hashtag(s)
    content += "'\n"
    for hashtag in hashtags:
        content += "#" + hashtag + " "

    # create facebook post
    if image_name:
        post = fb_client.put_photo(image=open(image_name, "rb"), message=content)
    else:
        post = fb_client.put_object("me", "feed", message=content)

    # like post
    fb_client.put_like(object_id=post["id"])

    # add comment
    comment = fb_client.put_comment(object_id=post["id"], message=comment)

    return FacebookPostInfo(
        post_id=post["id"],
        comment_id=comment["id"],
    )


# TODO
def edit_fb_post():
    pass


# TODO
def edit_fb_comment():
    pass


# TODO
def delete_fb_post():
    pass
