# libraries
import facebook


# local
from core.conf import settings
from core.models import SecretKeys, KeyTypeEnum

fb_client = None


# Extend the expiration time of a valid OAuth access token.
async def extend_expiration_time() -> str:
    extended_token = (
        fb_client.extend_access_token(settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
    )["access_token"]

    secret = await SecretKeys.find_one(SecretKeys.key_name == KeyTypeEnum.FACEBOOK_ACCESS_TOKEN)
    if secret:
        secret.value = extended_token
        secret.encode_value_on_save()
        await secret.save()
    else:
        await SecretKeys(
            key_name=KeyTypeEnum.FACEBOOK_ACCESS_TOKEN,
            value=extended_token,
        ).insert()

    return extended_token


async def connect_to_facebook_api():
    global fb_client

    settings.FACEBOOK_ACCESS_TOKEN = (
        await SecretKeys.find_one(SecretKeys.key_name == KeyTypeEnum.FACEBOOK_ACCESS_TOKEN)
    ).get_value()
    fb_client = facebook.GraphAPI(settings.FACEBOOK_ACCESS_TOKEN)
    await extend_expiration_time()
