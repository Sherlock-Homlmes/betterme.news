# libraries
import facebook
from beanie.odm.operators.update.general import Set


# local
from core.conf import settings
from core.models import SecretKeys, KeyTypeEnum

fb_client = None


# Extend the expiration time of a valid OAuth access token.
async def extend_expiration_time() -> str:
    extended_token = (
        fb_client.extend_access_token(settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
    )["access_token"]

    secret_key = await SecretKeys.find_one(
        SecretKeys.key_name == KeyTypeEnum.FACEBOOK_ACCESS_TOKEN
    ).upsert(
        Set({SecretKeys.value: extended_token}),
        on_insert=SecretKeys(
            key_name=KeyTypeEnum.FACEBOOK_ACCESS_TOKEN,
            value=extended_token,
        ),
    )
    secret_key.value = extended_token
    await secret_key.save()

    return extended_token


async def connect_to_facebook_api():
    global fb_client

    settings.FACEBOOK_ACCESS_TOKEN = (
        await SecretKeys.find_one(SecretKeys.key_name == KeyTypeEnum.FACEBOOK_ACCESS_TOKEN)
    ).get_value()
    fb_client = facebook.GraphAPI(settings.FACEBOOK_ACCESS_TOKEN)
    await extend_expiration_time()
