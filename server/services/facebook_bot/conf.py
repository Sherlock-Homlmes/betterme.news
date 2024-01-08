# libraries
import facebook

# local
from core.conf import settings

fb_client = facebook.GraphAPI(settings.FACEBOOK_ACCESS_TOKEN)

# # Extend the expiration time of a valid OAuth access token.
# extended_token = fb_client.extend_access_token(
#     settings.FACEBOOK_APP_ID,
#     settings.FACEBOOK_APP_SECRET
# )
# print(extended_token) #verify that it expires in 60 days
