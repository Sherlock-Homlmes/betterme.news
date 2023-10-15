# mypy: disable-error-code="index"
# default
from typing import List

# local
from services.facebook import fb_client
from core.models import FacebookPostInfo


def post_to_fb(
    origin: str, image_name: str, content: str, comment: str, hashtags: List[str]
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
    fb_client.put_like(object_id=post["post_id"])

    # add comment
    comment = fb_client.put_comment(object_id=post["post_id"], message=comment)

    return FacebookPostInfo(
        post_id=post["post_id"],
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
